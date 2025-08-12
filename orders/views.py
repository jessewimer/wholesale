from rest_framework import viewsets
from .serializers import OrderSerializer
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
import datetime
from .models import Order, OrderIncludes  # Adjust imports based on your models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings





def get_order_id_by_number(request, order_number):
    """
    API endpoint to get order ID by order number
    """
    try:
        order = Order.objects.get(order_number=order_number)
        return JsonResponse({'order_id': order.id})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

def generate_order_pdf(request, order_id):
    try:

        # Get the order and items
        order = get_object_or_404(Order, id=order_id)
        order_includes = OrderIncludes.objects.filter(order=order).select_related('product')

        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )

        elements = []
        styles = getSampleStyleSheet()

        # Custom styles
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=8,
            textColor=colors.HexColor('#2d4a22'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#4a5568'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        )

        # Header
        elements.append(Paragraph("UPRISING SEEDS", header_style))
        elements.append(Paragraph("Wholesale Order Summary", subheader_style))
        elements.append(Spacer(1, 20))

        # Order info
        # current_date = datetime.date.today().strftime("%B %d, %Y")
        elements.append(Paragraph(f"<b>Order Number:</b> {order.order_number}", styles['Normal']))
        elements.append(Paragraph(f"<b>Order Date:</b> {order.order_date.strftime('%B %d, %Y') if order.order_date else 'N/A'}", styles['Normal']))

        if hasattr(order, 'store') and order.store:
            elements.append(Paragraph(f"<b>Store:</b> {order.store.name}", styles['Normal']))

        elements.append(Spacer(1, 25))

        # Items table
        elements.append(Paragraph("Order Items", styles['Heading2']))

        table_data = [['Qty', 'Variety', 'Type', 'Unit Price', 'Subtotal']]
        pkt_price = settings.PACKET_PRICE
        total_cost = 0
        for item in order_includes:
            quantity = item.quantity or 0
            variety = item.product.variety if item.product else 'N/A'
            veg_type = item.product.veg_type if item.product else 'N/A'
            # unit_price = item.product.price if item.product else 0
            line_total = quantity * pkt_price

            # Truncate long variety names
            if len(variety) > 35:
                variety = variety[:32] + "..."

            table_data.append([
                str(quantity),
                variety,
                veg_type,
                f"${pkt_price:.2f}",
                f"${line_total:.2f}"
            ])

            total_cost += line_total

        # Create and style table
        items_table = Table(table_data, colWidths=[0.6*inch, 3.2*inch, 1.2*inch, 0.8*inch, 0.8*inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d4a22')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Qty centered
            ('ALIGN', (1, 1), (2, -1), 'LEFT'),    # Variety and type left
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),  # Prices right

            # Styling
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))

        elements.append(items_table)
        elements.append(Spacer(1, 25))

        # Totals
        elements.append(Paragraph("Order Summary", styles['Heading2']))

        totals_data = [
            ['Subtotal:', f"${total_cost:.2f}"],
            ['Shipping:', 'TBD'],
            ['Total:', 'TBD']
        ]

        totals_table = Table(totals_data, colWidths=[4.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        elements.append(totals_table)
        elements.append(Spacer(1, 30))

        # Footer
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6c757d'),
            alignment=TA_CENTER
        )

        elements.append(Paragraph("Thank you for your wholesale order!", footer_style))
        elements.append(Paragraph("For questions, please contact us through our wholesale portal.", footer_style))

        # Build PDF
        doc.build(elements)

        pdf_data = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Uprising - {order.order_number}.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", content_type='text/plain')


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(pulled_for_processing=False)
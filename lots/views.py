from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def send_germ_samples(request):

    context = {
        'page_title': 'Send Germination Samples',
        # Add placeholder data - replace with real data later
        'pending_samples': [
            {
                'sample_id': 'GS-2024-001',
                'variety': 'Cherokee Purple Tomato',
                'batch': 'CPT-2024-03',
                'requested_date': '2024-08-12',
                'status': 'pending'
            },
            {
                'sample_id': 'GS-2024-002',
                'variety': 'Blue Kuri Squash',
                'batch': 'BKS-2024-01',
                'requested_date': '2024-08-10',
                'status': 'sent'
            },
        ],
        'total_pending': 1,
        'total_sent': 1,
    }
    
    # Adjust template path based on where your templates are located
    return render(request, 'office/send_germ_samples.html', context)


# Update your existing process_orders and view_stores views if needed:
@login_required
def inventory(request):
    context = {}

    # Point to lots app template if that's where it's located
    return render(request, 'lots/inventory.html', context)
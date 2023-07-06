#send an email to the store owner
def send_email(order):
    import csv
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    data = order.products

    filename = 'data.csv'
    subject = f'{order.store.name} - Order #{order.order_number}'
    subject2 = f'Uprising Seeds - Order #{order.order_number}'
    body = f'Order was placed successfully.'
    
    # Set up the email content
    sender_email = 'ndefe@outlook.com'
    uprising_email = 'wholesale@uprisingorganics.com'
    store_email = order.store.email

    password = '********'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = uprising_email
    message['Subject'] = subject

    message2 = MIMEMultipart(body)
    message2['From'] = sender_email
    message2['To'] = store_email
    message2['Subject'] = subject2

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in data.items():
            writer.writerow([key, value])

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(open(filename, 'rb').read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(attachment)

    # Log in to the SMTP server
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
    smtp_obj.starttls()
    smtp_obj.login(sender_email, password)

    # Send the email
    smtp_obj.sendmail(sender_email, uprising_email, message.as_string())
    smtp_obj.sendmail(sender_email, store_email, message2.as_string())
    smtp_obj.quit()

    print('Emails sent successfully')
    return 

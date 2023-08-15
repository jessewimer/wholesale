#send an email to the store owner
import json

# Load the configuration data from config.json
with open('config.json') as config_file:
    config_data = json.load(config_file)

# Access the email password, API key, and username
sender_email = config_data.get('sender_email')
password = config_data.get('password')
uprising_email = config_data.get('uprising_email')

# !!!! for some reason the store is not being passed to the send_email function
def send_email(order):
    import csv
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    data = order.products
    print(order.products)
    
    filename = 'data.csv'
    subject = f'{order.store.name} - Order #{order.order_number}'
    #subject = f'Order #{order.order_number}'
    subject2 = f'Uprising Seeds - Order #{order.order_number}'
    body = f'Order was placed successfully.'
    
    #store_email = order.store.email

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = uprising_email
    message['Subject'] = subject

    # Uncomment following lines to send email to store owner
    # message2 = MIMEMultipart(body)
    # message2['From'] = sender_email
    # message2['To'] = store_email
    # message2['Subject'] = subject2

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
    #smtp_obj.sendmail(sender_email, store_email, message2.as_string())
    smtp_obj.quit()

    print('Emails sent successfully')
    return 

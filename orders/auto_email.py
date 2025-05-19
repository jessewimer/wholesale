## Todo: enable emails to be sent to store owners ##
import os
import base64
from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
api_key = config('SENDGRID_API')

# Accessing the email password, and username
uprising_email = config('UPRISING_EMAIL')

def send_email(order):
    import csv
    data = order.products
    csv_filename = 'data.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in data.items():
            writer.writerow([key, value])

    # Email parameters
    from_email = uprising_email
    #to_email = 'jesse.wimer@wsu.edu'
    to_email = 'moonbreakfarm@gmail.com'
    subject = subject = f'{order.store.name} - Order #{order.order_number}'
    content = 'Please find the attached CSV file.'

    # Create a message
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )

    with open(csv_filename, "rb") as file:
        file_data = file.read()
        file_encoded = base64.b64encode(file_data).decode()

    # Create an attachment
    attachment = Attachment()
    attachment.file_content = FileContent(file_encoded)
    attachment.file_name = FileName(csv_filename)
    attachment.file_type = FileType("application/csv")
    attachment.disposition = "attachment"
    message.attachment = attachment


    sg = SendGridAPIClient(api_key)
    response = sg.send(message)

    # Check if the email was sent successfully
    if response.status_code == 202:
        print('Email sent successfully!')
    else:
        print('Failed to send email. Status code:', response.status_code)

def send_test_email():
    # import csv
    # data = order.products
    # csv_filename = 'data.csv'
    # with open(csv_filename, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     for key, value in data.items():
    #         writer.writerow([key, value])

    # Email parameters
    from_email = uprising_email
    to_email = 'moonbreakfarm@gmail.com'
    subject = subject = f'Test 8-20'
    content = 'Please find the attached CSV file.'

    # Create a message
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )

    # with open(csv_filename, "rb") as file:
    #     file_data = file.read()
    #     file_encoded = base64.b64encode(file_data).decode()

    # Create an attachment
    # attachment = Attachment()
    # attachment.file_content = FileContent(file_encoded)
    # attachment.file_name = FileName(csv_filename)
    # attachment.file_type = FileType("application/csv")
    # attachment.disposition = "attachment"
    # message.attachment = attachment


    sg = SendGridAPIClient(api_key)
    response = sg.send(message)

    # Check if the email was sent successfully
    if response.status_code == 202:
        print('Email sent successfully!')
    else:
        print('Failed to send email. Status code:', response.status_code)


send_test_email()

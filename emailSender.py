import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import qrcode
import base64
from io import BytesIO

SENDGRID_API_KEY = 'API_KEY'

def send_email():
    sender_email = 'Sender_Email'
    receiver_email = 'Reciever_Email'

    # Generate the QR code
    img = qrcode.make('Hello World')

    # Create a BytesIO object to hold the image in memory
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    
    # Get the image data
    buffered.seek(0)
    data = buffered.read()
    encoded = base64.b64encode(data).decode()

    # Create the attachment
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('image/png')
    attachment.file_name = FileName('qrcode.png')
    attachment.disposition = Disposition('inline')
    attachment.content_id = 'qr_code_img'

    # Create the email message
    message = Mail(
        from_email=sender_email,
        to_emails=receiver_email,
        subject='QR Code Check In',
        plain_text_content='Hello, World!',
        html_content='<img src="cid:qr_code_img">'
    )

    message.add_attachment(attachment)

    try:
        api = SendGridAPIClient(SENDGRID_API_KEY)
        response = api.send(message)
        print(f'Email sent! Status Code: {response.status_code}')
    except Exception as e:
        print(f'Error sending email: {e}')

if __name__ == '__main__':
    send_email()

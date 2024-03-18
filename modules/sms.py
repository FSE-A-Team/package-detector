import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_sms_via_email(sms_gateway, message, google_account, google_password):
    """
    Sends an SMS message via an email gateway.

    Parameters:
        sms_gateway (str): The recipient's SMS gateway (e.g., '1234567890@carrier.com').
        message (str): The message to send.
        google_account (str): Your Google/Gmail account.
        google_password (str): Your Google/Gmail password or App Password.
    """

    # Create the message
    email_msg = MIMEMultipart()
    email_msg['From'] = google_account
    email_msg['To'] = sms_gateway
    email_msg['Subject'] = 'SMS via Email'  # You can change or remove the subject
    email_msg.attach(MIMEText(message, 'plain'))

    # Server setup
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(google_account, google_password)

    # Send the email
    text = email_msg.as_string()
    server.sendmail(google_account, sms_gateway, text)
    server.quit()

    print("SMS sent successfully.")


#send_sms_via_email('holgate.mark1@gmail.com', 'Hello, World!', 'raspberrypi.apps@gmail.com', 'password')
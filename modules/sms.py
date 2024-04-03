import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from modules import crypto



def send_sms_via_email(sms_gateway, message):
    """
    Sends an SMS message via an email gateway.

    Parameters:
        sms_gateway (str): The recipient's SMS gateway (e.g., '1234567890@carrier.com').
        message (str): The message to send.
        google_account (str): Your Google/Gmail account.
        google_password (str): Your Google/Gmail password or App Password.
    """
    global account, password
    # Create the message
    email_msg = MIMEMultipart()
    email_msg['From'] = account
    email_msg['To'] = sms_gateway
    #email_msg['Subject'] = 'SMS via Email'  # You can change or remove the subject
    email_msg['MIME-Version'] = '1.0'
    email_msg.add_header('Content-Type', 'text/plain; charset="UTF-8"')
    
    email_msg.attach(MIMEText(message, 'plain', 'utf-8'))
    headers = ["From: " + account,
                "To: " + sms_gateway,
                "MIME-Version: 1.0",
                "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    text = headers + "\r\n\r\n" + message

    # Server setup
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(account, password)

    # Send the email
    #text = email_msg.as_string()
    server.sendmail(account, sms_gateway, text)
    server.quit()

    print("SMS sent successfully.")

def set_credentials(credentialDict):
    """
    Sets the global account and password variables to the specified values.

    Parameters:
        account (str): Your Google/Gmail account.
        password (str): Your Google/Gmail password or App Password.
    """
    global account, password
    account = credentialDict['login']
    password = crypto.decrypt_credentials(credentialDict)

def get_credentials():
    """
    Returns the global account and password variables.

    Returns:
        str: Your Google/Gmail account.
        str: Your Google/Gmail password or App Password.
    """
    global account, password
    return account, password
#send_sms_via_email('holgate.mark1@gmail.com', 'Hello, World!', 'raspberrypi.apps@gmail.com', 'password')


"""

Mobile carrier	SMS gateway domain	MMS gateway domain
Alltel	sms.alltelwireless.com	mms.alltelwireless.com
AT&T	txt.att.net	mms.att.net
Boost Mobile	sms.myboostmobile.com	myboostmobile.com
Cricket Wireless	mms.cricketwireless.net	mms.cricketwireless.net
MetroPCS	mymetropcs.com	mymetropcs.com
Google Fi	 	msg.fi.google.com
Republic Wireless	text.republicwireless.com	 
Sprint	messaging.sprintpcs.com	pm.sprint.com
T-Mobile	tmomail.net	tmomail.net
U.S. Cellular	email.uscc.net	mms.uscc.net
Verizon Wireless	vtext.com	vzwpix.com
Virgin Mobile	vmobl.com	vmpix.com
SMS gateway domains for Canadian carriers:

Mobile carrier	SMS gateway domain
Bell Canada	txt.bell.ca
Bell MTS	text.mts.net
Fido Solutions	fido.ca
Freedom Mobile	txt.freedommobile.ca
Koodo Mobile	msg.koodomobile.com 
msg.telus.com

PC Mobile	mobiletxt.ca
Rogers Communications	pcs.rogers.com
SaskTel	sms.sasktel.com
Telus	msg.telus.com

"""
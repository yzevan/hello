# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


from smtplib import SMTPException, SMTPAuthenticationError
import string
import base64
import sspi

# NTLM Guide -- http://curl.haxx.se/rfc/ntlm.html

SMTP_EHLO_OKAY = 250
SMTP_AUTH_CHALLENGE = 334
SMTP_AUTH_OKAY = 235

def asbase64(msg):
    return string.replace(base64.encodestring(msg), '\n', '')

def connect_to_exchange_as_current_user(smtp):
    """Example:
    >>> import smtplib
    >>> smtp = smtplib.SMTP("my.smtp.server")
    >>> connect_to_exchange_as_current_user(smtp)
    """

    # Send the SMTP EHLO command
    code, response = smtp.ehlo()
    if code != SMTP_EHLO_OKAY:
        raise SMTPException("Server did not respond as expected to EHLO command")

    sspiclient = sspi.ClientAuth('NTLM')

    # Generate the NTLM Type 1 message
    sec_buffer=None
    err, sec_buffer = sspiclient.authorize(sec_buffer)
    ntlm_message = asbase64(sec_buffer[0].Buffer)

    # Send the NTLM Type 1 message -- Authentication Request
    code, response = smtp.docmd("AUTH", "NTLM " + ntlm_message)

    # Verify the NTLM Type 2 response -- Challenge Message
    if code != SMTP_AUTH_CHALLENGE:
        raise SMTPException("Server did not respond as expected to NTLM negotiate message")

    # Generate the NTLM Type 3 message
    err, sec_buffer = sspiclient.authorize(base64.decodestring(response))
    ntlm_message = asbase64(sec_buffer[0].Buffer)

    # Send the NTLM Type 3 message -- Response Message
    code, response = smtp.docmd("", ntlm_message)
    if code != SMTP_AUTH_OKAY:
        raise SMTPAuthenticationError(code, response)



me = "evan_wang@trendmicro.com.cn"
you = "evan_wang@trendmicro.com.cn"

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
#fp = open(textfile, 'rb')
# Create a text/plain message
msg = MIMEText("this is a test")
#fp.close()

# me == the sender's email address
# you == the recipient's email address
#msg['Subject'] = 'The contents of %s' % textfile
msg['Subject'] = "Test"
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('cdcexcas.tw.trendnet.org', 25)
connect_to_exchange_as_current_user(s)
s.sendmail(me, [you], msg.as_string())
s.quit()

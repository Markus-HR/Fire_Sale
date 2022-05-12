import smtplib
from email.message import EmailMessage

EmailAddress = "firesale.group60@gmail.com"
Password = "BuglesPepsi"


def sendmail(email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EmailAddress
    msg['To'] = email
    msg.set_content(message)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EmailAddress, Password)
        smtp.send_message(msg)

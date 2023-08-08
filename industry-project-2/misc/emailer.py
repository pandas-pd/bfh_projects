import smtplib
from email.mime.text import MIMEText
import cdsapi

def send_email(subject, body, sender, recipients, password):

    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())

    smtp_server.quit()

    return

def message(body = "sample", to = "joel.tauss@gmail.com"):

    recipients = [to]

    subject = "Copernicus data gathering"

    sender = "pythonmailer418@gmail.com"
    password = "ukbxhznembqulfva"

    try:
        send_email(subject, body, sender, recipients, password)
    except:
        print("An error occured while sending the mail")

if __name__ == "__main__":
    message()
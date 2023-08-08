import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

class Email():
    """
    Sending emails with images of detected objects.
    """

    def __init__(self,message, to):
        """
        Constructor sets up smtp server and logs into gmail account. 
        If you like to use your own account, make sure to enable "2-factor-auth" and then create an app password. Use app password to login
        """

        self.gmail_user = 'object.detector.btw2403@gmail.com'
        self.gmail_password = '54dhsasdase3hzt!'
        self.app_password = 'etorulwqtsqmfcgc'

        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465) #465 = smtp over ssl 
            self.server.ehlo()
            #self.server.starttls() #does not work
            self.server.login(self.gmail_user, self.app_password)
        except Exception as e:
            print ('Something went wrong...', e)
        
        self.send_mail(message, to)

    def send_mail(self,message, to):
        """
        Change email receiver adress here. Add multiple addresses to the list, if needed.
        """

        sent_from = self.gmail_user
        subject = "Machine Learning modul"

        msg = MIMEMultipart()
        
        msg['subject']  = subject
        msg['to']       = to
        msg['from']     = sent_from
        
        msg.attach(MIMEText(message))

        """path= os.path.join(os.path.dirname(os.path.abspath(__file__)),"image.jpg")
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format("image.jpg"))
        msg.attach(part)"""


        try:
            self.server.send_message(msg)
            self.server.close()

            print ('Email sent!')

        except Exception as e:
            print ('Something went wrong...', e)
            self.server.close()

        

if __name__ == '__main__':
    Email("this is a test", "joel.tauss@gmail.com")

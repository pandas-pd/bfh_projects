import smtplib

class New_mail():

    def __init__(self,message):

        """
        Constructor sets up smtp server and logs into gmail account. 
        If you like to use your own account, make sure to enable "allow unsecure app" in your gmail account settings.
        """

        self.gmail_user = 'email'
        self.gmail_password = 'password'

        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(self.gmail_user, self.gmail_password)
        except Exception as e:
            print ('Something went wrong...', e)
        
        self.send_mail(message)

    def send_mail(self,message):
        """
        Change email receiver adress here. Add multiple addresses to the list, if needed.
        """

        sent_from = self.gmail_user
        to = ['kobimarth@gmail.com'] #change receiver here
        subject = 'Trade Server Warning'

        email_text = f"""\
        From: {sent_from}
        To: {", ".join(to)}
        Subject: {subject}

        {message}
        """

        try:
            self.server.sendmail(sent_from, to,email_text)
            self.server.close()

            print ('Email sent!')
        except Exception as e:
            print ('Something went wrong...', e)

if __name__ == '__main__':
    New_mail("raspian test")
        

import smtplib

def sendMail(SUBJECT = "",TEXT = ""): ## FUNCTION FACILITATING

        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText
        
        msg = MIMEMultipart()

        msg['From'] = 'rafa@libring.com'
        msg['To'] = 'rafa@libring.com'
        msg['Subject'] = SUBJECT

        text = TEXT


        msg.attach(MIMEText(text))

        mailServer = smtplib.SMTP("smtp.1and1.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login('rafa@libring.com', 'SuperRafa2013')
        mailServer.sendmail('rafa@libring.com', 'rafa@libring.com', msg.as_string())
        # Should be mailServer.quit(), but that crashes...
        mailServer.close()

sendMail('TEST','IT WORKED')
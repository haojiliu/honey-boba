#!/usr/bin/python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText

import constants

def send(receivers, subject, body):
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.login(constants.CONST_EMAILER_SENDER, constants.CONST_EMAILER_PASSWORD)

  msg = MIMEMultipart()
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = ','.join(receivers)
  msg.attach(MIMEText(body, 'plain'))
  txt = msg.as_string()
  try:
    print('going to send an email!!')
    server.sendmail(sender, receivers, txt)
    print("Successfully sent email")
    return True
  except:
    print("Error: unable to send email")
    return False

#!/usr/bin/python
import smtplib, logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText

from jinja2 import Environment, PackageLoader

import constants

env = Environment(loader=PackageLoader('emailer', 'templates'))
new_review_template = env.get_template('notification_new_review.html')
new_upload_template = env.get_template('notification_new_upload.html')

def send_html(receivers, subject, body):
  sender = constants.CONST_EMAILER_SENDER
  server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
  # server.ehlo()
  # server.starttls()
  server.login(sender, constants.CONST_EMAILER_PASSWORD)

  msg = MIMEMultipart()
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = ','.join(receivers)
  msg.attach(MIMEText(body, 'html'))
  txt = msg.as_string()
  try:
    server.sendmail(sender, receivers, txt)
    logging.warning("Successfully sent email")
    return True
  except:
    logging.warning("Error: unable to send email")
    return False

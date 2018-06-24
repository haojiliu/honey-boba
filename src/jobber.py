import time

from model import Notification, User

from session_factory import create_session
import utils
import constants
import emailer
import logic as l

def build_email_body(designs_dict):
  return emailer.new_review_template.render(designs_dict=designs_dict)

def send_notifications():
  try:
    context = {}
    with create_session() as s:
      last_notification_sent = s.query(Notification).order_by(Notification.id.desc()).first()
      last_timestamp = float(last_notification_sent.created_at_utc) if last_notification_sent else -1
      print('last sent at %s' % last_timestamp)

      for user in l._get_users(s):
        context[user.id] = {}
        total_num_of_reviews = 0
        for design in user.designs:
          if len(design.reviews) > 0:
            context[user.id][design.uri] = {
              'name': design.description,
              'reviews': []
            }
            for review in design.reviews:
              if float(review.created_at_utc) > last_timestamp:
                new_review = {
                  'body': review.body,
                  'timestamp': utils.epoch_to_datetime_string(review.created_at_utc)
                }
                context[user.id][design.uri]['reviews'].append(new_review)
                total_num_of_reviews = total_num_of_reviews + 1
        if not total_num_of_reviews:
          subject = 'A summary of your recent design submissions'
          body = emailer.new_review_template.render(designs_dict=context[user.id])
          receivers = [user.email]
          emailer.send_html(receivers, subject, body)
        else:
          print('no new reviews on this user, skip sending email')
      o = Notification()
      o.updated_at_utc = time.time()
      s.add(o)
  except:
    raise
    return 'Failed'

while True:
  send_notifications()
  time.sleep(constants.CONST_EMAIL_DIGEST_INTERVAL_IN_SECONDS)

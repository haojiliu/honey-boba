from datetime import date
import time, datetime, logging

from model import Notification, Review, ReviewObject, Thumbnail, Comment, User

from session_factory import create_session
import utils
import constants
import emailer

def thumbnail(input_filepath, uri):
  for size_tuple in constants.THUMBNAIL_SIZE_TUPLE_TO_SIZE_CODE:
    size_code = constants.THUMBNAIL_SIZE_TUPLE_TO_SIZE_CODE[size_tuple]
    filename = utils.thumbnail(input_filepath, uri, size_tuple)
    touch_thumbnail(uri, filename, size_code)

def create_a_comment(body):
  try:
    with create_session() as s:
      o = Comment()
      o.body = body
      s.add(o)
    return ''
  except Exception as e:
    logging.warning(e)
    return 'Write a comments failed'

def get_reviews(uris=None, timestamp=None):
  try:
    context = []
    with create_session() as s:
      reviews = _get_reviews(s, uris=uris, timestamp=None)
      for review in reviews:
        new_review = {
          'body': review.body,
          'timestamp': utils.epoch_to_datetime_string(review.created_at_utc)
        }
        context.append(new_review)
    return context
  except:
    raise
    return 'Failed'

def get_all_active_designs(uris=None):
  """This is the api endpoint to get all related information for designs
  i.e, reviews, thumbnail image links, user info, upvotes, etc.

  Returns: list of dicts
  """
  try:
    context = []
    with create_session() as s:
      designs = _get_review_objects(s, uris=uris)
      for design in designs:
        new_design = {
          'uri': design.uri,
          'name': design.name,
          'desc': design.description,
          'uid': design.user.id if design.user else None,
          'updated_at_utc': utils.epoch_to_datetime_string(design.updated_at_utc),
          'reviews': []
        }
        for review in design.reviews:
          new_design['reviews'].append({
            'body': review.body,
            'timestamp': utils.epoch_to_datetime_string(review.created_at_utc)
          })
        new_design['reviews'].reverse()
        for thumbnail in design.thumbnails:
          if thumbnail.size_code == constants.SIZE_CODE_LARGE:
            new_design['thumbnail_uri'] = utils.build_thumbnail_filepath(
                thumbnail.review_object_uri, thumbnail.filename)
        context.append(new_design)
    logging.warning(context)
    return context
  except:
    raise
    return 'Failed'

def create_a_review(review_object_uri, body, email=None):
  try:
    with create_session() as s:
      r = _get_review_objects(s, [review_object_uri])
      if not r:
        return 'Invalid review object uri'
      o = Review()
      o.review_object_uri = review_object_uri
      o.body = body
      # touch time
      o.updated_at_utc = time.time()
      s.add(o)
    return ''
  except:
    raise
    return 'Failed to post a review, please try again.'

def touch_thumbnail(review_object_uri, filename, size_code):
  try:
    with create_session() as s:
      o = _get_thumbnail(s, [review_object_uri], [filename])
      if not o:
        o = Thumbnail()
      else:
        o = o[0]
        logging.warning('updating existing thumbnail')
      o.review_object_uri = review_object_uri
      o.filename = filename
      o.size_code = size_code
      # touch time
      o.updated_at_utc = time.time()
      s.add(o)
    return 'touch thumbnail succeeded'
  except:
    raise
    return 'Failed'

def touch_user(s, email):
  o = _get_user_by_email(s, email)
  if not o:
    logging.warning('user not exist, creating a new one...')
    o = User()
    o.email = email
    # touch time
    o.updated_at_utc = time.time()
    s.add(o)
    s.flush()
    return o
  return o[0]

def touch_review_object(uri, filename=None, email=None, name=None, description=None):
  try:
    with create_session() as s:
      o = _get_review_objects(s, [uri])
      if not o:
        o = ReviewObject()
      else:
        o = o[0]
        logging.warning('updating existing design')
      if filename:
        logging.warning('updating filename!!')
        o.filename = filename
      # always update name and desc
      logging.warning('updating desc!')
      o.description = description
      logging.warning('updating name!')
      o.name = name

      if not o.uri:
        o.uri = uri
      else:
        logging.warning('not updating uri for existing design')
      # touch time
      o.updated_at_utc = time.time()

      # try create the user
      if email:
        user = touch_user(s, email)
        o.uid = user.id
        logging.warning('the user id is: %s' % o.uid)
      s.add(o)
    return 'touch design succeeded'
  except:
    raise
    return 'Failed'

def _get_thumbnail(session, review_object_uris=None, filenames=None):
  """Return a list of Thumbnail"""
  q = session.query(ReviewObject)
  if review_object_uris:
    q = q.filter(ReviewObject.uri.in_(review_object_uris))
  if filenames:
    q = q.filter(ReviewObject.filename.in_(filenames))
  return q.all()

def _get_review_objects(session, uris):
  """Return a list of ReviewObject"""
  q = session.query(ReviewObject)
  q = q.filter(ReviewObject.flags == constants.CONST_FLAGS_ACTIVE)
  if uris:
    q = q.filter(ReviewObject.uri.in_(uris))
  q = q.order_by(ReviewObject.id.desc())

  return q.all()

def _get_users(session):
  q = session.query(User)
  return q.all()

def _get_user_by_email(session, email):
  """Return a list of ReviewObject"""
  q = session.query(User)
  q = q.filter(User.email == email)
  return q.all()

def _get_reviews(session, uris, timestamp):
  """Return a list of ReviewObject"""
  q = session.query(Review)
  if uris:
    q = q.filter(Review.review_object_uri.in_(uris))
  if timestamp:
    q = q.filter(Review.created_at_utc > timestamp)

  q = q.order_by(Review.id.desc())

  return q.all()

def get_email_by_uid(uid):
  with create_session() as session:
    q = session.query(User)
    q = q.filter(User.id == uid)
    user = q.first()
    return user.email if user else ''

def get_review_objects(uris=None):
  """Return a list of ReviewObject object in strings"""
  with create_session() as s:
    return _get_review_objects(s, uris)

def delete_review_objects(uris):
  try:
    with create_session() as s:
      for o in _get_review_objects(s, uris):
        if o.flags == constants.CONST_FLAGS_INACTIVE:
          return 'Design already deleted'
        o.flags = o.flags | constants.CONST_FLAGS_INACTIVE
  except:
    raise
    return 'Delete failed'
  return ''

def report_review_objects(uris):
  try:
    with create_session() as s:
      for o in _get_review_objects(s, uris):
        if o.flags & constants.CONST_FLAGS_REPORTED:
          return 'Design already reported'
        o.flags = o.flags | constants.CONST_FLAGS_INACTIVE
        o.flags = o.flags | constants.CONST_FLAGS_REPORTED
  except:
    raise
    return 'Report failed'
  return ''

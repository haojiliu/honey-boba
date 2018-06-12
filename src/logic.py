from datetime import date
import time, datetime

from model import Notification, Review, ReviewObject, Thumbnail

from session_factory import create_session
import utils
import constants

def thumbnail(input_filepath, uri):
  for size_tuple in constants.THUMBNAIL_SIZE_TUPLE_TO_SIZE_CODE:
    size_code = constants.THUMBNAIL_SIZE_TUPLE_TO_SIZE_CODE[size_tuple]
    filename = utils.thumbnail(input_filepath, uri, size_tuple)
    touch_thumbnail(uri, filename, size_code)

def get_reviews(uris=None):
  try:
    context = []
    with create_session() as s:
      reviews = _get_reviews(s, uris=uris)
      for review in reviews:
        new_review = {
          'body': review.body,
          'timestamp': review.created_at_utc
        }
        context.append(new_review)
    print(context)
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
        print(design.updated_at_utc)
        new_design = {
          'uri': design.uri,
          'updated_at_utc': utils.epoch_to_datetime_string(design.updated_at_utc),
          'reviews': []
        }
        for review in design.reviews:
          new_design['reviews'].append({
            'body': review.body,
            'timestamp': utils.epoch_to_datetime_string(review.created_at_utc)
          })
        for thumbnail in design.thumbnails:
          if thumbnail.size_code == constants.SIZE_CODE_LARGE:
            new_design['thumbnail_uri'] = utils.build_thumbnail_filepath(
                thumbnail.review_object_uri, thumbnail.filename)
        context.append(new_design)
    print(context)
    return context
  except:
    raise
    return 'Failed'

def create_a_review(review_object_uri, body, email=None):
  try:
    with create_session() as s:
      r = _get_review_objects(s, [review_object_uri])
      assert r, 'Invalid review object uri'
      o = Review()
      o.review_object_uri = review_object_uri
      o.body = body
      # touch time
      o.updated_at_utc = time.time()
      s.add(o)
    return 'adding a new review succeeded'
  except:
    raise
    return 'Failed'

def touch_thumbnail(review_object_uri, filename, size_code):
  try:
    with create_session() as s:
      o = _get_thumbnail(s, [review_object_uri], [filename])
      if not o:
        o = Thumbnail()
      else:
        o = o[0]
        print('updating existing thumbnail')
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

def touch_review_object(uri, filename):
  try:
    with create_session() as s:
      o = _get_review_objects(s, [uri])
      if not o:
        o = ReviewObject()
      else:
        o = o[0]
        print('updating existing design')
      o.uri = uri
      o.filename = filename
      # touch time
      o.updated_at_utc = time.time()
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
  if uris:
    q = q.filter(ReviewObject.uri.in_(uris))
  return q.all()

def _get_reviews(session, uris):
  """Return a list of ReviewObject"""
  q = session.query(Review)
  if uris:
    q = q.filter(Review.review_object_uri.in_(uris))
  return q.all()

def get_review_objects(uris=None):
  """Return a list of ReviewObject object in strings"""
  with create_session() as s:
    return _get_review_objects(s, uris)

def delete_review_objects(uris):
  return 'fake deleted'
  try:
    with create_session() as s:
      for o in _get_review_objects(s, uris):
        s.delete(o)
  except:
    raise
    return 'Delete failed'
  return 'Deleted'
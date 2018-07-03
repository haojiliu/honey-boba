# Haoji Liu
import os, sys, uuid, json, logging

import requests, jsonify

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask import Flask, flash, jsonify, request, redirect, url_for
from flask import send_from_directory, render_template, safe_join

import logic as l
import utils
import constants
import emailer

from flask_cors import CORS

import zmq

try:
  context = zmq.Context()
  connect_string = 'tcp://{}:{}'.format(
      constants.zmq_event_host, constants.event_pub_port)
  socket = context.socket(zmq.PUB)
  socket.connect(connect_string)
  logging.warning('connected to %s' % connect_string)
except:
  logging.warning('not able to connect to the socket')

# Instantiate the Node
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['MAX_CONTENT_LENGTH'] = constants.MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = constants.UPLOAD_FOLDER
app.secret_key = b'(D*@SK+2309_jvoe)\n\xec]/'

def recaptcha():
  """
  Returns: bool, True if usr is not a robot per Google's analysis
  """
  user_ip = request.environ['REMOTE_ADDR']
  user_browser = request.headers['User-Agent']
  g_recaptcha_response = request.form.get('g-recaptcha-response')
  g_recaptcha_post_data = {
    'secret': constants.CONST_GOOGLE_RECAPTCHA_SECRET_KEY,
    'response': g_recaptcha_response}
  r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=g_recaptcha_post_data)
  is_g_recaptcha_verified = r.json().get('success', False)
  return is_g_recaptcha_verified

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return render_template("index.html")

@app.route('/api/designs', methods=['GET'])
def api_designs():
  """Returns: list of dicts"""
  designs = l.get_all_active_designs()
  return jsonify(designs)

@app.route('/api/design/<uri>', methods=['GET'])
def api_design(uri):
  """Returns: dict"""
  designs = l.get_all_active_designs(uris=[uri])
  assert len(designs) <= 1
  design = designs[0] if designs else {}
  return jsonify(design)

@app.route('/api/thumbnail/<uri>', methods=['GET'])
def api_thumbnail(uri):
  """api endpoint to serve all thumbnails"""
  filename = '1024_by_1024.jpg'
  filepath = uri + '/' + filename
  return send_from_directory(constants.THUMBNAIL_FULL_DIR, filepath)

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS

@app.route('/api/review/<uri>', methods=['GET'])
def api_review(uri):
  reviews = l.get_reviews(uris=[uri])
  return jsonify(reviews)

@app.route('/api/review', methods=['POST'])
def api_review_post():
  if request.method == 'POST':
    error_msg = ''
    review_text = utils.sanitize_user_input(request.form.get('reviewText'))
    uri = utils.sanitize_user_input(request.form.get('uri'))
    error_msg = l.create_a_review(uri, review_text)
    return jsonify({
      'status': 0 if not error_msg else 1,
      'error_msg': error_msg
    })

def file_upload_sanity_check(uri):
  """
  Make sure:
  1. file is not empty
  2. file size is below threshold
  3. file has the correct formats
  4. if updating existing design, make sure the uri exists
  """
  # check if the post request has the file part
  if 'file' not in request.files:
    return 'No selected file'
  file = request.files['file']
  # if user does not select file, browser also
  # submit a empty part without filename
  if file.filename == '':
    return 'No selected file'
  if not allowed_file(file.filename):
    return 'Only accepting %s file formats' % ' or '.join(constants.ALLOWED_EXTENSIONS)
  if uri:
    if not l.get_review_objects([uri]):
      return 'Design not found'
  return ''

def _handle_file_upload(file, uri=None):
  filename = file.filename
  uri = uri or str(uuid.uuid4())
  fdir = safe_join(app.config['UPLOAD_FOLDER'], uri)
  if not os.path.exists(fdir):
    os.makedirs(fdir)
  fpath = safe_join(fdir, filename)
  file.save(fpath)

  if constants.MODE == 'PROD':
    pass
    # TODO: upload to s3

  l.thumbnail(fpath, uri)
  return {'uri': uri, 'filename': filename}

def _touch_file(uri, email, name, desc):
  error_msg = file_upload_sanity_check(uri)
  if error_msg:
    return error_msg, None
  # first save the file and thumbnail it
  file_info_dict = _handle_file_upload(request.files['file'], uri)
  uri = file_info_dict['uri']
  # lastly, create a database ORM for it
  filename = file_info_dict['filename']
  l.touch_review_object(uri, filename, email, name, desc)
  return error_msg, uri

@app.route('/api/update', methods=['POST'])
def api_update():
  """Handles design info update,
  """
  try:
    uri = utils.sanitize_user_input(request.form.get('uri'))
    name = utils.sanitize_user_input(request.form.get('name'))
    desc = utils.sanitize_user_input(request.form.get('desc'))
    logging.warning('uri is %s desc is %s and name is %s' % (uri, desc, name))
    l.touch_review_object(uri, None, None, name, desc)
    return jsonify({
      'status': 0,
      'errors': ''
    })
  except:
    return jsonify({'status': 1, 'errors': 'Something wrong when updating design info'})

# TODO: use this https://pythonhosted.org/Flask-Uploads/
@app.route('/api/upload', methods=['POST'])
def api_upload():
  """Handles design submissions,
  if uri is specified, update the existing design,
  otherwise create a new entry for the review object and
  return the generated uri
  """
  try:
    uri = utils.sanitize_user_input(request.form.get('uri'))
    email = utils.sanitize_user_input(request.form.get('email'))
    name = utils.sanitize_user_input(request.form.get('name'))
    desc = utils.sanitize_user_input(request.form.get('desc'))
    if not uri and not recaptcha():
      error_msg = 'Are you a robot?'
    else:
      error_msg, uri = _touch_file(uri, email, name, desc)
      assert not (error_msg and uri), 'Either error message or uri, not both'
      # if file successfully uploaded, send an email
      if not error_msg:
        logging.warning('no error message')
        if email:
          logging.warning('going to send an email')
          payload = {
            'type': 0,
            'receivers': [email],
            'uri': uri,
            'name': name
          }
          socket.send_json(payload)
        else:
          # either updating existing design, or uploader didn't provide an email
          pass
    return jsonify({
      'status': 0 if not error_msg else 1,
      'errors': error_msg,
      'uri': uri
    })
  except RequestEntityTooLarge:
    return jsonify({'status': 1, 'errors': 'File too large, please downsize and try again.'})

@app.route('/api/auth/email', methods=['POST'])
def api_auth_email():
  """
  This is the endpoint to delete the uploaded design
  """
  email = utils.sanitize_user_input(request.form.get('email'))
  uid = utils.sanitize_user_input(request.form.get('uid'))
  true_email = l.get_email_by_uid(uid=uid)
  logging.warning('true email: %s email: %s, uid: %s' % (true_email, email, uid))
  return jsonify({
    'status': 0 if email == true_email else 1,
    'errors': 'Failed, please try again.'
  })

@app.route('/api/delete', methods=['POST'])
def api_delete():
  """
  This is the endpoint to delete the uploaded design
  """
  uri = utils.sanitize_user_input(request.form.get('uri'))
  error_msg = l.delete_review_objects(uris=[uri])
  return jsonify({
    'status': 0 if not error_msg else 1,
    'error_msg': error_msg
  })

@app.route('/api/report', methods=['POST'])
def api_report():
  """
  This is the endpoint to report an inappropriate design
  """
  uri = utils.sanitize_user_input(request.form.get('uri'))
  error_msg = l.report_review_objects(uris=[uri])
  return jsonify({
    'status': 0 if not error_msg else 1,
    'error_msg': error_msg
  })

@app.route('/api/dev', methods=['POST'])
def api_dev():
  """
  This is the endpoint to leave a comment or report a bug
  """
  body = utils.sanitize_user_input(request.form.get('body'))
  error_msg = l.create_a_comment(body=body)
  logging.warning('comments: %s' % body)
  return jsonify({
    'status': 0 if not error_msg else 1,
    'error_msg': error_msg
  })

@app.route('/dev/db/haoji', methods=['GET'])
def dev_db_viewer():
  """
  For dev debug only
  """
  context = {
    'tables': [
      {
        'comment': [],
        'user': [],
        'review': [],
        'thumbnail': []
      }
    ]
  }
  return render_template("index.html", context=context)

if __name__ == '__main__':
  IS_DEV = constants.MODE == 'DEV'
  if IS_DEV:
    p = 5000
  elif len(sys.argv) == 2:
    p = sys.argv[1]
  else:
    p = 5000
  print('is in dev mode? %s' % IS_DEV)
  app.run(host='0.0.0.0', port=int(p), debug=IS_DEV)

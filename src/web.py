# Haoji Liu
import os, sys, uuid, json

import requests, jsonify

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask import Flask, flash, jsonify, request, redirect, url_for
from flask import send_from_directory, render_template, safe_join

import logic as l
import utils
import constants

from flask_cors import CORS

# Instantiate the Node
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['MAX_CONTENT_LENGTH'] = constants.MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = constants.UPLOAD_FOLDER
app.secret_key = b'(D*@SK+2309_jvoe)\n\xec]/'

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
  designs = l.get_all_active_designs(uris=[uri,])
  assert len(designs) == 1
  return jsonify(designs[0])

@app.route('/api/thumbnail/<uri>', methods=['GET'])
def api_thumbnail(uri):
  """api endpoint to serve all thumbnails"""
  filename = '1024_by_1024.jpg'
  filepath = uri + '/' + filename
  return send_from_directory(constants.THUMBNAIL_FULL_DIR, filepath)

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS

@app.route('/api/review', methods=['GET','POST'])
def api_review():
  if request.method == 'POST':
    review_text = request.form.get('reviewText')
    uri = request.form.get('uri')
    sanitized_review_text = utils.sanitize_user_input(review_text)
    if len(sanitized_review_text) < constants.MIN_LEN_REVIEW:
      return 'Your review is too short! Sure you can suggest more!'
    else:
      l.create_a_review(uri, sanitized_review_text)
      return 'Your review "%s" was posted' % sanitized_review_text

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
  if uri:
    print('updating existing design...')
  else:
    print('creating new design...')

  filename = file.filename
  uri = uri or str(uuid.uuid4())
  fdir = safe_join(app.config['UPLOAD_FOLDER'], uri)
  if not os.path.exists(fdir):
    os.makedirs(fdir)
  fpath = safe_join(fdir, filename)
  file.save(fpath)
  l.thumbnail(fpath, uri)
  return {'uri': uri, 'filename': filename}

def _touch_file(uri):
  error_msg = file_upload_sanity_check(uri)
  if error_msg:
    return error_msg, None
  file_info_dict = _handle_file_upload(request.files['file'], uri)
  uri = file_info_dict['uri']
  # create a database ORM for it
  filename = file_info_dict['filename']
  l.touch_review_object(uri, filename)
  return error_msg, uri

# TODO: use this https://pythonhosted.org/Flask-Uploads/
@app.route('/api/upload', methods=['POST'])
def api_upload():
  """Handles design submissions,
  if uri is specified, update the existing design,
  otherwise create a new entry for the review object and
  return the generated uri
  """
  try:
    uri = request.form.get('uri')
    print(uri)
    error_msg, uri = _touch_file(uri)
    assert not (error_msg and uri), 'Either error message or uri, not both'
    return jsonify({
      'status': 0 if not error_msg else 1,
      'errors': error_msg,
      'uri': uri
    })
  except RequestEntityTooLarge:
    return jsonify({'errors': 'from flask: File too large, downsize and try again.'})

@app.route('/api/delete', methods=['POST'])
def api_delete():
  """
  This is the endpoint to delete the uploaded design
  """
  uri = request.form.get('uri')
  print(uri)
  error_msg = l.delete_review_objects(uris=[uri])
  return jsonify({
    'status': 0,
    'error_msg': error_msg
  })

if __name__ == '__main__':
  if len(sys.argv) == 2:
    p = sys.argv[1]
  else:
    p = 5000
  app.run(host='0.0.0.0', port=int(p), debug=True)
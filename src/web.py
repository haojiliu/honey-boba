# Haoji Liu
import os, sys, uuid, json

import requests

from werkzeug.utils import secure_filename

from flask import Flask, flash, jsonify, request, redirect, url_for
from flask import send_from_directory, render_template, safe_join

import logic as l
import utils
import constants

# Instantiate the Node
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_FILE_SIZE

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = constants.UPLOAD_FOLDER
app.secret_key = b'(D*@SK+2309_jvoe)\n\xec]/'

@app.route('/', methods=['GET'])
def hello_world():
  return 'hello world'

@app.route('/designs', methods=['GET'])
def designs():
  """Designs displayed in a masonry style"""
  designs = l.get_designs()
  context = {
    'is_review_enabled': True,
    'is_reviews_collapsed': True,
    'designs': designs
  }
  return render_template('all_designs.html', context=context)

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS

def file_upload_sanity_check():
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

def _touch_file(uri=None):
  error_msg = file_upload_sanity_check()
  if error_msg:
    return error_msg, None
  file_info_dict = _handle_file_upload(request.files['file'], uri)
  uri = file_info_dict['uri']
  # create a database ORM for it
  filename = file_info_dict['filename']
  msg = l.touch_review_object(uri, filename)
  print('the msg is %s' % msg)
  return error_msg, uri

# TODO: use this https://pythonhosted.org/Flask-Uploads/
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    error_msg, uri = _touch_file()
    if error_msg:
      flash(error_msg)
      return redirect(request.url)
    flash('Congratulations! Your design has been posted')
    return redirect(url_for('uploaded_file', uri=uri))
  else:
    return render_template('upload.html')

@app.route('/uploads/delete/<uri>', methods=['GET'])
def uploaded_file_delete(uri):
  """
  This is the endpoint to view or delete the uploaded design
  """
  return 'your design has been deleted.'

@app.route('/uploads/<uri>', methods=['GET', 'POST'])
def uploaded_file(uri):
  """
  This is the endpoint to view or delete the uploaded design
  """
  if request.method == 'POST':
    uri = _touch_file(uri=uri)
    error_msg, uri = _touch_file()
    if error_msg:
      flash(error_msg)
    else:
      flash('Your design has been successfully updated')
    # TODO: need to clear browser cache here to see the updated thumbnail
    return redirect(request.url)
  elif request.method == 'DELETE':
    return 'your design has been deleted.'
  else:
    designs = l.get_designs(uris=[uri])
    assert len(designs) == 1, '%s designs found for uri %s' % (len(d), uri)
    context = {
      'is_review_enabled': False,
      'uri': uri,
      'designs': designs,
      'is_reviews_collapsed': False
    }
    return render_template('uploaded_design.html', context=context)

@app.route('/post/review/<uri>', methods=['POST'])
def post_review(uri):
  review_text = request.form.get('reviewText')
  sanitized_review_text = utils.sanitize_user_input(review_text)
  if len(sanitized_review_text) < constants.MIN_LEN_REVIEW:
    flash('Your review is too short! Sure you can suggest more!')
  else:
    l.create_a_review(uri, sanitized_review_text)
    flash('Your review "%s" was posted' % sanitized_review_text)
  return redirect(url_for('designs'))

if __name__ == '__main__':
  if len(sys.argv) == 2:
    p = sys.argv[1]
  else:
    p = 5000
  app.run(host='0.0.0.0', port=int(p), debug=True)

# import yaml file as modules
########################
# TODO: move this part out to a bootstrap file
import yaml
import os

MODE = os.environ.get('ANONBETA_MODE')

if MODE == 'DEV':
  config_yaml_path = '../config/dev.yaml'
elif MODE == 'PROD':
  config_yaml_path = '/srv/config/prod.yaml'
else:
  config_yaml_path = '../config/dev.yaml'

GLOBAL_CONFIG = {}
with open(config_yaml_path, 'r') as stream:
  try:
    GLOBAL_CONFIG = yaml.load(stream)
  except yaml.YAMLError as exc:
    print(exc)

print(GLOBAL_CONFIG)

DB_PATH = GLOBAL_CONFIG.get('DB_PATH', 'app.db')
# This is to make local dev work without a docker
if not MODE:
  BASE_DIR = '/Users/haojiliu/src/honey-boba/'
else:
  BASE_DIR = GLOBAL_CONFIG['BASE_DIR']

S3_BUCKET = GLOBAL_CONFIG['S3_BUCKET']
AWS_ACCESS_KEY = GLOBAL_CONFIG['AWS_ACCESS_KEY']
AWS_SECRET_KEY = GLOBAL_CONFIG['AWS_SECRET_KEY']
S3_THUMBNAIL_FOLDER = GLOBAL_CONFIG['S3_THUMBNAIL_FOLDER']

#######################
UPLOAD_FOLDER = BASE_DIR + 'uploaded_files'

THUMBNAIL_FOLDER = '/static/thumbnail/designs'
THUMBNAIL_FULL_DIR = BASE_DIR + 'src/static/thumbnail/designs'


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

FORMAT_JPEG = 'jpg'

# only one size thumbnail 1024 x 1024 only
SIZE_CODE_LARGE = 0
# SIZE_CODE_MEDIUM = 1

THUMBNAIL_SIZE_TUPLE_TO_SIZE_CODE = {
  (1024, 1024): SIZE_CODE_LARGE
}
THUMBNAIL_FILENAME = '1024_by_1024.jpg'

MAX_FILE_SIZE = 16 * 1024 * 1024 # 16MB

MIN_LEN_REVIEW = 4

CONST_FLAGS_ACTIVE = 0
CONST_FLAGS_INACTIVE = 1 << 1
CONST_FLAGS_REPORTED = 1 << 2

CONST_SKU_PREFIX_DEFAULT = 'ABC'

CONST_GOOGLE_RECAPTCHA_SITE_KEY = '6LcwUV8UAAAAAJo2f_MbbAbJTdr8xFpw1T4Naxpy'
CONST_GOOGLE_RECAPTCHA_SECRET_KEY = '6LcwUV8UAAAAAKIgLoONyXdp9G6rCVzQRMZgxVfE'

CONST_EMAILER_SENDER = 'notifications@anonbeta.com'
CONST_EMAILER_PASSWORD = '1949101_Saruman'

CONST_DESIGN_URL = 'http://www.anonbeta.com/uploaded/%s'
CONST_EMAIL_DIGEST_INTERVAL_IN_SECONDS = 3600 * 24 # Send digest email per hour

zmq_event_host = '0.0.0.0'
event_pub_port = 8081
event_sub_port = 8082

JOB_TYPE_S3_UPLOAD_ORIGINAL = 0
JOB_TYPE_S3_UPLOAD_THUMBNAIL = 1
JOB_TYPE_EMAIL_UPLOAD_SUCCESS = 2

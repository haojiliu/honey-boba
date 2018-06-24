BASE_DIR = '/Users/haojiliu/src/honey-boba/'
UPLOAD_FOLDER = BASE_DIR + 'uploaded_files'

THUMBNAIL_FOLDER = '/static/thumbnail/designs'
THUMBNAIL_FULL_DIR = BASE_DIR + 'src/static/thumbnail/designs'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

FORMAT_JPEG = 'jpg'

SIZE_CODE_LARGE = 0
SIZE_CODE_MEDIUM = 1

THUMBNAIL_SIZE_TUPLE_TO_SIZE_CODE = {
  (1024, 1024): SIZE_CODE_LARGE,
  (512, 512): SIZE_CODE_MEDIUM
}

MAX_FILE_SIZE = 16 * 1024 * 1024 # 16MB

MIN_LEN_REVIEW = 4

CONST_FLAGS_ACTIVE = 0
CONST_FLAGS_INACTIVE = 1 << 1
CONST_FLAGS_REPORTED = 1 << 2

CONST_SKU_PREFIX_DEFAULT = 'ABC'

CONST_GOOGLE_RECAPTCHA_SITE_KEY = '6LcwUV8UAAAAAJo2f_MbbAbJTdr8xFpw1T4Naxpy'
CONST_GOOGLE_RECAPTCHA_SECRET_KEY = '6LcwUV8UAAAAAKIgLoONyXdp9G6rCVzQRMZgxVfE'

CONST_EMAILER_SENDER = 'divid86391@gmail.com'
CONST_EMAILER_PASSWORD = '1949101Saruman'

CONST_DESIGN_URL = 'http://www.honey-boba.com/uploaded/%s'
CONST_EMAIL_DIGEST_INTERVAL_IN_SECONDS = 3600

zmq_event_host = '0.0.0.0'
event_pub_port = 8081
event_sub_port = 8082

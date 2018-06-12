# Haoji Liu
import os, sys, datetime, time
from PIL import Image
import constants

def epoch_to_datetime_string(epoch_time):
  return datetime.datetime.fromtimestamp(int(float(epoch_time))).strftime("%Y-%m-%d %H:%M:%S")

def sanitize_user_input(user_input):
  return user_input

def color_conversion(im):
  fmt = im.format
  if fmt == 'PNG':
    im = im.convert('RGB')
  return im

def build_thumbnail_filepath(uri, filename):
  # fdir = os.path.join(constants.THUMBNAIL_FOLDER, uri)
  # return os.path.join(fdir, filename)
  return '/api/thumbnail/' + uri

def thumbnail(input_filepath, uri, size_tuple, fmt=constants.FORMAT_JPEG):
  width, height = size_tuple
  output_filename = str(width) + '_by_' + str(height) + '.' + fmt
  output_dir = os.path.join(constants.THUMBNAIL_FULL_DIR, uri)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  output_filepath = os.path.join(output_dir, output_filename)
  print('thumbnailing %s to output %s' % (size_tuple, output_filepath))
  try:
    im = Image.open(input_filepath)
    print(im.format)
    im = color_conversion(im)
    print('image opened!')
    im.thumbnail(size_tuple)
    print('thumbnail finished!')
    print(output_filepath)
    im.save(output_filepath, "JPEG")
    print('saved to jpeg!!')
    return output_filename
  except IOError:
    raise
    print("cannot create thumbnail for %s" % input_filepath)

def generate_random_string(size):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def sku_generator(prefix=None):
  generated_parts = [generate_random_string(3), generate_random_string(3)]
  if prefix:
    return '-'.join([prefix, '-'.join(generated_parts)])
  else:
    return '-'.join([constants.CONST_SKU_PREFIX_DEFAULT, '-'.join(generated_parts)])
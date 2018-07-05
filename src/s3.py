# Haoji Liu
# S3 module
import boto3

import constants

def get_s3_client():
  client = boto3.client(
    's3',
    aws_access_key_id=constants.AWS_ACCESS_KEY,
    aws_secret_access_key=constants.AWS_SECRET_KEY
  )
  return client

def upload_original(uri, fname, fpath):
  s3 = get_s3_client()
  bucket_name = constants.S3_BUCKET
  key = 'uploaded_files/%s/%s' % (uri, fname)
  s3.upload_file(fpath, bucket_name, key)

def upload_thumbnail(uri, fname, fpath):
  s3 = get_s3_client()
  bucket_name = constants.S3_BUCKET
  key = 'thumbnails/%s/%s' % (uri, fname)
  s3.upload_file(fpath, bucket_name, key)

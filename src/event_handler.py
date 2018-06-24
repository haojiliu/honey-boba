# Haoji Liu
import sys, os, json
import time
import datetime
import threading
import logging

import zmq

import emailer
import constants

def write(sock):
  while True:
    logging.warning('waiting for write requests...')
    data = sock.recv_json()
    print('received an event request, data is %s' % data)
    receivers = data.get('receivers')
    uri = data.get('uri')
    name = data.get('name')
    subject = 'Woohoo!'
    body = emailer.new_upload_template.render(uri=uri, name=name)
    if not emailer.send_html(receivers, subject, body):
      # TODO: put the failed ones into a log
      pass

    logging.warning('Write succeeded...')

def main():
  write_sock = None
  try:
    context = zmq.Context()
    connect_string = 'tcp://{}:{}'.format(
        constants.zmq_event_host, constants.event_sub_port)
    write_sock = context.socket(zmq.SUB)
    write_sock.connect(connect_string)
    write_sock.setsockopt(zmq.SUBSCRIBE, b"")
    logging.warning('event handler addr is %s' % connect_string)

    write_thread = threading.Thread(target=write, args=(write_sock,))
    write_thread.daemon = True
    write_thread.start()
    write_thread.join()
  except Exception as e:
    logging.warning(e)
  finally:
    if write_sock:
      write_sock.close()

if __name__ == '__main__':
  main()

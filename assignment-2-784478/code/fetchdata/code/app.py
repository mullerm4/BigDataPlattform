from apscheduler.schedulers.background import BlockingScheduler
import os
import threading
from warnings import warn
import shutil
import yaml
from yaml import BaseLoader
import logging
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

import time
import logging



class CustomerHandler(LoggingEventHandler):
    def on_created(self, event):
        super().on_created(event)
        user = event.src_path.split('/')[1]
        threading.Thread(target=apply_profile_move, args=(event.src_path, user)).start()


def apply_profile_move(file, user):
    """
    Check if file fits constraints defined in profile and move the files accordingly
    :param file:
    :param user:
    :return:
    """
    if os.path.isdir(file):
        warn('Directories are not supported')
        return
    prefix = file.split('.')[-1]
    if prefix not in ingest_conf['suportedformats']:
        warn('Unsupported file format {}'.format(prefix))
        return
    if os.path.getsize(file) > int(ingest_conf['max-size']):
        warn('File is too big')
        return
    fname = file.split('/')[-1]
    new_path = os.path.join(STAGE, user + '.' + fname)
    logging.info('{}-->{}'.format(file, new_path))
    shutil.move(file, new_path)



with open("/config/profile.yml", 'r') as f:
    ingest_conf = yaml.load(f, Loader=BaseLoader)

STAGE = '/stage/'
DATA = '/data/'


if __name__ == "__main__":
    event_handler = CustomerHandler()
    observer = Observer()
    observer.schedule(event_handler, DATA, recursive=True)
    observer.start()
    try:
        while True:

            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

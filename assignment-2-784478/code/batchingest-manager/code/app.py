from apscheduler.schedulers.background import BlockingScheduler
from clientbatchingestapp import json_read_ingest, yaml_read_ingest
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, LoggingEventHandler
import threading

class LoggingHandlerCustomer(LoggingEventHandler):
    def on_created(self, event):
        super().on_created(event)
        if event.src_path.endswith('yaml') or event.src_path.endswith('yml'):
            print('Ingest file for yaml customer')
            threading.Thread(target=yaml_read_ingest, args=(event.src_path,)).start()
        elif event.src_path.endswith('json'):
            print('Ingest file for json customer')
            threading.Thread(target=json_read_ingest, args=(event.src_path,)).start()
        elif event.src_path.endswith('txt'):
            print("Ingest file for TXT customer")
        else:
            raise TypeError


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = '/stage'
    event_handler = LoggingHandlerCustomer()
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

import json
import time
import  argparse
import os
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import LoggingEventHandler

class MyHandler(PatternMatchingEventHandler):

    files_sizes = None
    number_of_files = None
    files_to_fetch = []


    def process(self, event):

        # the file will be processed there
        #if event.src_path.endswith(tuple([item.replace("*", "") for item in self.patterns])):
        _, file_extension = os.path.splitext(event.src_path)
        file_size = os.path.getsize(event.src_path) / 1024
        files_to_fetch_c = len(self.files_to_fetch)

        if file_size <= self.files_sizes and files_to_fetch_c < self.number_of_files:
            self.files_to_fetch.append(event.src_path)
            logging.info("%s %s file size: %s, files to fetch: %s, files allowed to upload: %s" %(event.src_path, event.event_type, file_size, files_to_fetch_c, self.number_of_files - files_to_fetch_c))

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
    def on_deleted(self, event):
        self.process(event)
class Fetching():
    def __init__(self, path):

        config = json.loads(open('profile_1.json').read())

        self.constraints = config["suportedformats"]
        MyHandler.number_of_files = 3  # config['numberoffiles']#, config["sizelimit"])
        MyHandler.files_sizes = 1024
    def LoadFetcher(self, dir):
        # event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(MyHandler(patterns=self.constraints), dir)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def getFiles(self, dir):
        return MyHandler.files_to_fetch


parser = argparse.ArgumentParser(description='mysimbdp-fetchdata: Fetches data from directory based on constraint profile.')
parser.add_argument('-user', metavar='N', type=str,
                    help='username', default='new_user_42')
parser.add_argument('-p', metavar='N', type=str,
                    help='password of the user', default='new_user_42')
parser.add_argument('-lp', metavar='N', type=str,
                    help='specify log directory for diffrent test cases. For example when 10 instances are running on the same time '
                         'provide 10 as argumemt.',
                    default=None)
parser.add_argument('-ci', metavar='N', type=str,
                    help='specify the client input directory.',
                    default=None)
args = parser.parse_args()

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
if args.ci is None or not os.path.exists(args.ci):
    exit(0)








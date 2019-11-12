import os
import pandas as pd
import json
import yaml
from yaml import BaseLoader
import string
from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
from paho.mqtt.client import Client
import random
from datetime import datetime

def generate_files(no_files=-1):
    """
    Generate files based on the selected gen type
    :param no_files:
    :return:
    """
    if no_files == -1:
        no_files = random.randint(10, 150)
    gen_type = random.choice(['json', 'yaml'])
    samples = pd.read_csv(DB_PATH).sample(no_files)
    now = datetime.now()
    if gen_type == 'yaml':
        print('Generate yaml ...')
        file = '{}.yml'.format(now.strftime("%m_%d_%Y_%H:%M:%S"))
        file = os.path.join(PATH, file)
        with open(file, 'w') as f:
            yaml.dump(samples.to_dict(), f)
        samples = pd.read_csv(DB_PATH).sample(no_files)
    elif gen_type == 'json':
        print('Generate json ...')
        file = '{}.json'.format(now.strftime("%m_%d_%Y_%H:%M:%S"))
        file = os.path.join(PATH, file)
        with open(file, 'w') as f:
            json.dump(samples.to_json(), f)
    else:
        print("Other customer types can be defined")

def random_string(stringLength=10):
    """
    Create random string
    :param stringLength:
    :return:
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



def publish_message_mqtt():
    """
    Notify mqtt server, that new component was generated.
    :return:
    """
    cb.loop_start()
    with open('/config/ingestion.yml', 'r') as f:
        values = yaml.load(f, Loader=BaseLoader)
    values = values['whatsapp']['fields']
    samples = pd.read_csv(DB_PATH).sample(1).to_dict()
    time = datetime.now().strftime('%m_%d_%Y_%H:%M:%S')
    for val in values:
        k = list(val.keys())[0]
        if k == 'created_utc':
            continue
        [[line, v]] = samples[k].items()
        topic = 'clients/' + USER + '/' + str(k)
        print('Sending mqtt with topic {}'.format(topic))
        msg_info = cb.publish(topic=topic, payload=str(v))
    cb.loop_stop()

# prepare
message_type = os.getenv('MESSAGE_TYPE', 'reddit')
DB_PATH = os.getenv('DB_PATH', '/reddit-comments/database.csv')
DATA = '/data'
USER = os.getenv('HOSTNAME', random_string())
PATH = ""

cb = Client('messenger' + USER)
cb.enable_logger()
gen_type = ''


if __name__ == "__main__":
    PATH = os.path.join(DATA, USER)
    try:
        os.mkdir(PATH)
    except FileExistsError:
        print('User already exists')
    cb.connect(host='mqtt', port=1883)
    scheduler = BlockingScheduler()
    job_mqtt = scheduler.add_job(publish_message_mqtt, 'interval', seconds=10)
    job = scheduler.add_job(generate_files, 'interval', seconds=15)
    scheduler.start()

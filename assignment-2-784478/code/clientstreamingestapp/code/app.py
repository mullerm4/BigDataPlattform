import paho.mqtt.client as mqtt
from pymongo import MongoClient, monitoring
import logging
import time
import os
import sys
import _pickle as cPickle
from logger import  *
from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
logger = logging.Logger(name='clientstreamingestapp', level=logging.DEBUG)
log_path = '/logs'
performance = {"success": 0, "failures":0, "rate":0, "overall":0, "avg_size": 0, "avg_ingest_time": 0, "number_of_messages": 0}


def on_disconnect(client, userdata, rc):
    """
    Occurs, when the connection to the server vanished
    :param client:
    :param userdata:
    :param rc:
    :return:
    """
    if rc != 0:
        print("Error: Mqtt server disconnection.")


def on_message(client, userdata, msg):
    """
    On message event, to post message to Mongo DB Server
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    logging.info(msg.topic + " " + str(msg.payload))
    receiveTime = str(int(time.time()))
    # Set up client for MongoDB
    logging.info('Connect to Mongo')
    mongoClient = MongoClient(host='database', port=27017)
    mng_db = mongoClient.whatsapp
    topic = str(msg.topic).split('/')
    user = topic[1]
    message = str(msg.payload)
    collection = mng_db[user]

    post = {str(receiveTime): {topic[-1]: message}}

    performance["avg_size"] =  sys.getsizeof(cPickle.dumps(post))
    logging.info('post to mongo: {}'.format(post))

    performance["success"] += 1

    try:
        start_time = time.time()
        collection.insert_one(post)
        duration = time.time() - start_time
        performance["avg_ingest_time"] = (duration+  performance["avg_ingest_time"]) / 2
        performance["number_of_messages"] += 1
        performance["rate"] =  performance["avg_size"] / duration
    except:
        performance["failures"] += 1
    finally:
        performance["overall"] += 1
    create_status_logging()


def on_connect(client, userdata, flags, rc):
    """
    Event occurs when client is connected, then the client subscribes
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    print("Connected with with mqtt server: " + str(rc))
    client.subscribe("clients/#")

def create_report_logging():
    """
    Create performance logging to focus on main results
    :param filename:
    :return:

    """
    print("Creating report")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=os.path.join(log_path, "client_stream_report.log"),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.info("Performance of client-streaming: Average_size: %s bytes, average ingest time: %s seconds, ingestion_rate: %s byte/sec" "number _of_messages: %s"
                 %(performance["avg_size"], performance["avg_ingest_time"], performance["rate"], performance["number_of_messages"]))
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

def create_status_logging():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=os.path.join(log_path, "clientstreamingapp.log"),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.info("messages proccessed, %s success: %s, failures: %s, ingestion_rate: %s byte/sec " %
                (performance["overall"],performance["success"], performance["failures"], performance["rate"]))
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


if __name__ == "__main__":
    #  Create client for  Mosquitto broker

    client = mqtt.Client()
    client.enable_logger()

    scheduler = BackgroundScheduler()
    job = scheduler.add_job(create_report_logging, 'interval', seconds=15)
    scheduler.start()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    conn = client.connect("mqtt", 1883)
    client.loop_forever()


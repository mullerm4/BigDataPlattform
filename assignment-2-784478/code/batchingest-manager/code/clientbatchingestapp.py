import json
import yaml
from yaml import BaseLoader
import os
from logger import *
from pymongo import MongoClient, monitoring
import time
import logging
from warnings import warn

log_path = '/logs'
performance = {}




def json_read_ingest(file):
    """
    Ingester for the json customer
    :param file:
    :return:
    """
    user = 'json'
    create_logging(user+".log")
    try:
        check_profile(file)
        with open(file, 'r') as f:
            data = json.loads(json.load(f))
    except:
        logging.info("Failure for customer service %s " % file)
        return
    write_data(data, 'reddit', file, user)


def yaml_read_ingest(file):
    """
    Ingester for the yaml customer
    :param file:
    :return:
    """
    user = 'yaml'
    create_logging(user+ ".log")
    try:
        check_profile(file)
        with open(file, 'r') as f:
            data = yaml.load(f, Loader=BaseLoader)
    except:
        logging.info("Failure for customer service %s " % file)
        return
    write_data(data, 'twitter', file, user)



def write_data(data, f_type, file, user):
    """
    Ingestion data to the Mongo DB
    :param data:
    :param f_type:
    :param file:
    :param user:
    :return:
    """
    mng_client = MongoClient(host='database', port=27017)
    mng_db = mng_client[f_type]
    collection = mng_db[user]
    ## for KB
    file_size = os.path.getsize(file) /1024
    ## for MB
    big_file_size = file_size / 1024

    ingestion_rate = 0
    big_ingestion_rate = 0


    try:
        data = check_data(data, type=f_type)
    except KeyError:
        logging.info("Failure for ingestion checks for file %s " % file)
        return
    try:
        start_time = time.time()
        logging.info("Ingesting file %s" % file)
        collection.insert_one({user: data})
        duration = time.time() - start_time

        ingestion_string = "Needed %s seconds ingestion time for %s of size %s KB\ MB %s" % (duration, file, file_size, big_file_size)

        big_ingestion_rate = big_file_size/(duration) # in MB
        ingestion_rate = file_size / duration ## in KB
        if user not in performance:
            user_perf = {"rate": ingestion_rate, "bigrate": big_ingestion_rate, "success": 1, "failures": 0}
            performance[user] = user_perf
        else:
            performance[user]["rate"] = (performance[user]["rate"] + ingestion_rate) / 2
            performance[user]["bigrate"] = (performance[user]["bigrate"] + big_ingestion_rate) / 2
            performance[user]["success"] += 1

        logging.info("Successful ingestion")
        logging.info("%sMB/s" % big_ingestion_rate )
        logging.info("%sKB/s" % ingestion_rate )
        logging.info(ingestion_string)
    except:
        logging.info("Failure in ingestion for file %s " % file)
        if user not in performance:
            user_perf = {"rate": 0, "bigrate": 0, "success": 0, "failures": 1}
            performance[user] = user_perf
        else:
            performance[user]["rate"] = (performance[user]["rate"]) / 2
            performance[user]["bigrate"] = (performance[user]["bigrate"] ) / 2
            performance[user]["failures"] += 1


    # Updataing performance aferr each ingestions
    create_performnance_logging(user+"_performance.log")
    logging.info("File ingestions: %s , succeeded: %s, failures: %s"
            %(performance[user]["success"]+ performance[user]["failures"] ,
                 performance[user]["success"], performance[user]["failures"]))

    logging.info("average rate in KB: %s" %(performance[user]["rate"]))
    logging.info("average rate in MB: %s" %(performance[user]["bigrate"]))
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


def check_profile(file):
    """
    Check the file, wether if it's fits the constraints in the profile.yaml file.
    :param file:
    :return:
    """
    with open("/config/profile.yml", 'r') as f:
        ingest_conf = yaml.load(f, Loader=BaseLoader)
    if os.path.isdir(file):
        raise RuntimeError
    prefix = file.split('.')[-1]
    if prefix not in ingest_conf['suportedformats']:
        raise TypeError
    if os.path.getsize(file) > int(ingest_conf['max-size']):
        raise RuntimeError

def check_data(data, type):
    """
    Check if structure of data fits the structure of the ingestion.yaml
    :param data:
    :param type:
    :return:
    """
    with open("/config/ingestion.yml", 'r') as f:
        ingest_conf = yaml.load(f, Loader=BaseLoader)
    ingest_conf = ingest_conf[type]
    fields = [list(f.keys())[0] for f in ingest_conf['fields']]
    new_data = {}
    for key in fields:
        if key in data:
            new_data[key] = data[key]
        else:
            logging.info('key "{}" not in the data'.format(key))
            raise KeyError
    return new_data


def create_performnance_logging(filename):
    """
    Create performance logging to focus on main results
    :param filename:
    :return:
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(filename=os.path.join(log_path, filename),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)



def create_logging(filename):
    """
    Logging for server stats, connection error and also performance
    :param filename:
    :return:
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=os.path.join(log_path, filename),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    monitoring.register(CommandLogger())
    monitoring.register(ServerLogger())
    monitoring.register(TopologyLogger())



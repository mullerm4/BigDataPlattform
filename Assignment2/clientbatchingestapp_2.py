#to read data from data sources(files/external databases) of the tenant/user and then store the data by calling APIs ofmysimbdp-coredms

from pymongo import MongoClient, monitoring
from datetime import datetime
import logging
import pandas as pd
import os
import json
import numpy as np
import argparse
import time



class MongoDBClient(object):
    @staticmethod
    def get_connection(user, password):
        return MongoClient("mongodb+srv://%s:%s@cluster0-ukbbs.gcp.mongodb.net/test?retryWrites=true&w=majority" %(user, password), event_listeners=[CommandLogger()])




class CSVInputHandler():
    @staticmethod
    def getdatafromCSV(file_name, samplesize=None):
        if samplesize == None:
            data = pd.read_csv(file_name)
        else:
            data = pd.read_csv(file_name).sample(samplesize)
        return data

    @staticmethod
    def getJsonfromDf(data):
        header = data.head()
        new_header = [str(head).replace('.', '_') for head in header]
        data.columns = new_header

        return json.loads(data.to_json(orient='records'))

    @staticmethod
    def getJsonfromCSV(filename, samplesize=None):

        data = CSVInputHandler.getdatafromCSV(filename, samplesize)
        return CSVInputHandler.getJsonfromDf(data)



class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        logging.info("Command {0.command_name} with request id "
                     "{0.request_id} started on server "
                     "{0.connection_id}".format(event))

    def succeeded(self, event):
        logging.info("Command {0.command_name} with request id "
                     "{0.request_id} on server {0.connection_id} "
                     "succeeded in {0.duration_micros} "
                     "microseconds".format(event))

    def failed(self, event):
        logging.info("Command {0.command_name} with request id "
                     "{0.request_id} on server {0.connection_id} "
                     "failed in {0.duration_micros} "
                     "microseconds".format(event))

class ServerLogger(monitoring.ServerListener):

    def opened(self, event):
        logging.info("Server {0.server_address} added to topology "
                     "{0.topology_id}".format(event))

    def description_changed(self, event):
        previous_server_type = event.previous_description.server_type
        new_server_type = event.new_description.server_type
        if new_server_type != previous_server_type:
            # server_type_name was added in PyMongo 3.4
            logging.info(
                "Server {0.server_address} changed type from "
                "{0.previous_description.server_type_name} to "
                "{0.new_description.server_type_name}".format(event))

    def closed(self, event):
        logging.warning("Server {0.server_address} removed from topology "
                        "{0.topology_id}".format(event))


class HeartbeatLogger(monitoring.ServerHeartbeatListener):

    def started(self, event):
        logging.info("Heartbeat sent to server "
                     "{0.connection_id}".format(event))

    def succeeded(self, event):
        # The reply.document attribute was added in PyMongo 3.4.
        logging.info("Heartbeat to server {0.connection_id} "
                     "succeeded with reply "
                     "{0.reply.document}".format(event))

    def failed(self, event):
        logging.warning("Heartbeat to server {0.connection_id} "
                        "failed with error {0.reply}".format(event))

class TopologyLogger(monitoring.TopologyListener):

    def opened(self, event):
        logging.info("Topology with id {0.topology_id} "
                     "opened".format(event))

    def description_changed(self, event):
        logging.info("Topology description updated for "
                     "topology id {0.topology_id}".format(event))
        previous_topology_type = event.previous_description.topology_type
        new_topology_type = event.new_description.topology_type
        if new_topology_type != previous_topology_type:
            # topology_type_name was added in PyMongo 3.4
            logging.info(
                "Topology {0.topology_id} changed type from "
                "{0.previous_description.topology_type_name} to "
                "{0.new_description.topology_type_name}".format(event))
        # The has_writable_server and has_readable_server methods
        # were added in PyMongo 3.4.
        if not event.new_description.has_writable_server():
            logging.warning("No writable servers available.")
        if not event.new_description.has_readable_server():
            logging.warning("No readable servers available.")

    def closed(self, event):
        logging.info("Topology with id {0.topology_id} "
                     "closed".format(event))



class Clientbatching ():
    @staticmethod
    def ingest(user, pw, log_path, filename):

        if log_path is None:
            log_path = os.curdir
        if not  os.path.exists(log_path):
            os.mkdir(log_path)


        logname = user + "_" + str(datetime.now().strftime("%H_%M_%S")) + ".log"
        logfilepath = os.path.join(log_path,logname)

        print("Create log file %s in %s" %(filename, log_path))
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(filename= logfilepath,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)


        monitoring.register(CommandLogger())
        monitoring.register(ServerLogger())
        monitoring.register(TopologyLogger())

        print("Establishing connection for user %s with password %s" %(user, pw))
        mng_client = MongoDBClient.get_connection(user, pw)

        mng_db = mng_client['As2']
        db_cm = mng_db["sample"]
        if False:
            mng_db.drop_collection(collection_name)
            print("Dropped database for test cases.")
            os.remove(logfilepath)
            exit(0)

        data = CSVInputHandler.getdatafromCSV(filename)
        print("Trying to upload %s documents" % len(data))
        file_size = os.path.getsize(filename) / 1024

        success = 0
        failure = 0
        len_data  = len(data)
        response = 0
        for g, df in data.groupby(np.arange(len_data) // 100):
            try:
                json_data = CSVInputHandler.getJsonfromDf(df)
                logging.info("start insert %s row and % columns " % (df.shape[0], df.shape[1]))
                start_time = time.time()


                db_cm.insert(json_data)
                logging.info("succesfully inserted %s rows and %s columns" % (df.shape[0], df.shape[1]))
                resp = time.time()-start_time
                response+=resp
                rt_msg = "upload rate: %.2f Kb/s ---" % ((file_size  * (len(df) / len_data)) / resp )
                logging.info(rt_msg)
                print(rt_msg)
                suc = df.shape[0]
                success += suc

            except:
                logging.info("failed to upload. Retry ")
                json = CSVInputHandler.getJsonfromCSV(df)
                logging.info("start insert %s rows and % columns " % (df.shape[0], df.shape[1]))
                db_cm.insert(json)
                fail = df.shape[0]
                failure += fail

        logging.info("Overall success rate for : %s %%" %(success *100 / len_data))
        logging.info("Overall failure rate  for : %s %% for %s documents upload. " % ((failure * 100 / len_data), len_data))
        logging.info("Overall response time : %s seconds  for %s documents upload. " % (response, len_data))

        print("Overall success rate for : %s %%" %(success *100 / len_data))
        print("Overall failure rate  for : %s %% for %s documents upload. "%((failure * 100 / len_data), len_data))
        print("Overall response time : %s seconds  for %s documents upload. "%(response, len_data))




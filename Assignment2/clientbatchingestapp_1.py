#to read data from data sources(files/external databases) of the tenant/user and then store the data by calling APIs ofmysimbdp-coredms

from pymongo import MongoClient, monitoring
from datetime import datetime
import logging
import os
import time
import gridfs



class MongoDBClient(object):
    @staticmethod
    def get_connection(user, password):
        return MongoClient("mongodb+srv://%s:%s@cluster0-ukbbs.gcp.mongodb.net/test?retryWrites=true&w=majority" %(user, password), event_listeners=[CommandLogger()])

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
    def ingest(user, pw, log_path, file):



        if log_path is None:
            log_path = os.curdir
        if not  os.path.exists(log_path):
            os.mkdir(log_path)


        filename = user + "_" + str(datetime.now().strftime("%H_%M_%S")) + ".log"
        logfilepath = os.path.join(log_path, filename)

        print("Create log file %s in %s" %(filename, log_path))
        logging.basicConfig(filename= logfilepath,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)


        filename = file
        monitoring.register(CommandLogger())
        monitoring.register(ServerLogger())
        monitoring.register(TopologyLogger())

        print("Establishing connection for user %s with password %s" %(user, pw))
        mng_client = MongoDBClient.get_connection(user, pw)

        mng_db = mng_client['As2']
        file_size = os.path.getsize(filename)  /1024
        try:
            start_time = time.time()
            print("Ingesting file %s" %filename)
            logging.info("Ingesting file %s" %filename)
            fs = gridfs.GridFS(mng_db)
            a = fs.put(open( file, 'rb'))
            duration = time.time()-start_time

            ingestion_string = "Needed %s seconds ingestion time for %s of size %s KB"%(duration, filename, file_size)
            ingestion_rate = "%sKB/s" %(file_size / duration)
            logging.info("Successful ingestion")
            logging.info(ingestion_string)
            logging.info(ingestion_rate)
        except:
            logging.info("Failure for ingestion file %s " %filename)




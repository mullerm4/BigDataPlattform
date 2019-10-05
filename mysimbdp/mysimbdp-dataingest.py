#to read data from data sources(files/external databases) of the tenant/user and then store the data by calling APIs ofmysimbdp-coredms

from pymongo import MongoClient, monitoring
import logging
import pandas as pd
import os
import json
import numpy as np
import argparse
import  time



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
            data = pd.read_csv(filename).sample(samplesize)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dataingest : Uploads source from user..')
    parser.add_argument('-user', metavar='N', type=str,
                        help='username', default='new_user_42')
    parser.add_argument('-p', metavar='N', type=str,
                        help='password of the user', default='new_user_42')
    parser.add_argument('-samp', metavar='N', type=int,
                        help='sampels to be upload from source. If sample size is not set, upload whole dataset', default=43)
    parser.add_argument('-drop', metavar='N', type=bool,
                        help='drop table if desired',
                       default=False)



    logging.info("Running Urban Planning")

    args = parser.parse_args()
    filename = "2019.csv"
    monitoring.register(CommandLogger())

    print("Establishing connection for user %s with password %s" %(args.user, args.p))
    mng_client = MongoDBClient.get_connection(args.user, args.p)
    mng_db = mng_client['As1']  # Replace mongo db name
    collection_name = filename # Replace mongo db collection name

    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)

    # reading external source data
    print("Trying to upload %s documents" %(args.samp))

    data = CSVInputHandler.getdatafromCSV(filename, samplesize=args.samp)
    success = 0
    failure = 0
    len_data  = len(data)
    response = 0
    for g, df in data.groupby(np.arange(len_data) // 100):
        try:
            json_data = CSVInputHandler.getJsonfromDf(df)
            logging.info("start insert %s row and % collumns " % (df.shape[0], df.shape[1]))
            start_time = time.time()


            db_cm.insert(json_data)
            logging.info("succesfully inserted %s rows and %s collumns" % (df.shape[0], df.shape[1]))
            resp = time.time()-start_time
            response+=resp
            logging.info("response time %.2f seconds ---" % (resp))
            suc = df.shape[0]
            success += suc

        except:
            logging.info("failed to upload. Retry ")
            json = CSVInputHandler.getJsonfromCSV(df)
            logging.info("start insert %s rows and % collumns " % (df.shape[0], df.shape[1]))
            db_cm.insert(json)
            fail = df.shape[0]
            failure += fail


        finally:
            print()
            #print("---------------Progess rate %.2f %% of uploading %s documents -----------------" %((success * 100 / len_data), args.samp))
    print("Overall success rate for : %s %%" %(success *100 / len_data))
    print("Overall failure rate  for : %s %% for %s documents upload. "%((failure * 100 / len_data), args.samp))
    print("Overall response time : %s seconds  for %s documents upload. "%(response, args.samp))



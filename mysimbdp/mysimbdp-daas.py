#   key component to store and manage data .This component isa platform-as-a-service.

import pandas as pd


from pymongo import MongoClient

class Connect(object):
    @staticmethod
    def get_connection():
        return MongoClient("mongodb+srv://new_user_42:new_user_42@cluster0-ukbbs.gcp.mongodb.net/test?retryWrites=true&w=majority")

client = Connect.get_connection()

test = client.test2

test.inventory.insert_one(
    {"item": "canvas",
     "qty": 100,
     "tags": ["cotton"],
      "size": {"h": 28, "w": 35.5, "uom": "cm"}})
# data = pd.read_csv("2019.csv")
#
# print(data.shape)
#
# puffer =  data.iloc [[3, 4], :]
# for idx, item  in  enumerate(puffer):
#     print(puffer.iloc[[idx], 2])
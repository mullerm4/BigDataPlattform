#of which APIs can be called by external dataproducers/consumers to store/read data into/from mysimbdp-coredms. This component isa platform-as-a-service.

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
print(myclient.list_database_names())
mydb = myclient["mydatabase"]

print(mydb.list_collection_names())
mycol = mydb["test"]

#!/bin/bash

# Insert new data by providing the path to a csv file
python ./mysimbdp-daas.py -user="new_user_1" -p="new_user_1" -lp="data_ingest_perf" -ins=insert_data_mysimdb-daas.csv

# Reading documents fitting the json querry
python ./mysimbdp-daas.py -user="new_user_1" -p="new_user_1" -lp="data_ingest_perf" -read="{'determinand_notation': { '\$gt': 400 }}"

# Updating these documents in the collection
python  ./mysimbdp-daas.py -user="new_user_1" -p="new_user_1" -lp="data_ingest_perf" -read="{'determinand_notation': { '\$gt': 400 }}" -update="{'\$set': {'sample_purpose_label': 'Modified water label'}}"

# Reading documents to ensure that the doucuments are acutally updated
python ./mysimbdp-daas.py -user="new_user_1" -p="new_user_1" -lp="data_ingest_perf" -read="{'determinand_notation': { '\$gt': 400 }}"
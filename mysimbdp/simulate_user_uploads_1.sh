#!/bin/bash


echo "Simulating concurrent 10 diffrent user dataingest invokation"

python ./mysimbdp-dataingest.py -user="new_user_1"  -p="new_user_1" -dt=True -lp='log_concurrent_user_1'
# Start the first process
python ./mysimbdp-dataingest.py -user="new_user_1"  -p="new_user_1" -samp=50000 -lp='log_concurrent_user_1'

# Start the second process

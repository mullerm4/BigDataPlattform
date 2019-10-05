#!/bin/bash


echo "Simulating concurrent 10 diffrent user dataingest invokation"
# Start the first process
python ./mysimbdp-dataingest.py -user="new_user_1"  -p="new_user_1" -samp=500000 &

# Start the second process

python  ./mysimbdp-dataingest.py -user="new_user_2"  -p="new_user_2"  -samp=50000 &

python  ./mysimbdp-dataingest.py -user="new_user_3"  -p="new_user_3"  -samp=50000 &

python  ./mysimbdp-dataingest.py -user="new_user_4"  -p="new_user_4"  -samp=50000 &

python  ./mysimbdp-dataingest.py -user="new_user_5"  -p="new_user_5"  -samp=50000 &

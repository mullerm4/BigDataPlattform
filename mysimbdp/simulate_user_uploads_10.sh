#!/bin/bash


echo "Simulating concurrent 10 diffrent user dataingest invokation"
# Drop table to make sure that there is sufficient space for test cases
python ./mysimbdp-dataingest.py -user="new_user_1"  -p="new_user_1" -dt=True -lp='log_concurrent_user_10'

python ./mysimbdp-dataingest.py -user="new_user_1"  -p="new_user_1" -samp=50000 -lp='log_concurrent_user_10' &

# Start the second process

python  ./mysimbdp-dataingest.py -user="new_user_2"  -p="new_user_2"  -samp=50000 -lp='log_concurrent_user_10' &

python  ./mysimbdp-dataingest.py -user="new_user_3"  -p="new_user_3"  -samp=50000 -lp='log_concurrent_user_10' &

python  ./mysimbdp-dataingest.py -user="new_user_4"  -p="new_user_4"  -samp=50000 -lp='log_concurrent_user_10' &

python  ./mysimbdp-dataingest.py -user="new_user_5"  -p="new_user_5"  -samp=50000 -lp='log_concurrent_user_10' &

python  ./mysimbdp-dataingest.py -user="new_user_6"  -p="new_user_6"  -samp=50000 -lp='log_concurrent_user_10' &

python  ./mysimbdp-dataingest.py -user="new_user_7"  -p="new_user_7"  -samp=50000 -lp='log_concurrent_user_10' &

python  ./mysimbdp-dataingest.py -user="new_user_8"  -p="new_user_8"  -samp=50000 -lp='log_concurrent_user_10' &

python  ./mysimbdp-dataingest.py -user="new_user_9"  -p="new_user_9"  -samp=50000 -lp='log_concurrent_user_10' &

python  ./mysimbdp-dataingest.py -user="new_user_10"  -p="new_user_10"  -samp=50000 -lp='log_concurrent_user_10'
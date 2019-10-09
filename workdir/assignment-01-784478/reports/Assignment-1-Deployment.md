# 1.Preparations to run mysimbdb
The mysimbdb-coredms is running on a MongoDB Atlas Server. I already whitelist every IP-Adress that the server would accept a test from an arbitrary workstation. If there are still access problems, please contact me.

Moreover, to run several tests I created bash scripts that are only runnable in a Linux environment. Also, my code based written and evaluated using python 3.6.
## 1.1 Prepare  mysimbdb-dataingest
The code is in the code directory of my submitted zip file. To install everything automatically, please specify your python environment in your Linux system:
```bash
source /your_python_env_path/bin/activate
```
Then all packages can be automatically installed by invoking:
```bash
pip install -r requirements.txt
```
The code also assumes that there is the 2019.csv dataset in the code directory, since it causes some issues in my environment.

## 1.2 How to run the test for mysimbdb-dataingest

I created already some bash scripts to run several different dataingest test simultaneously. There are also located in the code subdirectory
```
simulate_user_uploads_1.sh
simulate_user_uploads_2.sh
simulate_user_uploads_5.sh
simulate_user_uploads_10.sh
```
The last number of the files indicates how many services are running simultaneously.
For example the file simulate_user_uploads_10.sh
consists of:
```bash
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
```
If the resources of the test environment are exhausted for a heavy test like ***simulate_user_uploads_10.sh***, the sample size per user can be decreased changing ***-samp*** number.

## 1.3 Docker environment creation (Not necessary if pip environment is already created)
This step is not necessary if the pip environment is already installed. Also, note that the log files are created in the ***image file*** when using the docker environment.
My docker utilized docker version is ***19.03.2***.
The image can be created using the following command:
```bash
## naviage to the code path using the terminal
cd /codepath/
### build the environment
docker build --tag=mysimbdb .
```
The test for Part2 can be now executed using the command line:
```bash
docker run mysimbdb
```


## 1.4 How to print the options of mysimbdb-dataingest
I implemented also a help for all arguments which are printed using the command:
```bash
python ./mysimbdp-dataingest.py --help
```


## 1.5 Log generation
The code will also generate the log files in the code directory in a separate folder specified in the ***-log*** argument used in the bashfile.
After running the bash script the code directory should have 5 different folder:
```bash
/log_concurrent_user_1
/log_concurrent_user_2
/log_concurrent_user_5
/log_concurrent_user_10
```

# 2 mysimbdb-daas
## 2.1 Run mysimbdb-daas
I also implemented the service ***mysimbdb-daas***. This service can insert, read and update in the MongoDB Atlas database. The bash script ***insert_test_data_mysimbd-dass.sh*** runs these performance tests using one insert, one update and two read instructions.

## 2.2 List help arguments mysimbdb-daas
I implemented also help for all arguments which are printed using the command:
```bash
python ./mysimbdp-daas.py --help
```
## 2.3 Log generation

The code will also generate the log files in the code directory in a separate folder specified in the ***-log*** argument used in the bash file.
After running the bash script the code directory should have one additional folder called ***data_ingest_perf***:
```
+--data_ingest_perf
|   +-- Insert_performance_new_user_time.log
|   +-- Read_performance_new_user_time.log
|   +-- Read_performance_new_user_time.log
|   +-- Update performnacenew_user_time.log
|   +-- on-simplicity-in-technology.markdown
```

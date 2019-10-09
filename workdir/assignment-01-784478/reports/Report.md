#  Report First Assignment - Building Your Big-Data Platforms

## Part 1

### 1.1)
![Kitten](AS1_1.png "A cute kitten")
There two implemented developed python script services that interact with the mysimbdp-coredms. The service ***mysimbdp-dataingest*** read the data from sources as CSV files and upload it in batches into the database using the mysimbdp-coredms. The mysimbdp-coredms service is hosted by MongoDB Atlas with three nodes and it manages and stores the data into the database.
The other service mysimbdb-daas is python service which stores and reads data from the database using the mysimbdp-coredms service. Both python script utilizing the API pymongo in order to interact with the mysimbdp-coredms.


### 1.2

The minimum requirement for a MongoDB cluster is to have at least two nodes: The first node represents a primary node where the second one represents a backup node. In the case that the primary node fails, the second node becomes the primary node. If a cluster has more than two nodes, an election takes place which chooses one of the available nodes to become the primary partition. This configuration provides a horizontally scalable and fault-tolerant deployment.

### 1.3

VM’s allocate in general more CPU and memory resources compared to the Docker technology. Moreover, the container is light-weighted in their snapshot size and can use shared labrys of the OS.
This allows multiple containers on the same operating system. Besides, containers are launching in milliseconds where virtual machines take in general some minutes to launch.
Hence, I will use the container from Docker.

### 1.4


As I already mentioned before, I chose MongoDB Atlas as my mysimbdp-coredms provider which offers me a cluster of three nodes. The first node serves as a primary node and will be replaced by one of the two other nodes if it fails.
The cluster is hosted by Google Platforms service and provides shared CPU and memory usages which will be dynamically allocated if the mysimbdp-coredms require it.
MongoDB provides the opportunity to scale vertically by buying another CPU and RAM or scaling horizontally by ordering resources. Further horizontally scaling can be achieved by adding additional servers to increase capacity as required.  These resources are completely sufficient for this use case since my bandwidth is the real bottleneck to the server.
### 1.5
Unfortunately, my computer does not have sufficient CPU, RAM and storage resources to host the platform on my machine. As I mentioned before, I chose MongoDB since it provides sufficient resources for this use case for free. Besides, it based on a schema-less table which reduces the complexity of the database. In particular, it allows the user to upload different documents of different sizes and the number of fields/columns in a single database.
## Part 2

### 2.1)
![Kitten](AS1_21.png "A cute kitten")
The design above represents the general structure of the MongoDB, embedding the data schema of the 2019.csv data set. Unlike a SQL-schema, each row is stored as a document with the corresponding fields/columns.
In our case the datasheet.
These are the following used in the MongoDB:

|object id | id |  Label | samplingPoint| notation| label| DateTime| determinand.label|
|---|---|---|---|---|---|---|---|

|determinand.definition | notation| resultQualifier.notation| result| interpretation|
---|---|---|---|---|

| determinand| dMaterialType| isCompliance| purpose.label| easting| northing|
---|---|---|---|---|---|

![Kitten](data_shema.png "A cute kitten")

### 2.2)
The collections of MongoDB are partition by shared keys that define the size and range of a chunk. A chunk is a subset of the collection and its size is adjustable. In particular., the chunk size represents how many documents can be stored in one chunk. Small chunks provide a uniform distribution of the data and will require more frequent migrations. In contrast, large chunk sizes lead to more efficient network transportation of the data since fewer layers have to be queried but suffer by a uniform data distribution on the chunks.
Another perspective is that the chunks itself have to be split when the size gets exceeded or too many documents are inserted. A splitting operation is required to prevent the chunks from growing too large. The splitting operation split a chunk based on the shared key shard into smaller multiple chunks.
The confgiured chunk size of my ***mysimbdp-coredms.py*
### 2.3)
I developed a python file called ***mysimbdp-dataingest.py***  and use a docker container environment to run the program.
The ***mysimbdp-dataingest.py***   uses the pymongo API to initialize a client instance which creates a connection to my MongoDB Atlas account.
### 2.4)
To run the n of concurrent ***mysimbdp-dataingest.py*** , I added 5 scrips in the docker environment which invokes n times concurrent ***mysimbdp-dataingest*** for a different user.  
Each service upload then the sampled data from the 2019.csv into the MongoDB database.

One script example for invoking 10 concurrent services in the docker environment.
```bash
#!/bin/bash


echo "Simulating concurrent 10 diffrent user dataingest invokation"
# Start the first process
python ./mysimbdp-dataingest.py -user="new_user_1"  -p="new_user_1" -samp=500000  -lp='log_concurrent_user_10' &

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


To upload the 50000 documents, I used a batch size of 100.
This shows the log of a single batch including the success rate as well as the response time. The full log file can be found in the log directory.


#### n=1 simulate_user_uploads_1.sh
To upload the 50000 documents, I used a batch size of 100.
This shows the log of a single batch including the success rate as well as the response time. The full log file can be found in the log directory.

```
00:04:30,246 root INFO start insert 100 row and ollumns
00:04:30,253 root INFO Command insert with request id 2044897763 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
00:04:30,253 root INFO Command insert with request id 2044897763 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
00:04:30,313 root INFO Command insert with request id 2044897763 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 62925 microseconds
00:04:30,313 root INFO Command insert with request id 2044897763 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 62925 microseconds
00:04:30,313 root INFO succesfully inserted 100 rows and 17 collumns
00:04:30,313 root INFO response time 0.07 seconds ---
```
So the overall response time  and error rate is:

```
00:05:07,213 root INFO Overall success rate for : 100.0 %
00:05:07,213 root INFO Overall failure rate  for : 0.0 % for 50000 documents upload.
00:05:07,213 root INFO Overall response time : 34.56025314331055 seconds  for 50000 documents upload.
```
### n=2 simulate_user_uploads_2.sh

##### Log results new_user_1:
```
00:29:24,428 root INFO start insert 100 row and ollumns
00:29:24,431 root INFO Command insert with request id 1189641421 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
00:29:24,431 root INFO Command insert with request id 1189641421 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
00:29:24,488 root INFO Command insert with request id 1189641421 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 57911 microseconds
00:29:24,488 root INFO Command insert with request id 1189641421 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 57911 microseconds
00:29:24,488 root INFO succesfully inserted 100 rows and 17 collumns
00:29:24,488 root INFO response time 0.06 seconds ---
```

```
00:30:00,784 root INFO Overall success rate for : 100.0 %
00:30:00,784 root INFO Overall failure rate  for : 0.0 % for 50000 documents upload.
00:30:00,784 root INFO Overall response time : 33.978217124938965 seconds  for 50000 documents upload.

```

##### Log results new_user_2:
```
00:29:24,530 root INFO start insert 100 row and ollumns
00:29:24,534 root INFO Command insert with request id 1025202362 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
00:29:24,534 root INFO Command insert with request id 1025202362 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
00:29:24,590 root INFO Command insert with request id 1025202362 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 57747 microseconds
00:29:24,590 root INFO Command insert with request id 1025202362 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 57747 microseconds
00:29:24,590 root INFO succesfully inserted 100 rows and 17 collumns
```
So the overall response time  and error rate is:

```
00:30:00,974 root INFO Overall success rate for : 100.0 %
00:30:00,975 root INFO Overall failure rate  for : 0.0 % for 50000 documents upload.
00:30:00,975 root INFO Overall response time : 34.1162850856781 seconds  for 50000 documents upload.

```
#### n=5 simulate_user_uploads_5.sh
The response and success rate is for all user nearly identical, hence in the following test report is just a part from the log for one user reported.
#### Log results new_user_5:

```
20:02:23,153 root INFO start insert 100 row and ollumns
20:02:23,165 root INFO Command insert with request id 1276673168 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
20:02:23,166 root INFO Command insert with request id 1276673168 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
20:02:23,275 root INFO Command insert with request id 1276673168 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 115296 microseconds
20:02:23,275 root INFO Command insert with request id 1276673168 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 115296 microseconds
20:02:23,276 root INFO succesfully inserted 100 rows and 17 collumns
20:02:23,276 root INFO response time 0.12 seconds ---
```
So the overall response time  and error rate is:
```
20:02:23,276 root INFO Overall success rate for : 100.0 %
20:02:23,276 root INFO Overall failure rate  for : 0.0 % for 50000 documents upload.
20:02:23,277 root INFO Overall response time : 41.304049491882324 seconds  for 50000 documents upload.
```





#### n=10 simulate_user_uploads_10.sh



#### Log results new_user_5:



```
00:33:44,534 root INFO start insert 100 row and 17 collumns
00:33:44,541 root INFO Command insert with request id 1748349614 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
00:33:44,541 root INFO Command insert with request id 1748349614 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
00:33:44,661 root INFO Command insert with request id 1748349614 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 122667 microseconds
00:33:44,661 root INFO Command insert with request id 1748349614 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 122667 microseconds
00:33:44,661 root INFO succesfully inserted 100 rows and 17 collumns
00:33:44,662 root INFO response time 0.13 seconds ---
```
So the overall response time  and error rate is:
```
00:33:46,91 root INFO Overall success rate for : 100.0 %
00:33:46,91 root INFO Overall failure rate  for : 0.0 % for 50000 documents upload.
00:33:46,91 root INFO Overall response time : 70.22667384147644 seconds  for 50000 documents upload.
```
### 2.5)
I don't experience failures when pushing a lot of data as 50.000 documents with several users simultaneously.
The limiting factor in this task is the infrastructure of my test environment and not the mysimbdp since the RAM of my notebook was maximally exhausted when running the test for 10 users simultaneously. Additionally, the upload of the 10 concurrent users is limited to my bandwidth.
Comparing the results of all test as shown in the table illustrated below, the average time needed for uploading 50.0000 documents with concurrent N=10 and N=1 user differ by 35 seconds. This twice the time of the test for one user, but then the test last test uploads 10 times the amount of data.



| Test| Average batch success rate| Average batch response|  Average success| Average time|
---|---|---|---|---|
N=1 concurrent user|100%|0.07 sec|100%|34 sec|
N=2 concurrent user|100%|0.07 sec|100%|34 sec|
N=5 concurrent user|100%|0.12 sec|100%|41 sec|
N=10 concurrent user|100%|0.13 sec|100%|70 sec|

### My suggestion to improve the performance:
The first t

## Part 3
## 3.3
Service discovery aims to build a flexible and maintainable infrastructure that allows combining services with minimal effort. DNS interfaces might be an appropriate solution for this problem, but this requires also to maintain DNS entries and keeping them up to date. However, the service discovery layer Consul from Hashicorp is a service discovery layer for a data center, as well as being a distributed key-value store and able to perform cross-data center replication and discovery. I would extend the ***mysimbdp-dataingest*** with the Consul interface to benefit from the service discovery layer.
## 3.4
The service of ***mysimbdp-daas*** would need several API interfaces in my opinion.
First of all, a user might want to check whether the documents are already up to date on the database. This requires a service that determines requested queries efficiently. Moreover, there is also a need to update and maintain the collection of databases. These services should update specific entries based on a query with new values given in an argument.
Furthermore, there is also an API required which can insert a huge amount of documents. This API should also be able to load the data into batches into the platform and also handles upload failures.
Explain APIs you would design for ***mysimbdp-daas***  so that any other developer who wants
to implement ***mysimbdp-dataingest*** can write his/her ingestion program to write the
data into mysimbdp-coredms by calling ***mysimbdp-daas***  (1 point)
## 3.5
I would change the implementation of ***mysimbdp-dataingest*** in the following sense:
The ***mysimbdp-dataingest*** service would mainly manage the external data and convert it into a suitable document format since MongoDB does not understand SQL-tables or CSV files.
Afterward, this service call the ***mysimbdb-daas**** with the corresponding JSON data format to upload the documents to the ***mysimbdb-coredms***.

## Bonus Points
I also implemented the service ***mysimbdb-daas***. This service is able to insert, read and update in the MongoDB Atlass database. The bash script ***insert_test_data_mysimbd-dass.sh*** runs these performance test using one insert, one update and two read instructions.
The content of the script is the following:
```bash
#!/bin/bash

# Insert new data by providing the path to a csv file
python ./mysimbdp-daas.py -user="new_user_1" -p="new_user_1" -lp="data_ingest_perf" -ins=insert_data_mysimdb-daas.csv

# Reading documents fitting the json querry
python ./mysimbdp-daas.py -user="new_user_1" -p="new_user_1" -lp="data_ingest_perf" -read="{'determinand_notation': { '\$gt': 400 }}"

# Updating these documents in the collection
python  ./mysimbdp-daas.py -user="new_user_1" -p="new_user_1" -lp="data_ingest_perf" -read="{'determinand_notation': { '\$gt': 400 }}" -update="{'\$set': {'sample_purpose_label': 'Modified water label'}}"

# Reading documents to ensure that the doucuments are acutally updated
python ./mysimbdp-daas.py -user="new_user_1" -p="new_user_1" -lp="data_ingest_perf" -read="{'determinand_notation': { '\$gt': 400 }}"
```

Note: The instructions for reproducing these results are explained in the [Assignment-1-Deployment.md](Assignment-1-Deployment.md).

 These are the following results from the log files:

Performance log located in the *.../data_ingest_perf/Insert_performance_new_user_1_14_19_36.log*:
```bash
14:19:37,288 root INFO start insert 20 row and ollumns
14:19:37,289 root INFO Command insert with request id 1189641421 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:37,289 root INFO Command insert with request id 1189641421 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:37,392 root INFO Command insert with request id 1189641421 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 103432 microseconds
14:19:37,393 root INFO Command insert with request id 1189641421 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 103432 microseconds
14:19:37,393 root INFO succesfully inserted 20 rows and 18 collumns
14:19:37,393 root INFO response time 0.11 seconds ---
14:19:37,394 root INFO Overall success rate for : 100.0 %
14:19:37,394 root INFO Overall failure rate  for : 0.0 % for 20 documents upload.
14:19:37,394 root INFO Overall response time : 0.10567021369934082 seconds  for 20 documents upload.
```


Read operation:
./data_ingest_perf/Read_performance_new_user_1_14_19_38.log
```bash
14:19:38,227 root INFO Querrying the following querry {'determinand_notation': {'$gt': 400}}
14:19:38,227 root INFO Querry time takes 0.0001 seconds
14:19:38,559 root INFO Command saslStart with request id 424238335 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:38,560 root INFO Command saslStart with request id 424238335 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:38,595 root INFO Command saslStart with request id 424238335 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 35212 microseconds
14:19:38,595 root INFO Command saslStart with request id 424238335 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 35212 microseconds
14:19:38,610 root INFO Command saslContinue with request id 719885386 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:38,611 root INFO Command saslContinue with request id 719885386 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:38,646 root INFO Command saslContinue with request id 719885386 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34853 microseconds
14:19:38,646 root INFO Command saslContinue with request id 719885386 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34853 microseconds
14:19:38,647 root INFO Command saslContinue with request id 1649760492 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:38,647 root INFO Command saslContinue with request id 1649760492 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:38,682 root INFO Command saslContinue with request id 1649760492 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34923 microseconds
14:19:38,682 root INFO Command saslContinue with request id 1649760492 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34923 microseconds
14:19:38,683 root INFO Command count with request id 596516649 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:38,683 root INFO Command count with request id 596516649 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:38,720 root INFO Command count with request id 596516649 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 36219 microseconds
14:19:38,720 root INFO Command count with request id 596516649 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 36219 microseconds
14:19:38,720 root INFO Found 11 results according to the querry
.....

```
Two of the eleven documents which fit the query:
```bash
14:19:40,309 root INFO {'_id': ObjectId('5d9dc2490b6c975c1d36e05e'), 'Unnamed: 0': 781646, '@id': 'http://environment.data.gov.uk/water-quality/data/measurement/SW-3384978-9993', 'sample_samplingPoint': 'http://environment.data.gov.uk/water-quality/id/sampling-point/SW-82211815', 'sample_samplingPoint_notation': 'SW-82211815', 'sample_samplingPoint_label': 'RIVER HAYLE AT ESTUARY MOUTH', 'sample_sampleDateTime': '2019-07-25T11:07:00', 'determinand_label': 'NH3 filt N', 'determinand_definition': 'Ammoniacal Nitrogen, Filtered as N', 'determinand_notation': 9993, 'resultQualifier_notation': '<', 'result': 0.007, 'codedResultInterpretation_interpretation': None, 'determinand_unit_label': 'mg/l', 'sample_sampledMaterialType_label': 'ESTUARINE WATER', 'sample_isComplianceSample': False, 'sample_purpose_label': 'STATUTORY FAILURES (FOLLOW UPS AT NON-DESIGNATED POINTS)', 'sample_samplingPoint_easting': 154980, 'sample_samplingPoint_northing': 38000}
14:19:40,309 root INFO {'_id': ObjectId('5d9dc2490b6c975c1d36e061'), 'Unnamed: 0': 760626, '@id': 'http://environment.data.gov.uk/water-quality/data/measurement/SW-3377741-3722', 'sample_sampling
```

'Update query:
**"{'\$set': {'sample_purpose_label': 'Modified water label'}}**

*/data_ingest_perf/Update performnacenew_user_1_14_19_39.log*:
```bash
14:19:40,78 root INFO Command saslStart with request id 424238335 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:40,79 root INFO Command saslStart with request id 424238335 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:40,117 root INFO Command saslStart with request id 424238335 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34635 microseconds
14:19:40,117 root INFO Command saslStart with request id 424238335 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34635 microseconds
14:19:40,133 root INFO Command saslContinue with request id 719885386 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:40,133 root INFO Command saslContinue with request id 719885386 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:40,169 root INFO Command saslContinue with request id 719885386 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 35512 microseconds
14:19:40,169 root INFO Command saslContinue with request id 719885386 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 35512 microseconds
14:19:40,170 root INFO Command saslContinue with request id 1649760492 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:40,170 root INFO Command saslContinue with request id 1649760492 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:40,205 root INFO Command saslContinue with request id 1649760492 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34850 microseconds
14:19:40,205 root INFO Command saslContinue with request id 1649760492 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34850 microseconds
14:19:40,206 root INFO Command count with request id 596516649 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:40,207 root INFO Command count with request id 596516649 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:40,244 root INFO Command count with request id 596516649 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 37547 microseconds
14:19:40,245 root INFO Command count with request id 596516649 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 37547 microseconds
14:19:40,245 root INFO Found 11 results according to the querry
```

'Another read operation was performed in order to make sure that the field *determinand_notation* of the documents which fits the query: **"{'determinand_notation': { '\$gt': 400 }}**"
 from the first operation have been already updated to
 Modified water label

 Read_performance_new_user_1_14_19_41.log:

```bash
14:19:41,194 root INFO Querry time takes 0.0001 seconds
14:19:41,545 root INFO Command saslStart with request id 424238335 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,545 root INFO Command saslStart with request id 424238335 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,581 root INFO Command saslStart with request id 424238335 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 35203 microseconds
14:19:41,581 root INFO Command saslStart with request id 424238335 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 35203 microseconds
14:19:41,596 root INFO Command saslContinue with request id 719885386 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,596 root INFO Command saslContinue with request id 719885386 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,631 root INFO Command saslContinue with request id 719885386 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34573 microseconds
14:19:41,631 root INFO Command saslContinue with request id 719885386 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 34573 microseconds
14:19:41,632 root INFO Command saslContinue with request id 1649760492 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,632 root INFO Command saslContinue with request id 1649760492 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,667 root INFO Command saslContinue with request id 1649760492 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 35120 microseconds
14:19:41,668 root INFO Command saslContinue with request id 1649760492 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 35120 microseconds
14:19:41,668 root INFO Command count with request id 596516649 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,669 root INFO Command count with request id 596516649 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,705 root INFO Command count with request id 596516649 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 36183 microseconds
14:19:41,705 root INFO Command count with request id 596516649 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 36183 microseconds
14:19:41,706 root INFO Found 11 results according to the querry
14:19:41,707 root INFO Command find with request id 1189641421 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,707 root INFO Command find with request id 1189641421 started on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017)
14:19:41,746 root INFO Command find with request id 1189641421 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 39019 microseconds
14:19:41,746 root INFO Command find with request id 1189641421 on server ('cluster0-shard-00-00-ukbbs.gcp.mongodb.net', 27017) succeeded in 39019 microseconds
```
These are two of the eleven raw documents which changed their field 'sample_purpose_label': 'Modified water'.
```
14:19:41,747 root INFO {'_id': ObjectId('5d9dc2490b6c975c1d36e05e'), 'Unnamed: 0': 781646, '@id': 'http://environment.data.gov.uk/water-quality/data/measurement/SW-3384978-9993', 'sample_samplingPoint': 'http://environment.data.gov.uk/water-quality/id/sampling-point/SW-82211815', 'sample_samplingPoint_notation': 'SW-82211815', 'sample_samplingPoint_label': 'RIVER HAYLE AT ESTUARY MOUTH', 'sample_sampleDateTime': '2019-07-25T11:07:00', 'determinand_label': 'NH3 filt N', 'determinand_definition': 'Ammoniacal Nitrogen, Filtered as N', 'determinand_notation': 9993, 'resultQualifier_notation': '<', 'result': 0.007, 'codedResultInterpretation_interpretation': None, 'determinand_unit_label': 'mg/l', 'sample_sampledMaterialType_label': 'ESTUARINE WATER', 'sample_isComplianceSample': False, 'sample_purpose_label': 'STATUTORY FAILURES (FOLLOW UPS AT NON-DESIGNATED POINTS)', 'sample_samplingPoint_easting': 154980, 'sample_samplingPoint_northing': 38000}
14:19:41,747 root INFO {'_id': ObjectId('5d9dc2490b6c975c1d36e061'), 'Unnamed: 0': 760626, '@id': 'http://environment.data.gov.uk/water-quality/data/measurement/SW-3377741-3722', 'sample_samplingPoint': 'http://environment.data.gov.uk/water-quality/id/sampling-point/SW-81810915', 'sample_samplingPoint_notation': 'SW-81810915', 'sample_samplingPoint_label': 'GORRAN HAVEN (LITTLE PERHAVER) BEACH STR', 'sample_sampleDateTime': '2019-05-16T14:08:00', 'determinand_label': 'IE Pres', 'determinand_definition': 'Enterococci: Intestinal: Presumptive: MF', 'determinand_notation': 3722, 'resultQualifier_notation': None, 'result': 72.0, 'codedResultInterpretation_interpretation': None, 'determinand_unit_label': 'cfu/0.1l', 'sample_sampledMaterialType_label': 'RIVER / RUNNING SURFACE WATER', 'sample_isComplianceSample': False, 'sample_purpose_label': 'PLANNED INVESTIGATION (LOCAL MONITORING)', 'sample_samplingPoint_easting': 201300, 'sample_samplingPoint_northing': 41560}'
```

So, in general, I can report that the performance of these data ingest are pretty good at the consideration that all resources are free. The longest operation is still the insert operation with an approximate 0.1 seconds of 20 documents. In contrast, the read operation took 0.035120  and the update operation 0.034923 seconds.

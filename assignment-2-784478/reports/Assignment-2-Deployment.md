# Preparations to run mysimbdb
To run this submission, it is *docker* as well as *docker-compose* required.
The scripts were implemented and evaluated on a Ubuntu 18.04 (64-bit machine).
Since, the following script will install all packages to the container, an active internet
connections is required.

# Deploy the environment
The environment is very easy to deploy:
```
cd code
docker-compose up
```
To enforce the rebuild of the image, the following command can be used:
```
docker-compose up --build
```

# FLaNK-IceIceData
Docker, OSS, Apache NiFi, Apache Iceberg, Apache Hive Metastore, Postgresql, LocalStack, S3, JSON, Data



````
env.sh
export DATABASE_HOST=kafka
export DATABASE_DB=hivemetastore
export DATABASE_USER=tspann
export DATABASE_PASSWORD=tspann
export S3_BUCKET=tspann
export S3_PREFIX=tspann

aws configure --profile default
aws s3 mb s3://tspann --endpoint-url http://192.168.1.166:4566

aws s3 ls --endpoint-url=http://192.168.1.166:4566 --recursive --human-readable

localstack status services
````


## REFERENCE

https://dev.to/navedrizv/setup-aws-s3-bucket-locally-with-localstack-3n4o


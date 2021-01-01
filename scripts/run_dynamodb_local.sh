#!/bin/bash

DDB_LOCAL_BUCKET_URI="https://s3.us-west-2.amazonaws.com/dynamodb-local"
DDB_LOCAL_TARBALL_FILE="dynamodb_local_latest.tar.gz"
DDB_LOCAL_CHCKSUM_FILE="$DDB_LOCAL_TARBALL_FILE.sha256"
DDB_LOCAL_TARBALL_URI="$DDB_LOCAL_BUCKET_URI/$DDB_LOCAL_TARBALL_FILE"
DDB_LOCAL_CHCKSUM_URI="$DDB_LOCAL_BUCKET_URI/$DDB_LOCAL_CHCKSUM_FILE"

echo "==> Downloading DynamoDB Local @ $DDB_LOCAL_TARBALL_URI"
wget -NP /tmp $DDB_LOCAL_TARBALL_URI
echo "==> Downloading checksum @ $DDB_LOCAL_CHCKSUM_URI"
wget -NP /tmp $DDB_LOCAL_CHCKSUM_URI
echo "==> Validating download package..."
echo "$(cut -f1 -d" " /tmp/$DDB_LOCAL_CHCKSUM_FILE) /tmp/$DDB_LOCAL_TARBALL_FILE" | sha256sum --check

echo "==> Untarring DynamoDB Local..."
mkdir -p /tmp/dynamodb
rm -rf /tmp/dynamodb/*
tar -xf /tmp/$DDB_LOCAL_TARBALL_FILE -C /tmp/dynamodb

echo "==> Spawning DyanmoDB Local..."
java -Djava.library.path=/tmp/dynamodb/DynamoDBLocal_lib -jar /tmp/dynamodb/DynamoDBLocal.jar -inMemory -delayTransientStatuses &>/dev/null &

#!/bin/bash
IP_PATH=$1

# echo $IP_PATH
while read line
do
	echo "$line"
	scp remote_setup.sh $line":/home/rocky/Documents/git/Net/Kafka"
	ssh $line "ls /home/rocky/Documents/git/Net/Kafka/"
	ssh $line "bash -s" < /home/rocky/Documents/git/Net/Kafka/remote_setup.sh
done < "$IP_PATH"
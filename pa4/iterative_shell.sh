#!/bin/bash

######  Initially for interative command, not used in this demo ############
PROMPT='$ '
list_topic='bin/kafka-topics.sh --list --zookeeper localhost:2181'
list_consumer='bin/kafka-consumer-groups.sh  --list --bootstrap-server localhost:9092'
create_topic='bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test1'
delete_topic='bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic test1'
while :
do
  echo -n "$PROMPT"
  read line
  if [ "$line" = 'list_topic' ]
  then
  	eval $list_topic
  elif [ "$line" = 'list_consumer' ]
  then
  	eval $list_consumer
  elif [ "$line" = 'create_topic' ]
  then
    eval $create_topic
  elif [ "$line" = 'delete_topic' ]
  then 
    eval $delete_topic
  fi
  done
exit 0

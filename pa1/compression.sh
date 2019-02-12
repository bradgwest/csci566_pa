#!/usr/bin/env bash

# A script for determining compression time from network measurements

# Set Latency Rule
sudo tc qdisc add dev wlp1s0 root netem delay 200ms rate 100kbit burst 16kbit limit 10000	

ts=$(date +%s%N)
# Download the file
scp -C -i aws_csci566_pa1.pem ubuntu@ec2-18-191-149-47.us-east-2.compute.amazonaws.com:~/file.txt .
tt=$((($(date +%s%N) - $ts)/1000000))
DURATION+=( $tt )
	
# Delete Latency Rule
sudo tc qdisc del dev wlp1s0 root

# Print and write results to file (if positional argument)
echo --RESULTS--
echo latency,duration
for ((i=0; i<${#LATENCY[*]}; i++));
do
    echo ${LATENCY[i]},${DURATION[i]}
    if [ "$1" != "" ]; then
	    echo ${LATENCY[i]},${DURATION[i]} >> $1
    fi
done
echo DONE

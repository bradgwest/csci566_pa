#!/usr/bin/env bash

# A script for measuring download times for various latency configurations

LATENCY=( 50 100 200 300 400 500 600 700 800 900 1000 )
DURATION=( )
for l in "${LATENCY[@]}"
do
	echo Latency ${l}ms
	# Set Latency Rule
	sudo tc qdisc add dev wlp1s0 root netem delay ${l}ms	

	ts=$(date +%s%N)
	# Download the file
	scp -i aws_csci566_pa1.pem ubuntu@ec2-18-191-149-47.us-east-2.compute.amazonaws.com:~/file.txt .
	tt=$((($(date +%s%N) - $ts)/1000000))
	DURATION+=( $tt )
	
	# Delete Latency Rule
	sudo tc qdisc del dev wlp1s0 root
done

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

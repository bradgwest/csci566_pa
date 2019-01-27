#!/bin/bash

# A script for measuring download speed at varying bandwidth restrictions 

BANDWIDTH=( 100 100 100 100 100 100 100 )
DURATION=( )
MEASURED_B=( )
for b in "${BANDWIDTH[@]}"
do
	echo BANDWIDTH ${b}KBits/sec
	# Set Latency Rule
	sudo tc qdisc add dev wlp1s0 root tbf rate ${b}kbit burst 16kbit limit 10000

	ts=$(date +%s%N)
	# Download the file
	scp -i aws_csci566_pa1.pem ubuntu@ec2-18-191-149-47.us-east-2.compute.amazonaws.com:"gzip ~/file.txt" .
	tt=$((($(date +%s%N) - $ts)/1000000))
	DURATION+=( $tt )

	# Measure the bandwidth
	iperf3 --logfile iperf3.log -c 18.191.149.47
	echo $(grep receiver$ iperf3.log)
	B=$( grep receiver$ iperf3.log | grep -Po [0-9\\.]+\\sKbits/sec | grep -Po [0-9\\.]+)
	echo Measured Bandwidth: $B
	MEASURED_B+=( $B )
	rm -f iperf3.log
	
	# Delete Latency Rule
	sudo tc qdisc del dev wlp1s0 root
done

# Print and write results to file (if positional argument)
echo --RESULTS--
echo bandwidth,duration
for ((i=0; i<${#BANDWIDTH[*]}; i++));
do
    echo ${MEASURED_B[i]},${DURATION[i]}
    if [ "$1" != "" ]; then
	    echo ${MEASURED_B[i]},${DURATION[i]} >> $1
    fi
done
echo DONE

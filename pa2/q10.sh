#!/usr/bin/env bash

# IP to send to
SERVER_IP=$1
# Output file to write to
OUTPUT=$2

if [[ ! -d  results ]]; then
  mkdir results
fi

sudo tc qdisc add dev eth0 root handle 1: netem delay 30ms
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 30ms burst 32kbit

echo Sending to ${SERVER_IP}, writing to ${OUTPUT}
python3 client_udp.py -s ${SERVER_IP} -p 5201 -t cs -b 32 -q 10 > ${OUTPUT}

## delete the rule
sudo tc qdisc del dev eth0 root

echo ...DONE

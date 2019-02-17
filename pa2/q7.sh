#!/usr/bin/env bash

# loss percentage (0.2, 0.4)
LOSS=$1
# whether it is client or not (true, false)
CLIENT=$2
# IP to send to if client
SERVER_IP=$3

if [[ ! -d  timbo ]]; then
  mkdir timbo
fi

## delete the rule
sudo tc qdisc del dev eth0 root
## Add rules
sudo tc qdisc add dev eth0 root handle 1: netem delay 30ms loss ${LOSS}%
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 30ms burst 32kbit

if [[ "$CLIENT" = "true" ]]; then
  echo client
  python3 client_udp.py -s ${SERVER_IP} -p 5201 -t cs > ./results/q7_client_${LOSS}.csv
else
  echo server
  python3 server_udp.py -s ${SERVER_IP} -p 5201 -t cs > ./results/q7_server_${LOSS}.csv
fi

echo ...DONE

#!/usr/bin/env bash

# loss percentage (0.2, 0.4)
LOSS=$1
# whether it is client or not (true, false)
CLIENT=$2
# IP to send to if client
SERVER_IP=$3

if [[ ! -d  results ]]; then
  mkdir results
fi

if [[ ! -e ./results/q7_results.csv ]]; then
  touch ./results/q7_results.csv
fi

## Add rules
if [[ "${LOSS}" = "0" ]]; then
  sudo tc qdisc add dev eth0 root handle 1: netem delay 30ms
else
  sudo tc qdisc add dev eth0 root handle 1: netem delay 30ms loss ${LOSS}%
fi
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 30ms burst 32kbit

if [[ "$CLIENT" = "true" ]]; then
  echo Running client
  python3 client_udp.py -s ${SERVER_IP} -p 5201 -t cs -q 7 > ./results/q7_client_${LOSS}.csv
  SENT=$(grep -c "send" ./results/q7_client_${LOSS}.csv)
  REC=$(grep -c "rec" ./results/q7_client_${LOSS}.csv)
  echo Client sent ${SENT} and received ${REC} with loss ${LOSS}
  echo "${LOSS},${SENT},${REC}" >> ./results/q7_results.csv
else
  echo running server
  python3 server_udp.py -s ${SERVER_IP} -p 5201 -t cs -q 7 > ./results/q7_server_${LOSS}.csv
  REC=$(grep -c "rec" ./results/q7_server_${LOSS}.csv)
  echo Server received ${REC} messages with loss ${LOSS}
  echo "${LOSS},${REC}" >> ./results/q7_results.csv
fi

## delete the rule
sudo tc qdisc del dev eth0 root

echo ...DONE

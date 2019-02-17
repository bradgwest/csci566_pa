#!/usr/bin/env bash

#!/usr/bin/env bash

# loss percentage (0.2, 0.4)
LOSS=$1
# whether it is client or not (true, false)
CLIENT=$2
# IPs to send to if server
ClIENT_IP=$3
CLIENT_PORTS=$4

if [[ ! -d  results ]]; then
  mkdir results
fi

if [[ ! -e ./results/q8_results.csv ]]; then
  touch ./results/q8_results.csv
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
  python3 client_udp.py -p 5201 -t scc -q 8 > ./results/q8_client_${LOSS}.csv
  REC=$(grep -c "rec" ./results/q8_client_${LOSS}.csv)
  echo Client received ${REC} with loss ${LOSS}
  echo "${LOSS},${REC}" >> ./results/q8_results.csv
else
  echo running server
  python3 server_udp.py -p 5201 -c ${ClIENT_IP} -cp ${CLIENT_PORTS} -b 32 -r 256 -q 8 -t scc > ./results/q8_server_${LOSS}.csv
  SENT=$(grep -c "send" ./results/q8_server_${LOSS}.csv)
  echo Server sent ${SENT} messages with loss ${LOSS}
  echo "${LOSS},${SENT}" >> ./results/q8_results.csv
fi

## delete the rule
sudo tc qdisc del dev eth0 root

echo ...DONE
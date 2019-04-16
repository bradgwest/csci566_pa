#!/bin/bash
lat=$1
bw=$2
loss=$3
# echo ${lat}
# echo ${bw}
# echo ${loss}
echo "Deleting current net rule.."
sudo tc qdisc del dev eth0 root
echo "Setting up net rule.."
sudo tc qdisc add dev eth0 root handle 1: netem delay ${lat}ms loss ${loss}%
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate ${bw}bit burst 32kbit limit 10000
#!/bin/bash

sudo tc qdisc add dev eth0 root handle 1: netem delay 15ms loss 1%
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 15ms burst 32kbit
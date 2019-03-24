# Guide

## Setup




```bash
bash ec2_setup.sh ec2-3-91-237-177.compute-1.amazonaws.com True
bash ec2_setup.sh ec2-3-90-146-184.compute-1.amazonaws.com True
```


```bash
sudo tc qdisc add dev eth0 root handle 1: netem delay 15ms loss 1%
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 15ms burst 32kbit
```


```bash
# start iperf on the server with `iperf -s`
# make sure the bandwidth is higher than your settings above
iperf -c 3.91.237.177 -u -b15m -t 30
```

Delete the rules:

```bash
sudo tc qdisc del dev eth0 root
```
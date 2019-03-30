# Guide

## Setup

The script set_up.sh takes ip address and type of an intance(kafka or client) as argument. If the type is kafka, send the kafka source zip folder to the instance and extract it. For both type of instance, remote_setup.sh is sent to the instance and execute it to
* 	install iproute2 and iperf3,
*	install java jdk, 
*	install ntp to sync clock,
*	 and install confluent_kafka and required package.
Running set_up.sh is done by the run_experiment.py.

Before starting kafker server, the server.config file needs to editted. Need to uncomment the advertised.listeners and replace your.host.name with kafka instance's public ip.

zookeeper and kafka server need to be manually started by logging into kafka instance and run 
```bash
~/pa4/kafka_2.11-2.1.0/bin/zookeeper-server-start.sh config/zookeeper.properties
~/pa4/kafka_2.11-2.1.0/bin/kafka-server-start.sh config/server.properties
```

To measure network setting, use following script on local machine and AWS instances.

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
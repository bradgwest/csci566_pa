# Experimental Setup

We created two AWS EC2 instances in the same availability zone. We then copied the client and server code to the boxes with:

```bash
scp -r -i ../aws-personal.pem . ubuntu@ec2-3-90-209-49.compute-1.amazonaws.com:~/
```

In order to do this, you must change the permissions on the pem file, `chmod 400 you-pem.pem`. 

We installed the necessary packages, iperf3 and iproute2:

```bash
sudo apt update
sudo apt install iperf3
sudo apt install iproute2
```

We then began to execute the problems.

0. Using iproute2 we created a rule that limited bidirectional latency to 30ms, bandwidth to 10Mbits/sec, and packet loss to 1%:

```bash
# Throttle bandwidth/add delay and loss
sudo tc qdisc add dev eth0 root handle 1: netem delay 30ms loss 1%
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 30ms burst 32kbit
# see current rules
sudo tc qdisc show dev eth0
# delete the rule
sudo tc qdisc del dev eth0 root
```

Using iperf3 and ping, we measured these results and plotted them.

```bash
# iperf3 -- start the server with `iperf -s -u -i 1`
iperf -c 18.208.213.242 -u -b15m -t 30 -o ./results/q0_bw.log
ping -c 60 54.90.251.34 >> ./results/q0_lat_loss.log
```

```
Client connecting to 18.208.213.242, UDP port 5001
Sending 1470 byte datagrams, IPG target: 784.00 us (kalman adjust)
UDP buffer size:  208 KByte (default)
------------------------------------------------------------
[  3] local 172.31.23.104 port 51756 connected with 18.208.213.242 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-30.0 sec  53.6 MBytes  15.0 Mbits/sec
[  3] Sent 38267 datagrams
[  3] Server Report:
[  3]  0.0-30.2 sec  34.8 MBytes  9.65 Mbits/sec   0.000 ms 13437/38267 (0%)
```

Interestingly, our packet loss is 3%, and not 1% as requested. We attempted to reduce packet loss without success.

```
--- 18.208.213.242 ping statistics ---
60 packets transmitted, 58 received, 3% packet loss, time 59127ms
rtt min/avg/max/mdev = 30.481/30.598/31.986/0.307 ms
```

1. UDP does not require a connection time, so there is nothing to measure here.

2. Likewise, for question 2, there is no connection time to measure.

3. For 3, we set rules on bandwidth (10mbit) and latency (30ms).

```bash
# Throttle bandwidth/add delay and loss
sudo tc qdisc add dev eth0 root handle 1: netem delay 30ms
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 30ms burst 32kbit
```

We then used our custom code to send messages from a client to a server in two different manners. We first sent a client to server message. We logged out messages and times, where the messages had unique ids. We progressively increased message payload size, measuring the message delay each time, over a period of 30 seconds.

```bash
# server
python3 server_udp.py -s 172.31.25.152 -p 5201 -t cs
# client
python3 client_udp.py -s 18.208.213.242 -p 5201 -b 1 -d 5 -t cs
``` 

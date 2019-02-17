# Experimental Setup

We created two AWS EC2 instances in the same availability zone. We then copied the client and server code to the boxes with:

```bash
scp -i ../aws-personal.pem ./*.py ubuntu@ec2-3-90-209-49.compute-1.amazonaws.com:~/
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

We then used our code to send messages from a client to a server in two different manners. We first sent a client to server message. We logged out messages and times, where the messages had unique ids. We progressively increased message payload size, measuring the message delay each time, over a period of 30 seconds.

```bash
# server
python3 server_udp.py -s 172.31.25.152 -p 5201 -t cs >> ./results/q3_server.csv
# client
python3 client_udp.py -s 18.208.213.242 -p 5201 -b 1 -t cs >> ./results/q3_client.csv
``` 

We wrote a simple csv parsing script to parse the logs and get the send and receive times, calculating the min, max and average delay. Some messages were lost, in which case the time it took for messages to reach the client was proportional to the timeout we set, which was 5 seconds.

4. For question 4, it would have been nice to implement multicast, but unfortunately AWS does not support that. We could do a multithreaded program, but programming in python with sockets is generally not thread safe. Plus, since we are only concerned with uni-directional delay, it's simple enough to just broadcast in a loop to the necessary clients. This is the benefit of UDP, that it does not involve opening more than one socket. Our delay is just the delay for looping through the clients, plus the individual message delay.

```bash
sudo tc qdisc add dev eth0 root handle 1: netem delay 30ms
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 30ms burst 32kbit
```

```bash
# server
python3 server_udp.py -p 5201 -c 52.207.230.200,34.224.7.137 -cp 5201,5201 -b 32 -r 1 -t scc > ./results/q4_server_2clients.csv
# client
python3 client_udp.py -p 5201 -t scc > ./results/q4_client_2clients_a.csv
```

5 and 6. Because UDP is connectionless, there is not a way to define sequence number or packet loss. If you are implementing UDP, it is assumed your application can cope with packet loss. For this reason, adding packet loss to the communication has no bearing on delay, because the packets will not be resent. It is generally frowned upon to attempt to determine which packets were lost since if this is of concern to you, UDP is likely not the best choice. So, these questions are not relevant to UDP. We have used our results from question 3.

7 and 8. Despite not caring about which packets are lost, we can design an experiment to determine the packets that were lost. We can simply send a ton of messages from the client or server, logging which ones were received, and then determine which ones were received by the server or client, respectively. We did this. The programs are nearly identical to questions 3 and 4, only we just output a count of the messages send and messages received, and run this for a certain duration.

```bash
sudo tc qdisc add dev eth0 root netem loss 0.2%
```

9. For this experiment we switched to using a local machine and one AWS EC2 instance, in order to use Wireshark to measure packet size.

10. For question 10, we adapted our code for question 3 to simple send messages via a certain rate rather than sending a set number of messages and varying the size of the messsage.

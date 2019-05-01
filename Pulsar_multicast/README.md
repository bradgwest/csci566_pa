# Multicasting with Pulsar

To accomplish muticasting with pulsar, we utilize the message routing mechanism supported by pulsar functions. When pulsar function receives messages from an input topic, it can publish messages to one or more output topics. 

First we download the pulsar's binary from the offcial website and unzip it. We navigate to the pulsar directory and move the python scripts to the director. Then we run 
```bash
bin/pulsar standalone
```
to start pulsar in standlone mode.

Then we start pulsar functions by calling

```bash
bin/pulsar-admin functions localrun --py myfunc.py --className myfunc.RoutingFunction --inputs persistent://public/default/my-topic
  --output persistent://public/default/topic1
```

We have the produce.py to produce messages to my-topic, the pulsar function RoutingFunction will receive the message, and publish it to topic1 and topic2. We have two terminals running consume.py to consume messages from topic1 and topic2

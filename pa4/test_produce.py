from confluent_kafka import Producer, Consumer, KafkaError
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.value()))
p = Producer({'bootstrap.servers':'54.201.231.207:9092'})
p.produce("mytopic",value="hello",callback=acked)
p.flush()
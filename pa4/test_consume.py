from confluent_kafka import Producer, Consumer, KafkaError
settings = {
    'bootstrap.servers': '54.201.231.207:9092',
    'group.id': 'mygroup',
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}

c = Consumer(settings)

c.subscribe(["mytopic"])
while True:
	msg=c.poll()
	if msg is None:
		continue
	else:
		print(msg.value())
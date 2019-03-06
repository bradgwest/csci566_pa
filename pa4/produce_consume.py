from confluent_kafka import Producer,Consumer, KafkaError
def consume():
	c = Consumer({'bootstrap.servers':'localhost:9092',
				  'group.id':'mygroup',
				  'client.id':'client-1',
				  'enable.auto.commit':True,
				  'session.timeout.ms':6000,
				  'default.topic.config':{'auto.offset.reset':'smallest'}
				  })
	c.subscribe(['mytopic'])
	msg = c.poll(0.1)
	print(msg.value())

def produce():
	p = Producer({'bootstrap.servers':'localhost:9092'})
	p.produce('mytopic',key='hello',value = 'world')

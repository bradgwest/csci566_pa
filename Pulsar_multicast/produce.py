import pulsar
client = pulsar.Client('pulsar://localhost:6650')

producer = client.create_producer('my-topic')

for i in range(5):
	producer.send(('Counter-%d' % i).encode('utf-8'))

client.close()
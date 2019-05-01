import sys
import pulsar

topic = sys.argv[1]
client = pulsar.Client('pulsar://localhost:6650')
consumer = client.subscribe(topic, 'my-subscription')

while True:
    msg = consumer.receive()
    try:
        print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)
    except:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)

client.close()
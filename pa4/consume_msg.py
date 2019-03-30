from confluent_kafka import Consumer, KafkaError
import logging
import time
from prod_msg import *

kafka_ip = sys.argv[1]
topic = sys.argv[2]
message_forwarding = sys.argv[3]
forwarding_topic = sys.argv[4]

settings = {
    'bootstrap.servers': kafka_ip+':9092',
    'group.id': 'mygroup',
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}

c = Consumer(settings)

c.subscribe([topic])

try:
    while True:
        msg = c.poll()
        if msg is None:
            continue
        elif not msg.error():
            logging.basicConfig(level=logging.DEBUG, filename=log_name,filemode='w')
            logging.info("Start running experiment for question 3>>>>>>>>>>")
            logging.basicConfig(filemode='a')
            # print('Received message: {0}'.format(msg.value()))
            if(message_forwarding = 'True'):
                produce_from_local(kafka_ip,forwarding_topic,[msg.value()])
        # elif msg.error().code() == KafkaError._PARTITION_EOF:
        #     print('End of partition reached {0}/{1}'
        #           .format(msg.topic(), msg.partition()))
        else:
            print('Error occured: {0}'.format(msg.error().str()))

except KeyboardInterrupt:
    pass

finally:
    c.close()
from confluent_kafka import Consumer, KafkaError
import logging
import time
from prod_msg import *
from aux_func import *
from confluent_kafka import Producer, Consumer, KafkaError

kafka_ip = get_kafka_ip()
topic = sys.argv[1]
log_name = sys.argv[2]
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

logging.basicConfig(level=logging.DEBUG, filename=log_name,filemode='w')
logging.info("Start Receiving Message >>>>>>>>>>")
logging.basicConfig(filemode='a')
try:
    while True:
        msg = c.poll()
        if msg is None:
            continue
        elif not msg.error():
            logging.info("Receive message: {} from topic: {} at time: {}".format(msg.value(),topic,time.time()))
            if(message_forwarding = 'True'):
                produce_wo_delay(kafka_ip,forwarding_topic,[msg.value()])
        # elif msg.error().code() == KafkaError._PARTITION_EOF:
        #     print('End of partition reached {0}/{1}'
        #           .format(msg.topic(), msg.partition()))
        else:
            print('Error occured: {0}'.format(msg.error().str()))

except KeyboardInterrupt:
    pass

finally:
    c.close()
from confluent_kafka import Consumer, KafkaError
import logging
import time
from prod_msg import *
from aux_func import *
from confluent_kafka import Producer, Consumer, KafkaError
import sys
kafka_ip = get_kafka_ip()
topic = sys.argv[1]
log_name = sys.argv[2]
message_forwarding = sys.argv[3]
forwarding_topic = sys.argv[4]

def write_to_file(filename,content):
    with open(filename,'w') as file:
        file.write(content+'\n')

def append_to_file(filename,content):
    with open(filename,'a') as file:
        file.write(content+'\n')

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


# logging.basicConfig(level=logging.DEBUG, filename=log_name,filemode='w')
# logging.info("Start Receiving Message >>>>>>>>>>")
# logging.basicConfig(filemode='a')
write_to_file(log_name,'Start Receiving Message >>>>>>')
p = Producer({'bootstrap.servers': kafka_ip+':9092'})

try:
    while True:
        msg = c.poll()
        if msg is None:
            continue
        elif not msg.error():
            consume_time = time.time()
            print("Receive message: (key={} msg size={}) from topic: {} at time: {}".format(msg.key(),len(msg.value()),topic,consume_time))
            append_to_file(log_name,"Receive message: (key={} msg size={}) from topic: {} at time: {}".format(msg.key(),len(msg.value()),topic,consume_time))
            if(message_forwarding == 'True'):
                produce_msg(p,forwarding_topic,msg.key(),msg.value(),log_name)
        # elif msg.error().code() == KafkaError._PARTITION_EOF:
        #     print('End of partition reached {0}/{1}'
        #           .format(msg.topic(), msg.partition()))
        else:
            append_to_file(log_name,'Error occured: {0}'.format(msg.error().str()))
            print("Consumption error!!")
            # logging.info('Consumption ERROR!!!')

except KeyboardInterrupt:
    pass

finally:
    c.close()
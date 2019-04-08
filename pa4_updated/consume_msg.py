from confluent_kafka import Consumer, KafkaError
import logging
import time
from aux_func import *
from confluent_kafka import Producer, Consumer, KafkaError
import sys
kafka_ip = get_kafka_ip()
topic = sys.argv[1]
log_name = sys.argv[2]
message_forwarding = sys.argv[3]
forwarding_topic = sys.argv[4]
group_id = sys.argv[5]

def write_to_file(filename,content):
    with open(filename,'w') as file:
        file.write(content+'\n')

def append_to_file(filename,content):
    with open(filename,'a') as file:
        file.write(content+'\n')

settings = {
    'bootstrap.servers': kafka_ip+':9092',
    'group.id': group_id,
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}

c = Consumer(settings)

c.subscribe([topic])

# write_to_file(log_name,'Start Receiving Message >>>>>>')
write_to_file(log_name,'')
p = Producer({'bootstrap.servers':kafka_ip+':9092',
                  'message.max.bytes':'1100000'})

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
                # produce_msg(p,forwarding_topic,msg.key(),msg.value(),log_name)
                p.produce(forwarding_topic,key=msg.key(),value=msg.value())
                p.flush()
                ts = str(time.time())
                append_to_file(log_name,"Produce message:(key={} msg_size={}) to topic: {} at time: {}".format(msg.key(),len(msg),forwarding_topic,ts))
        else:
            append_to_file(log_name,'Error occured: {0}'.format(msg.error().str()))
            print("Consumption error!!")
            # logging.info('Consumption ERROR!!!')

except KeyboardInterrupt:
    pass

finally:
    c.close()
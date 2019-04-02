from confluent_kafka import Producer
import logging
import time
from aux_func import *
# p = Producer({'bootstrap.servers': 'localhost:9092'})
# p.produce('mytopic', key='hello', value='world1')
# p.produce('mytopic', key='hello', value='world2')
# p.produce('mytopic', key='hello', value='world3')
# p.produce('mytopic', key='hello', value='world4')
# p.produce('mytopic', key='hello', value='world5')
# p.produce('mytopic', key='hello', value='world6')


# p.flush(30)

def write_to_file(filename,content):
    with open(filename,'w') as file:
        file.write(content+'\n')

def append_to_file(filename,content):
    with open(filename,'a') as file:
        file.write(content+'\n')
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
        append_to_file('error.log',"Failed to deliver message: {}: {}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: key = {} size = {}".format(msg.key(),len(msg.value())))

def produce_msg(producer,topic,key,msg,logname):
    producer.produce(topic,key=key,value=msg)
    producer.flush()
    append_to_file(logname,"produce message:(key={} msg size={}) to topic: {} at time: {}".format(key,len(msg),topic,time.time()))
    print("produce message:(key={} msg size={}) to topic: {} at time: {}".format(key,len(msg),topic,time.time()))

# def produce_wo_delay(ip,topic, msgs):
#     p = Producer({'bootstrap.servers': ip+':9092'})

#     try: 
#         for msg in msgs:
#             # logging.basicConfig(level=logging.DEBUG, filename='q3.log',filemode='a')
#             msg_key = str(time.time())
#             p.produce(topic,key=msg_key,value=msg, callback=acked)
#             p.flush()
#             logging.info("produce message:(key={} value={}) to topic: {} at time: {}".format(msg_key,msg,topic,time.time()))

#     except KeyboardInterrupt:
#         pass

# def produce_w_delay(topic,msg,delay):
#     try: 
#         for i in range(50):
#             # logging.basicConfig(level=logging.DEBUG, filename='q3.log',filemode='a')
#             msg_key = str(time.time())
#             p.produce(topic, key=msg_key,value=msg, callback=acked)
#             p.flush()
#             logging.info("produce message: (key={} value={})  to topic: {} at time: {}".format(msg_key,msg,topic,time.time()))
#             time.sleep(delay)
#     except KeyboardInterrupt:
#         pass
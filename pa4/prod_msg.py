from confluent_kafka import Producer
import logging
import time
# p = Producer({'bootstrap.servers': 'localhost:9092'})
# p.produce('mytopic', key='hello', value='world1')
# p.produce('mytopic', key='hello', value='world2')
# p.produce('mytopic', key='hello', value='world3')
# p.produce('mytopic', key='hello', value='world4')
# p.produce('mytopic', key='hello', value='world5')
# p.produce('mytopic', key='hello', value='world6')


# p.flush(30)


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.value()))

def produce_wo_delay(ip,topic, msgs):
    p = Producer({'bootstrap.servers': ip+':9092'})

    try: 
        for msg in msgs:
            # logging.basicConfig(level=logging.DEBUG, filename='q3.log',filemode='a')
            p.produce(topic, msg, callback=acked)
            p.flush()
            logging.info("produce message: {} to topic: {} at time: {}".format(msg.value(),topic,time.time()))

    except KeyboardInterrupt:
        pass

def produce_w_delay(topic,msg,delay):
    try: 
        for i in range(50):
            # logging.basicConfig(level=logging.DEBUG, filename='q3.log',filemode='a')
            p.produce(topic, msg, callback=acked)
            p.flush()
            logging.info("produce message: {} to topic: {} at time: {}".format(msg.value(),topic,time.time()))
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
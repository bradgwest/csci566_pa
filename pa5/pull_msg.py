import time
from aux_func import *
from pymongo import MongoClient
import sys
mongo_ip = get_mongo_ip()
log_name = sys.argv[1]
receiving_collection = sys.argv[2]
message_forwarding = sys.argv[3]
forwarding_collection = sys.argv[4]
# group_id = sys.argv[5]


client = MongoClient(mongo_ip,27017)
client.pa5[receiving_collection].delete_many({})
client.pa5[forwarding_collection].delete_many({})
counter = 0
write_to_file(log_name,'')
try:
    while True:

        msg = client.pa5[receiving_collection].find_one({'counter':counter})

        if(msg==None):
            continue
        else:
            ts= str(time.time())
            print("Counter is :{}, msg size is :{}".format(str(counter),len(msg['value'])))
            append_to_file(log_name,"Receive message: (counter={},msg_size={}),time: {}".format(str(counter),len(msg['value']),ts))
            counter+=1
            if message_forwarding == 'True':
                client.pa5[forwarding_collection].insert_one({'counter':counter-1,'value':msg['value']})
                print("Forwarding message with counter: {} and msg size {}".format(str(counter-1),len(msg['value'])))
                ts = str(time.time())
                append_to_file(log_name,"Forwarding message: (counter={},msg size={}),time: {}".format(str(counter-1),len(msg['value']),ts))



        # msg = c.poll()
        # if msg is None:
        #     continue
        # elif not msg.error():
        #     consume_time = time.time()
        #     print("Receive message: (key={} msg size={}) from topic: {} at time: {}".format(msg.key(),len(msg.value()),topic,consume_time))
        #     append_to_file(log_name,"Receive message: (key={} msg size={}) from topic: {} at time: {}".format(msg.key(),len(msg.value()),topic,consume_time))
        #     if(message_forwarding == 'True'):
        #         # produce_msg(p,forwarding_topic,msg.key(),msg.value(),log_name)
        #         p.produce(forwarding_topic,key=msg.key(),value=msg.value())
        #         p.flush()
        #         ts = str(time.time())
        #         append_to_file(log_name,"Produce message:(key={} msg_size={}) to topic: {} at time: {}".format(msg.key(),len(msg),forwarding_topic,ts))
        # else:
        #     append_to_file(log_name,'Error occured: {0}'.format(msg.error().str()))
        #     print("Consumption error!!")
        #     # logging.info('Consumption ERROR!!!')

except KeyboardInterrupt:
    pass

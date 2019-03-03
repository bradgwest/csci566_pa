"""
Client functionality
"""

import logging
import string
import sys
import time
import threading
import uuid

import boto3
import botocore.exceptions

import messages

# TODO Catch non-200 responses

LOG_LEVEL = messages.LOG_LEVEL


def send_messages(client, send_queue, num_messages, sizes, rate):
    for size in sizes:
        for r in rate:
            for let in string.ascii_letters[:num_messages]:
                response = client.send_message(
                    QueueUrl=send_queue,
                    MessageAttributes={},
                    MessageBody=int(size)*let,
                    MessageGroupId='0',
                    MessageDeduplicationId=str(uuid.uuid4())
                )
                logging.log(LOG_LEVEL, '{thread},{action},{time},{message_id},{size},{rate}'.format(
                    thread='',
                    action='send',
                    time=time.time(),
                    message_id=response["MessageId"],
                    size=size,
                    rate=r
                ))
            # after each message, wait if specified
            time.sleep(messages.rate_to_sec(int(r)))
    # Send instructions to exit
    for _ in range(3):
        client.send_message(
            QueueUrl=send_queue,
            MessageAttributes={
                'exit': {
                    'DataType': 'Number',
                    'StringValue': '1'
                }
            },
            MessageBody='EXIT',
            MessageGroupId='0',
            MessageDeduplicationId=str(uuid.uuid4())
        )
    return


def receive_messages(client, receive_queue, send_queue=None, delete_queue=None,
                     thread_id=0):
    count_messages_received = 0
    while True:
        response = client.receive_message(
            QueueUrl=receive_queue,
            MaxNumberOfMessages=1,
            VisibilityTimeout=30,
            MessageAttributeNames=['All']
        )
        if not response.get('Messages'):
            continue
        for message in response['Messages']:
            message_attributes = message.get('MessageAttributes')
            should_exit = message_attributes and message_attributes.get('exit')
            if send_queue:
                # send it to the send queue to pick off
                message_attributes['message_id'] = {
                    'StringValue': message['MessageId'],
                    'DataType': 'String'
                }
                _ = client.send_message(
                    QueueUrl=send_queue,
                    MessageAttributes=message_attributes,
                    MessageBody=message['Body'],
                    MessageGroupId='0',
                    MessageDeduplicationId=str(uuid.uuid4())
                )
                if should_exit:
                    return
            else:
                if message_attributes.get('message_id'):
                    message_id = message_attributes.get('message_id')['StringValue']
                else:
                    message_id = message['MessageId']
                logging.log(LOG_LEVEL, '{thread},{action},{time},{message_id}'.format(
                    thread=thread_id,
                    action='receive',
                    time=time.time(),
                    message_id=message_id
                ))
                if delete_queue:
                    # Send message to the delete queue
                    client.send_message(
                        QueueUrl=delete_queue,
                        MessageAttributes={
                            # Queue to delete message from
                            'deleteQueue': {
                                'DataType': 'String',
                                'StringValue': receive_queue
                            },
                            'receiptHandle': {
                                'DataType': 'String',
                                'StringValue': message['ReceiptHandle']
                            }
                        }
                    )
                else:
                    # delete the message because we're the only client
                    try:
                        _ = client.delete_message(
                            QueueUrl=receive_queue,
                            ReceiptHandle=message['ReceiptHandle']
                        )
                    except botocore.exceptions.ClientError:
                        pass
                count_messages_received += 1
                # Due to visibility timeout constraints, messages cannot be deleted with a timeout of zero
                if count_messages_received > 52:
                    logging.warning("Exiting without observing exit message")
                    return


def perform_experiment(device, latency, loss, bandwidth, log_file, send_queue,
                       receive_queue, delete_queue, num_messages, size, rate,
                       comm_type, sender, num_clients, server):
    messages.setup_log(log_file, 'client_logger')
    # setup networking
    messages.set_tc(device, latency, loss, bandwidth)

    # setup client and run the threads
    threads = []
    sqs = boto3.client('sqs')
    if comm_type == 'csc':
        # create threads
        if server:
            receive_messages(sqs,
                             receive_queue=send_queue,
                             send_queue=receive_queue,
                             delete_queue=None,
                             thread_id=0)
        else:
            sender = threading.Thread(target=send_messages,
                                      kwargs=dict(client=sqs,
                                                  send_queue=send_queue,
                                                  num_messages=num_messages,
                                                  sizes=size.split(','),
                                                  rate=rate.split(',')))
            receiver = threading.Thread(target=receive_messages,
                                        kwargs=dict(client=sqs,
                                                    receive_queue=receive_queue))
            threads = [sender, receiver]
    elif comm_type == 'scc':
        if sender:
            send_messages(sqs,
                          send_queue=send_queue,
                          num_messages=num_messages,
                          sizes=size.split(','),
                          rate=rate.split(','))
        else:
            rec_args = dict(client=sqs,
                            receive_queue=receive_queue,
                            delete_queue=delete_queue,
                            thread_id=0)
            for i in range(num_clients):
                rec_args['thread_id'] = i
                threads.append(threading.Thread(target=receive_messages,
                                                kwargs=rec_args))

    if threads:
        # Start the threads
        for t in threads:
            t.start()
        # Wait for threads to finish before proceeding
        for t in threads:
            t.join()

    # send message to delete queue to finish process
    if comm_type == 'scc' and not sender:
        sqs.send_message(
            QueueUrl=delete_queue,
            MessageAttributes={
                'exit': {
                    'DataType': 'Number',
                    'StringValue': '1'
                }
            },
            MessageBody='EXIT',
            MessageGroupId='0',
            MessageDeduplicationId=str(uuid.uuid4())
        )

    # purge queue messages
    logging.info("Purging queues")
    for q in [receive_queue, send_queue, delete_queue]:
        try:
            _ = sqs.purge_queue(QueueUrl=q)
        except Exception:
            pass

    # delete networking rules
    messages.delete_tc(device)

    return "DONE"


def main():
    args = messages.parse_arguments(sys.argv[1:])
    perform_experiment(args.device, args.latency, args.loss, args.bandwidth,
                       args.log_file, args.send_queue, args.receive_queue,
                       args.delete_queue, args.num_messages, args.size,
                       args.rate, args.comm_type, args.sender, args.num_clients)


if __name__ == "__main__":
    main()

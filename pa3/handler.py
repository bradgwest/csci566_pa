"""
Client functionality
"""

import logging
import string
import sys
import time
import threading

import boto3

import messages


def send_messages(client, send_queue, num_messages, sizes, rate):
    for size in sizes:
        for r in rate:
            for let in string.ascii_letters[:num_messages]:
                client.send_message(
                    QueueUrl=send_queue,
                    MessageAttributes=messages.create_message_attributes(size, r),
                    MessageBody=size*let
                )
                logging.info('{action},{time},{message},{size},{rate}'.format(
                    action='send', time=time.time(), message=let, size=size,
                    rate=r
                ))
            # after each message, wait if specified
            time.sleep(messages.rate_to_sec(r))
    # Send instructions to exit
    for _ in range(3):
        client.send_message(
            QueueUrl=send_queue,
            MessageAttributes={
                'exit': {
                    'Datatype': 'Number',
                    'StringValue': '1'
                }
            },
            MessageBody='EXIT'
        )


def receive_messages(client, receive_queue, delete_queue=None, thread_id=0):
    while True:
        response = client.receive_messages(
            QueueUrl=receive_queue,
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            MessageAttributeNames=['All']
        )
        for message in response['Messages']:
            message_attributes = message['MessageAttributes']
            should_exit = message_attributes.get('exit')
            if should_exit:
                return
            logging.info('{thread},{action},{time},{message},{size},{rate}'.format(
                thread=thread_id,
                action='receive',
                time=time.time(),
                message=message['Body'][0],
                size=message_attributes.get('size'),
                rate=message_attributes.get('rate')
            ))
            if delete_queue:
                # Send message to the delete queue
                client.send_message(
                    QueueUrl=delete_queue,
                    MessageAttributes={
                        # Queue to delete message from
                        'deleteQueue': {
                            'Datatype': 'String',
                            'StringValue': receive_queue
                        },
                        'receiptHandle': {
                            'Datatype': 'String',
                            'StringValue': message['ReceiptHandle']
                        }
                    }
                )


def perform_experiment(device, latency, loss, bandwidth, log_file, send_queue,
                       receive_queue, delete_queue, num_messages, size, rate,
                       comm_type, sender, num_clients):
    _ = messages.setup_log(log_file, 'client_logger')
        # setup networking
    messages.set_tc(device, latency, loss, bandwidth)

    # setup client and run the threads
    threads = []
    sqs = boto3.client('sqs')
    if comm_type == 'csc':
        # create threads
        sender = threading.Thread(target=send_messages,
                                  kwargs=dict(client=sqs,
                                              send_queue=send_queue,
                                              num_messages=num_messages,
                                              bytes=size.split(','),
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
                threads.append(threading.Thread(target=receive_messages, kwargs=rec_args))

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
                    'Datatype': 'Number',
                    'StringValue': '1'
                }
            },
            MessageBody='EXIT'
        )

    # purge queue messages
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

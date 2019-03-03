"""
Remotely invokes an experiment
"""

import argparse
import logging
import os
import subprocess

import boto3


QUEUE_ATTRIBUTES = {
    'ReceiveMessageWaitTimeSeconds': '1',
    'FifoQueue': 'true',
    'VisibilityTimeout': '720'
}

sizes = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072]
losses = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]


def setup_queues(sqs_client):
    # Create queues with long polling enabled
    queue_names = ('send_queue.fifo', 'receive_queue.fifo', 'delete_queue.fifo')
    sqs_queues = []
    for name in queue_names:
        response = sqs_client.create_queue(
            QueueName=name,
            Attributes=QUEUE_ATTRIBUTES
        )
        sqs_queues.append(response['QueueUrl'])
    # send_queue, receive_queue, delete_queue
    return sqs_queues


def copy_logs(instance, local_directory, remote_file):
    remote_loc = "ubuntu@{}:{}".format(instance, remote_file)
    logging.info("copying logs from {} to {}".format(remote_loc, remote_file))
    if not os.path.exists(local_directory):
        os.mkdir(local_directory)
    args = ["scp", remote_loc, local_directory]
    subprocess.run(args)


def setup_and_run_experiment(question, ec2_client_dns, ec2_server_dns=None,
                             size=0, loss=0):
    sqs = boto3.client("sqs")
    sqs_queues = setup_queues(sqs)
    logging.info("Created queues:")
    for q in sqs_queues:
        logging.info(q)
    if question == 3:
        logging.info("Running question 3")
        logfile_client = "log/q3_client_{}.log".format(sizes[size])
        logfile_server = "log/q3_server_{}.log".format(sizes[size])
        logfiles = (logfile_client, logfile_server)
        py_server_cmd = "python3 handler.py --send-queue {} " \
                        "--receive-queue {} --log-file {} --comm-type csc " \
                        "--server ".format(sqs_queues[0], sqs_queues[1], logfiles[1])
        py_client_cmd = "python3 handler.py --send-queue {} " \
                        "--receive-queue {} " \
                        "--size {} " \
                        "--rate 0 --log-file {} " \
                        "--comm-type csc " \
                        "--delay 0".format(sqs_queues[0], sqs_queues[1], sizes[size], logfiles[0])
        print("Run on server:")
        print(py_server_cmd)
        print("Run on client:")
        print(py_client_cmd)
        a = input("Copy Logs? [y/n]")
        if a != "y":
            print("Quitting")
            return
        for s, l in zip((ec2_client_dns, ec2_server_dns), logfiles):
            copy_logs(s, local_directory="log/q3/",
                      remote_file="~/{}".format(l))
    elif question == 5:
        logging.info("Running question 5")
        logfile_client = "log/q5_client_{}.log".format(losses[loss])
        logfile_server = "log/q5_server_{}.log".format(losses[loss])
        logfiles = (logfile_client, logfile_server)
        py_server_cmd = "python3 handler.py --send-queue {} " \
                        "--receive-queue {} --log-file {} --comm-type csc " \
                        "--server " \
                        "--loss {}".format(sqs_queues[0], sqs_queues[1], logfiles[1], losses[loss])
        py_client_cmd = "python3 handler.py --send-queue {} " \
                        "--receive-queue {} " \
                        "--size 32 " \
                        "--rate 0 --log-file {} " \
                        "--comm-type csc --loss {} " \
                        "--delay 0".format(sqs_queues[0], sqs_queues[1], logfiles[0], losses[loss])
        print("Run on server:")
        print(py_server_cmd)
        print("Run on client:")
        print(py_client_cmd)
        a = input("Copy Logs? [y/n]")
        if a != "y":
            print("Quitting")
            return
        for s, l in zip((ec2_client_dns, ec2_server_dns), logfiles):
            copy_logs(s, local_directory="log/q5/",
                      remote_file="~/{}".format(l))
    else:
        print("Question {} not implemented".format(question))
        return

    # delete the queues
    for q in sqs_queues:
         _ = sqs.delete_queue(QueueUrl=q)


def main():
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('question', help='question number', type=int)
    parser.add_argument('-c', '--client', help='public dns of ec2 client instance')
    parser.add_argument('-s', '--server', help='public dns of ec2 server instance')
    parser.add_argument('--size', type=int)
    parser.add_argument('--loss', type=int)
    args = parser.parse_args()
    setup_and_run_experiment(args.question, args.client, args.server, args.size, args.loss)


if __name__ == '__main__':
    main()

"""
Remotely invokes an experiment
"""

import argparse
import os
import subprocess

import boto3


QUEUE_ATTRIBUTES = {
    'ReceiveMessageWaitTimeSeconds': '1',
    'FifoQueue': 'true'
}


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
    if not os.path.exists(local_directory):
        os.mkdir(local_directory)
    args = ["scp", "ubuntu@{}:{}".format(instance, remote_file), local_directory]
    subprocess.run(args)


def setup_and_run_experiment(question, ec2_client_dns, ec2_server_dns):
    sqs = boto3.client("sqs")
    sqs_queues = setup_queues(sqs)
    if question == 3:
        logfile = "q3.log"
        args_server = ["python3", "handler.py",
                       "--send-queue", sqs_queues[1],
                       "--receive-queue", sqs_queues[0],
                       "--log-file", logfile,
                       "--comm-type", "csc",
                       "--server"]
        completed_process = subprocess.run(args_server, shell=True)
        completed_process.check_returncode()
        args_client = ["python3", "handler.py",
                       "--send-queue", sqs_queues[0],
                       "--receive-queue", sqs_queues[1],
                       "--size", "1,2,4,8,16,32,64,128,...",
                       "--rate", 0,
                       "--log-file", logfile,
                       "--comm-type", "csc"]
        completed_process = subprocess.run(args_client, shell=True)
        completed_process.check_returncode()
        copy_logs(ec2_client_dns, local_directory="log/q3/",
                  remote_file="~/log/{}".format(logfile))
    elif question == 4:
        pass
    else:
        print("Question {} not implemented".format(question))
        return

    # delete the queues
    for q in sqs_queues:
        _ = sqs.delete_queue(QueueUrl=q)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--question', help='question number', type=int, required=True)
    parser.add_argument('--ec2-client-dns', help='public dns of ec2 client instance', required=True)
    parser.add_argument('--ec2-server-dns', help='public dns of ec2 server instance', required=True)
    args = parser.parse_args()
    setup_and_run_experiment(args.question, args.ec2_client_dns,
                             args.ec2_server_dns)


if __name__ == '__main__':
    main()

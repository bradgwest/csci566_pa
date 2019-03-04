"""
Functionality for deleting messages from a queue
"""

import argparse

import boto3
import botocore.exceptions


# MESSAGE_LEDGER has queue urls as keys and dicts as values where that dict has
# receipt handles as keys and counts of clients that have sent
# that handle to the delete queue. When the count equals the number of clients,
# that message is deleted from the queue
MESSAGE_LEDGER = {}


def delete_messages(delete_queue, client_count):
    sqs = boto3.client("sqs")
    while True:
        response = sqs.receive_message(
            QueueUrl=delete_queue,
            MaxNumberOfMessages=10,
            MessageAttributeNames=['All']
        )
        if not response.get('Messages'):
            continue
        for message in response['Messages']:
            message_attributes = message['MessageAttributes']
            should_exit = message_attributes.get('exit')
            queue_to_delete_from_att = message_attributes.get('deleteQueue')
            receipt_handle_att = message_attributes.get('receiptHandle')
            if should_exit:
                return
            elif not (queue_to_delete_from_att or receipt_handle_att):
                continue
            else:
                queue_to_delete_from = queue_to_delete_from_att['StringValue']
                receipt_handle = receipt_handle_att['StringValue']
                if queue_to_delete_from not in MESSAGE_LEDGER or \
                        receipt_handle not in MESSAGE_LEDGER[queue_to_delete_from]:
                    MESSAGE_LEDGER[queue_to_delete_from] = dict(
                        receipt_handle=1
                    )
                elif MESSAGE_LEDGER[queue_to_delete_from] < (client_count - 1):
                    MESSAGE_LEDGER[queue_to_delete_from] += 1
                else:
                    try:
                        _ = sqs.delete_message(
                            QueueUrl=queue_to_delete_from,
                            ReceiptHandle=receipt_handle
                        )
                    except botocore.exceptions.ClientError:
                        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('delete_queue', help='queue to pick messages off of')
    parser.add_argument('client_count', help="number of clients in the system")
    args = parser.parse_args()
    delete_messages(args.delete_queue, args.client_count)


if __name__ == '__main__':
    main()

import boto3

client = boto3.client('sqs')
Qurl = client.get_queue_url(QueueName='testqueue1')
# client.change_message_visibility(
# 	QueueUrl=Qurl['QueueUrl'],
# 	ReceiptHandle='String',
# 	VisibilityTimeout=0)

def send_msg():
	response = client.send_message(
	    QueueUrl=Qurl['QueueUrl'],
	    MessageAttributes={
	    	'Group':{
	    		'DataType':'String',
	    		'StringValue':'1'
	    	}
	    },
	    MessageBody=(
	        'A brand new message')
	)
def receive_msg():
	response = client.receive_message(
		QueueUrl=Qurl['QueueUrl'],
		MessageAttributeNames=['Group',],
		MaxNumberOfMessages=1)
	# print(response)
	message = response['Messages'][0]
	# print(message)
	receipt_handle = message['ReceiptHandle']
	msg_body = message['Body']
	# att = message['Attributes']
	msg_att = message['MessageAttributes']
	# print(msg_body)
	# print(msg_att['Group']['StringValue'])
	group_id = msg_att['Group']['StringValue']
	# print(message['Body'])

	if(group_id == '1'):
		client.delete_message(
			QueueUrl=Qurl['QueueUrl'],
			ReceiptHandle=receipt_handle
		)

# send_msg()
receive_msg()


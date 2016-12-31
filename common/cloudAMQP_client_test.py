from cloudAMQP_client import CloudAMQPClient


CLOUDAMQP_URL = "amqp://chkyuhrv:Tqk3rIQqJjFE6HAKDwYx9fzVr7GegWvi@sidewinder.rmq.cloudamqp.com/chkyuhrv"
QUEUE_NAME = 'dataFetcherTaskQueue'

# initialize a client
client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

# send message
# client.sendDataFetcherTask({'zpid' : '83154148'})

# receive message
# while True:
#     client.getDataFetcherTask()

# get message count
print client.getQueueSize()

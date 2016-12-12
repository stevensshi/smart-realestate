from cloudAMQP_client import CloudAMQPClient


CLOUDAMQP_URL = "amqp://chkyuhrv:Tqk3rIQqJjFE6HAKDwYx9fzVr7GegWvi@sidewinder.rmq.cloudamqp.com/chkyuhrv"
QUEUE_NAME = 'test_queue'

# initialize a client
client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

# send message
# client.sendDataFetcherTask({'name':'test message'})

# receive message
client.getDataFetcherTask()

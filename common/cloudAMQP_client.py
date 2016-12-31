import json
import pika

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    # Send a message
    def sendDataFetcherTask(self, task):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(task))
        print "[x] Sent task to dataFetcherTaskQueue: %s" % task

    # Receive a message
    def getDataFetcherTask(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            print "[x] Received task from dataFetcherTaskQueue: %s" % body
            self.channel.basic_ack(method_frame.delivery_tag)
            return body
        else:
            print "No message returning"
            return None

    def getQueueSize(self):
        response = self.channel.queue_declare(self.queue_name, passive=True)
        return response.method.message_count

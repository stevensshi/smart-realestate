import pika
import json

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    #send message
    def sendDataFetcherTask(self, task):
        self.channel.basic_publish(exchange='',                                                     routing_key=self.queue_name,
                                   body=json.dumps(task))
        print "[x] Send task to dataFetherTaskQueue: %s" % task

    def getDataFetcherTask(self):
        method_frame,head_frame,body = self.channel.basic_get(self.queue_name)
        if method_frame:
            print "[x] received task from dataFetcherTaskQueue: %s" % body
            return body
        else:
            print "No message returning"
            return None

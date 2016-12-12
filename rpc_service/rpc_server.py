import pyjsonrpc
import os
import sys
import json

from bson.json_util import dumps

# import mongodb path
sys.path.append(os.path.join.dirname(__file__), '..', 'mongodb')

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

PROTERTY_TABLE_NAME = 'properties'

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    # """Test Method"""
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add gets called with %d and %d" % (a, b)
        return a+b

    @pyjsonrpc.rpcmethod
    def searchArea(self, query):
        res = []
        if query.isdigit():
            # TODO: search in DB
            print "postcode"
            db = mongodb_client.getDB()
            res = db[PROPERTY_TABLE_NAME].find({'postcode':query})
            res = json.loads(dumps(res))
        else:
            city = query.split(',')[0].strip()
            state = query.split(',')[1].strip()
            # TODO: search in DB
        return res


http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=(SERVER_HOST, SERVER_PORT),
    RequestHandlerClass=RequestHandler
)

print "Starting Http server..."
print "Listening on %s : %d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()

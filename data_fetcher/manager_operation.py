import logging
import threading


logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) % (message)s')


for t in threading.enumerate():

    

#/usr/bin/python3

from queue import Queue

class Fatman:
    def __init__(self):
        self.name = 'fatman'
        self.transmitter = 'arm'
        self.boards  = { "Asserv": 1302}
        self.semantic = '../semantic_fatman.py'
        self.host = 'fatman'
        self.queue = Queue()

        self.sensor_front = None 
        self.sensor_back = None

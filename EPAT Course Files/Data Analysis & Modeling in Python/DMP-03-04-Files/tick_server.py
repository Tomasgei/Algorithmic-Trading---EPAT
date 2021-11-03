#
# Simple Tick Data Server
#
import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://127.0.0.1:5555')

PRICE = 100.

while True:
    PRICE += random.gauss(0, 1) * 0.5
    msg = f'PRICE {PRICE:.3f}'
    print(msg)
    socket.send_string(msg)
    time.sleep(random.random() * 2)

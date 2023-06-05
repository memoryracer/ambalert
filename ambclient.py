import zmq
import threading
import sys


def zmq_connect(host="tcp://localhost", port=5555):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"{host}:{str(port)}")
    return socket

def zmq_alert_request(socket, message="Das ist ein Test"):
    socket.send_string(message)
    return socket.recv()



socket = zmq_connect(port=5556)

def get_input():
    while True:
        sys.stdout.write("$> ")
        text = input()
        if text == "exit":
            break
        zmq_alert_request(socket=socket, message=text)


get_input()
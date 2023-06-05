import sys
from threading import Thread
from time import sleep
import zmq
import signal
 
from g_python.gextension import Extension
from g_python.hmessage import Direction, HMessage
from g_python.hpacket import HPacket
from g_python import hparsers
from g_python import htools
 
extension_info = {
    "title": "AMB Alerter",
    "description": "Alert when AMB enters room",
    "version": "1.0",
    "author": "memoryracer"
}
 

def visit_and_alert(roomId, message):
    # {out:GetGuestRoom}{i:26926357}{i:1}{i:0}
    # {out:OpenFlatConnection}{i:26926357}{s:""}{i:-1}
    ext.send_to_server(HPacket("OpenFlatConnection", int(roomId), "", -1))
    print(roomId)
    print(message)
    sleep(0.1)
    ext.send_to_server(HPacket("Shout", message, 0))
    sleep(0.1)
    ext.send_to_server(HPacket("Quit"))

ext = Extension(extension_info, sys.argv)   # sys.argv are the commandline arguments, for example ['-p', '9092'] (G-Earth's extensions port)
ext.start()


context = zmq.Context()
socket = context.socket(zmq.REP)
sys.stdout.write("$ port> ")
port = input()
socket.bind(f"tcp://*:{port}")

terminate = False                            

def signal_handling(signum,frame):           
    global terminate                         
    terminate = True                         

signal.signal(signal.SIGINT,signal_handling) 

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    visit_and_alert(26572524, message.decode('utf-8'))

    #  Send reply back to client
    socket.send(message)
    if terminate:                            
        print("SIGINT")              
        break 


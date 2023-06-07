import sys
from threading import Thread
from time import sleep
from datetime import datetime
import zmq
import requests 

from g_python.gextension import Extension
from g_python.hmessage import Direction, HMessage
from g_python.hpacket import HPacket
from g_python import hparsers
from g_python import htools
 
extension_info = {
    "title": "AMB Alert Daemon",
    "description": "Alert when AMB enters room",
    "version": "1.0",
    "author": "memoryracer"
}
 
ext = Extension(extension_info, sys.argv)   # sys.argv are the commandline arguments, for example ['-p', '9092'] (G-Earth's extensions port)
 
 
ambassadors = [
    "LindaGirlAngel",
    "cundero",
    "T0WLY",
    "NedurkTschger",
    "Alduin",
    "Juchuhi"
    "Rosi999",
    "Cybercheck",
    "g00dbye",
    "Pakku",
    "NPLMxAndi",
    "Clepsidra",
    #"warnungvorboti"
]

roomIsSafe = True

def on_remove_user(user):
    try:
        removeUserThread = Thread(target=process_remove_user, args=(user,))
        removeUserThread.daemon = True
        removeUserThread.start()
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
        sys.exit(1)

 
def on_new_users(users):
    try:
        newUsersThread = Thread(target=process_new_users, args=(users,))
        newUsersThread.daemon = True
        newUsersThread.start()
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
        sys.exit(1)


def on_chat(message):
    try:
        chatProcessingThread = Thread(target=process_chat, args=(message.packet,))
        chatProcessingThread.daemon = True
        chatProcessingThread.start()
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
        sys.exit(1)


def process_remove_user(user):
    global roomIsSafe
    print(f"[{datetime.now()}] ({user.entity_type.name}) <{user.name}> hat den Raum verlassen.")
    if (user.name in ambassadors):
        ambCount = 0
        for userId in roomUsers.room_users:
            if (roomUsers.room_users[userId].name in ambassadors):
                ambCount = ambCount + 1
 
        if (ambCount > 0):
            message = f"ACHTUNG: {user.name} ist weg. Es sind immer noch {ambCount} Botschafter im Raum!"
            #ext.send_to_server(HPacket("Shout", message, 0))
            #ext.send_to_server(HPacket("ChangeMotto", ""))
            #ext.send_to_server(HPacket("UpdateFigureData", "M", "hr-891-40.hd-209-1370.sh-290-64.ha-1002-73.lg-285-82.ch-210-73"))
            socket = zmq_connect()
            print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message=message).decode('utf-8')}")
            roomIsSafe = False
            #{out:Shout}{s:"abcadef"}{i:0}
        else: 
            message = f"ENDLICH: {user.name} hat den Raum verlassen! Die Luft ist rein!"
            #ext.send_to_server(HPacket("UpdateFigureData", "M", "hr-891-40.hd-209-1370.sh-290-64.ha-1002-84.lg-285-82.ch-210-84"))
            socket = zmq_connect()
            print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message=message).decode('utf-8')}")
            #ext.send_to_server(HPacket("ChangeMotto", "Die Luft ist rein!"))
            #ext.send_to_server(HPacket("Shout", message, 0))
            roomIsSafe = True
 
 
def process_new_users(users):
    global roomIsSafe
    #print(users)
    for user in users:
        if (user.name in ambassadors):
            message = f"ACHTUNG: {user.name} hat den Raum betreten! Bitte die Regeln beachten!"
            #print(message)
            #ext.send_to_server(HPacket("Shout", message, 0))
            socket = zmq_connect()
            print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message=message).decode('utf-8')}")
            #ext.send_to_server(HPacket("ChangeMotto", ""))
            #ext.send_to_server(HPacket("UpdateFigureData", "M", "hr-891-40.hd-209-1370.sh-290-64.ha-1002-73.lg-285-82.ch-210-73"))
            roomIsSafe = False
        elif user.name == "daydr3amer":
            socket = zmq_connect()
            print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message='ACHTUNG: daydr3amer hat den Raum betreten! Ab jetzt bitte keine Rechtschreibfehler mehr!').decode('utf-8')}")
        elif user.name == "susase":
            socket = zmq_connect()
            print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message='ACHTUNG: susase hat den Raum betreten! Ab jetzt bitte keine frauenfeindlichen Witze mehr!').decode('utf-8')}")
        elif user.name == "habwohlbannups":
            socket = zmq_connect()
            print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message='ACHTUNG: habwohlbannups hat den Raum betreten! Versteckt eure Speedreste!').decode('utf-8')}")
        print(f"[{datetime.now()}] ({user.entity_type.name}) <{user.name}> hat den Raum betreten.")


def process_chat(packet):
    global roomIsSafe
    (userid, msg) = packet.read("is")
    msg = msg.encode('iso-8859-1').decode('utf-8')
    print(f"[{datetime.now()}] ({roomUsers.room_users[userid].entity_type.name}) <{roomUsers.room_users[userid].name}>: {msg}")
    if "luft rein" in msg.lower():
        socket = zmq_connect()
        if roomIsSafe:
            print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message='Ja, die Luft ist rein!').decode('utf-8')}")
        else:
            print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message='Nein, es befinden sich noch Spielverderber im Raum!').decode('utf-8')}")
    elif "wer hat das gras weg" in msg.lower():
        socket = zmq_connect()
        print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message='DerNeger!').decode('utf-8')}")
    elif "wer rammt dir den" in msg.lower():
        socket = zmq_connect()
        print(f"ALERT REQUEST {zmq_alert_request(socket=socket, message='DerNeger!').decode('utf-8')}")
    elif "wetter in" in msg.lower():
        city = msg.split(" ")[-1].replace("?", "").capitalize()
        response = requests.get(f"https://wttr.in/{city}?format=%l:+%C+%t", headers={'Accept-Language': 'de'})
        socket = zmq_connect()
        print(f"WEATHER REQUEST FOR {city} {zmq_alert_request(socket=socket, message=str(response.text)).decode('utf-8')}")



def show_sign():
    global roomIsSafe
    while True:
        sleep(3)
        if not roomIsSafe:
            print("UNSAFE")
            #ext.send_to_server(HPacket("Sign", 12))
            #ext.send_to_server(HPacket("EventLog", "OwnAvatarMenu", "click", "sign", "", 12))
            #ext.send_to_server(HPacket("UpdateFigureData", "M", "lg-270-73.sh-305-73.ch-215-73.wa-2007-0.hd-180-12.hr-100-0.ha-1002-73"))

        else:
            #print("SAFE")
            ext.send_to_server(HPacket("Sign", 15))
            ext.send_to_server(HPacket("EventLog", "OwnAvatarMenu", "click", "sign", "", 15))
        


def zmq_connect(host="tcp://localhost", port=5555):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"{host}:{str(port)}")
    return socket

def zmq_alert_request(socket, message="Das ist ein Test"):
    socket.send_string(message)
    sleep(0.6)
    return socket.recv()



roomUsers = htools.RoomUsers(ext)
roomUsers.on_new_users(on_new_users)
roomUsers.on_remove_user(on_remove_user)

ext.intercept(Direction.TO_CLIENT, on_chat, "Chat")
ext.intercept(Direction.TO_CLIENT, on_chat, "Shout")

try:
    signThread = Thread(target=show_sign)
    signThread.daemon = True
    #signThread.start()
except KeyboardInterrupt:
    print("Ctrl+C pressed...")
    sys.exit(1)

ext.start()
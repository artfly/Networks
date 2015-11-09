import signal
import socket
import struct
import sys
from threading import Thread
import logging

BORN, MSG, DEAD = range(3)
nicknames = []
MSG_FORMAT = '=b'
s = None


def get_input(nick):
    while True:
        content = input()
        if content.split()[0] == "!users":
            print(' '.join(nicknames))
            continue
        full_msg = struct.pack(MSG_FORMAT, MSG) + content.encode("utf-8")
        s.send(full_msg)


def exterminate(signum, frame):
    s.send(struct.pack(MSG_FORMAT, DEAD))
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage : %s <server_ip> <server_port> <nickname>")
        sys.exit(1)
    server_ip, server_port, nickname = sys.argv[1:]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, int(server_port)))
    msg = struct.pack(MSG_FORMAT, BORN) + nickname.encode("utf-8")
    s.send(msg)
    connected = s.recv(1024).decode("utf-8")
    nicknames.extend(connected.split())
    signal.signal(signal.SIGINT, exterminate)
    thread = Thread(target=get_input, args=(nickname,))
    thread.daemon = True
    thread.start()
    while True:
        data = s.recv(1024).decode("utf-8")
        chunks = data.split()
        if data is '':
            print("user with this username is already existing")
            sys.exit(1)
        elif chunks[0] == "!user":
            nicknames.append(chunks[1])
            print("user %s connected" % chunks[1])
        elif chunks[0] == "!quit":
        	nicknames.remove(chunks[1])
        	print("user %s left chat" % chunks[1])
        else:
            print(data)

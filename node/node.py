import sys
import socket
import struct
import signal
from threading import Thread

__author__ = 'arty'

CHILD, MSG, QUIT, PARENT = range(4)
MSG_FORMAT = '=bBBBBH'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
parent = None
me = ()
children = []


def compose_msg(msg_type: int, addr: tuple) -> bytes:
    ip = [int(x) for x in addr[0].split(".")]
    msg = struct.pack(MSG_FORMAT, msg_type, ip[0], ip[1], ip[2], ip[3], int(addr[1]))
    return msg


def get_input():
    print(me)
    while True:
        msg = input()
        full_msg = compose_msg(MSG, me) + msg.encode("utf-8")
        for addr in children + [parent]:
            if addr is not None:
                sock.sendto(full_msg, addr)


def exterminate(signum, frame):
    global parent
    print(parent)
    if parent is not None:
        sock.sendto(compose_msg(QUIT, me), parent)
    if parent is None and len(children) > 1:
        parent = children[0]
        del children[0]
    for child in children:
        sock.sendto(compose_msg(PARENT, parent), child)
    sys.exit(0)


def main():
    global me
    global parent
    argc = len(sys.argv)
    if argc != 2 and argc != 4:
        print(sys.argv[0] + " [parent_ip] [parent_port] port")
        sys.exit(1)
    port = int(sys.argv[-1])
    sock.bind(('', port))
    me = (socket.gethostbyname(socket.gethostname()), sock.getsockname()[1])
    print(me)
    signal.signal(signal.SIGINT, exterminate)
    thread = Thread(target=get_input)
    thread.daemon = True
    thread.start()
    if len(sys.argv) == 4:
        parent = (sys.argv[1], int(sys.argv[2]))
        sock.sendto(compose_msg(CHILD, me), parent)
    while True:
        msg, recv_from = sock.recvfrom(1024)
        data = struct.unpack(MSG_FORMAT, msg[:7])
        msg_type = data[0]
        print(msg_type)
        ip = '{}.{}.{}.{}'.format(data[1], data[2], data[3], data[4])
        port = data[5]
        if msg_type == CHILD:
            children.append((ip, port))
            print("NEW CHILD: " + ip + ":" + str(port))

        if msg_type == MSG:
            print("Received new message from " + ip + ":" + str(port))
            content = msg[7:]
            msg = compose_msg(MSG, me) + content
            for addr in children + [parent]:
                if addr != (ip, port) and addr is not None:
                    sock.sendto(msg, addr)
            print(content.decode("utf-8"))

        if msg_type == QUIT:
            print("Received quit message from " + ip + ":" + str(port))
            addr = (ip, port)
            if addr in children:
                children.remove(addr)
            if addr == parent:
                parent = None

        if msg_type == PARENT:
            parent = (ip, port)
            sock.sendto(compose_msg(CHILD, me), parent)


if __name__ == "__main__":
    main()
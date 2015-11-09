import socket
import struct
import sys
import threading
import logging


BORN, MSG, DEAD = range(3)
users = {}
MSG_FORMAT = '=b'


def client_thread(conn):
    my_client = ''
    while True:
        msg = conn.recv(1024)
        msg_type = struct.unpack(MSG_FORMAT, msg[:1])[0]
        if msg_type == BORN:
            my_client = msg[1:].decode("utf-8")
            connected = ' '
            if len(users) != 0:
                connected = ' '.join(list(users))
            if my_client in users:
                conn.close()
                return
            users[my_client] = conn
            print("user %s connected" % my_client)
            for user in list(users.values()):
                if user != conn:
                    user.send(("!user %s" % my_client).encode("utf-8"))
            conn.send(connected.encode("utf-8"))
        if msg_type == MSG:
            content = msg[1:].decode("utf-8")
            to = content.split()[0][1:]
            content = my_client + ":" + content
            if to in users:
                users[to].send(content.encode("utf-8"))													# TODO : from
            else:
                for user in list(users.values()):
                    if user != conn:
                        user.send(content.encode("utf-8"))
        if msg_type == DEAD:
            nick = list(users.keys())[list(users.values()).index(conn)]
            users.pop(nick)
            for user in list(users.values()):
                user.send(("!quit %s" % nick).encode("utf-8"))
                print("user %s left chat" % nick)
            return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage : %s <port>" % sys.argv[0])
        sys.exit(1)
    port = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), int(port)))
    me = (socket.gethostbyname(socket.gethostname()), s.getsockname()[1])
    s.listen(5)
    print(me)
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=client_thread, args=(conn,))
        t.daemon = True
        t.start()

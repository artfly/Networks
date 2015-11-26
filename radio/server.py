import socketserver
import socket
import threading
import requests
from os import listdir
from os.path import isfile, join
import sys
import time

stations = []
names = ('rock', 'alternative', 'metal')


class Station(threading.Thread):
    def __init__(self, folder, addr):
        super().__init__()
        self.folder = folder
        self.songs = [f for f in listdir(folder) if (isfile(join(folder, f)) and f != 'titles')]
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.addr = addr
        titles_path = self.folder + "/titles"
        with open(titles_path) as f:
            self.titles = f.read().splitlines()

    def run(self):
        super(Station, self).run()
        print(self.songs)
        while True:
            for f in self.songs:
                time.sleep(5)
                with open(self.folder + '/' + f, 'rb') as song:
                    for line in song:
                        self.sock.sendto(line, self.addr)
                    # data = song.read(1024)
                    # while data:
                    #     self.sock.sendto(data, self.addr)
                    #     data = song.read(1024)
                    #     time.sleep(2)


class RadioTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("new connection!")
        while True:
            data = self.request.recv(1024)
            msg_type = requests.parse_type(data)
            if msg_type == requests.LIST:
                response = bytes(' '.join(names), 'utf-8')
            elif msg_type == requests.STATION:
                name = requests.parse_station(data)
                station = stations[names.index(name)]
                print("client choise is %s" % name)
                for title in station.titles:
                    response = requests.title_msg(title)
                    self.request.send(response)
                    self.request.recv(1024)
                response = requests.station_msg(station.addr[0])
            # self.request.send(response)
            # continue
            elif msg_type == requests.EXIT:
                print("client exit!")
                return
            else:
                print("this cannot be")
            self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage : %s <server_port>' % sys.argv[0])
        sys.exit(1)
    port = int(sys.argv[1])
    for i in range(0, len(names)):
        stations.append(Station(names[i], ('239.255.0.' + str(i), port)))
        stations[i].start()

    server = socketserver.ThreadingTCPServer(('', port), RadioTCPHandler)
    ip, port = server.server_address
    print("ip : {} port : {}".format(ip, port))
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

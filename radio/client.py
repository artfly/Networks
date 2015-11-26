import socket
import signal
import threading
import requests
import sys
import struct

tcp_sock = None


def exterminate(arg1, arg2):
    tcp_sock.send(requests.exit_msg())
    sys.exit(0)


def listen(sock):
    print("listen...")
    while True:
        try:
            data = sock.recv(1024)
            print(data.decode("utf-8"))
        except OSError:
            return


def show_help():
    print('''
!help - show help
!list - get stations
!station <station> - connect to station
!stop - disconnect from station
''')


if __name__ == '__main__':
    if len(sys.argv[1:]) != 3:
        print("usage : %s <server_ip> <server_port> <client_port>")
        sys.exit(1)
    port = int(sys.argv[3])
    server_port = int(sys.argv[2])
    server_ip = sys.argv[1]
    udp_thread = None
    udp_sock = None

    signal.signal(signal.SIGINT, exterminate)

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((server_ip, server_port))
    show_help()
    while True:
        cmd = input()
        if cmd == '!help':
            show_help()
        elif cmd == '!list':
            tcp_sock.send(requests.list_msg())
            stations = tcp_sock.recv(1024).decode("utf-8")
            print(stations)
        elif cmd.split()[0] == '!station':
            tcp_sock.send(requests.station_msg(cmd.split()[1]))
            while True:
                song, ret = requests.parse_song(tcp_sock.recv(1024))
                if ret is None:
                    break
                tcp_sock.send(requests.list_msg())
                print(song)
            addr = song
            print(addr)
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp_sock.bind(('', server_port))
            addr_bytes = struct.pack("=4sl", socket.inet_aton(addr), socket.INADDR_ANY)
            udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, addr_bytes)
            udp_thread = threading.Thread(target=listen, args=(udp_sock,))
            udp_thread.daemon = True
            udp_thread.start()
        elif cmd == '!stop':
            udp_sock.close()
        else:
            show_help()

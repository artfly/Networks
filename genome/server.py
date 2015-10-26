import sys
import socket
import struct


GET, RESULT = range(2)
chars = {1 : 'A', 2 : 'C', 3 : 'G', 4 : 'T'}
shift = 20000
MSG_FORMAT = '=b'

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage : %s <hash> <min_length> <max_length>" % sys.argv[0])    
        sys.exit(1)
    start = 5 ** (int(sys.argv[2]) - 1)
    to = (5 ** int(sys.argv[3])) - 1
    print("From %s to %s" % (start, to))
    str_hash = sys.argv[1]
    print(str_hash)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 6666))
    print("I'm %s:%s" % (socket.gethostname(), 6666))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        # print("Connection from : " + str(addr))
        msg = conn.recv(1024)
        msg_type = struct.unpack(MSG_FORMAT, msg[:1])[0]
        if msg_type == GET:
            if start < to:
                conn.send(str_hash.encode("utf-8") + struct.pack("=q", start))
                start += shift
            else:
                conn.send(str_hash.encode("utf-8") + struct.pack("=q", -1))
            conn.close()
        if msg_type == RESULT:
            found = struct.unpack("=h", msg[1:])[0]
            if found != 0:
                print("Client %s found %s matches" % addr, found)
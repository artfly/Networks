import socket
import sys
import struct
import hashlib

GET, RESULT = range(2)
chars = {1 : 'A', 2 : 'C', 3 : 'G', 4 : 'T'}
GET_FORMAT = '=b'
RESULT_FORMAT = '=bh'
shift = 20000


def dec2quinary(num):
    quinary = ''
    if num == 0:
    	return 0
    while num != 0:
        remainder = num % 5
        if remainder == 0:
        	return 0
        quinary = chars[remainder] + quinary
        num = int(num / 5)
    return quinary

def bruteforce(str_hash, start):
	found = 0
	for i in range(start, start + shift):
		seq = dec2quinary(i)
		if seq == 0:
			continue
		h_obj = hashlib.md5(seq.encode("utf-8"))
		if i == 3414431113:
			print("hex of GTATTGAAAG : " + h_obj.hexdigest())
		if h_obj.hexdigest() == str_hash:
			found += 1
			print('found match on ' + dec2quinary(i))
	return found


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("usage : %s <server_ip> <server_port>" % sys.argv[0])
		sys.exit(1)
	(server_ip, server_port) = sys.argv[1:]
	while True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((server_ip, int(server_port)))
		msg = struct.pack(GET_FORMAT, GET)
		s.send(msg)
		data = s.recv(1024)
		str_hash = data[:32].decode("utf-8")
		start = struct.unpack("=q", data[32:])[0]
		s.close()
		if start == -1:
			break
		found = bruteforce(str_hash, start)
		msg = struct.pack(RESULT_FORMAT, RESULT, found)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((server_ip, int(server_port)))
		s.send(msg)
		s.close()
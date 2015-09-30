import socket
import sys

BUFSIZE = 1024

def usage():
	print sys.argv[0] + " <host> <port> <packets_num>"

def main():
	if len(sys.argv) != 4:
		usage()
		sys.exit()
	host, port, packets_num = sys.argv[1:]
	msg = "ping"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(2)
	for i in range(0, int(packets_num)):
		sock.sendto(msg, (host, int(port)))
		try:
			in_msg = sock.recv(BUFSIZE)
			if (in_msg != "pong"):
				print "error : invalid server answer"
			print "Received : " + data + " from : " + addr
		except:
			print "Timeout"

if __name__ == "__main__":
    main()

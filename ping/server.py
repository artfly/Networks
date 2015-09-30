import socket
import sys

BUFSIZE = 1024

def usage():
	print sys.argv[0] + " <port>"

def main():
	if len(sys.argv) != 2:
		usage()
		sys.exit()
	port = int(sys.argv[1])
	msg = "pong"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(("", port))
	while True:
		in_msg, addr = sock.recvfrom(BUFSIZE)
		if (in_msg != "ping"):
			print "error : invalid client answer"
		print "Received %r from %r " % (in_msg, addr)
		sock.sendto(msg, addr)

if __name__ == "__main__":
    main()
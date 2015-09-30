import socket
import time
import sys

def usage():
	print sys.argv[0] + " <port>"

def main():
	if len(sys.argv) != 2:
		usage()
		sys.exit()
	port = int(sys.argv[1])
	count = 0
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.settimeout(2)
	sock.bind(('', port))

	sock.sendto("IBORN", ('<broadcast>', port))
	lifetime = time.time() + 60
	while time.time() < lifetime:
		try:
			message, address = sock.recvfrom(1024)
			print "Message : " + message + " from : " + address
			if message == "IBORN":
				sock.sendto("ILIVE", address)
				count += 1
				print "Current count of copies : " + count
			elif message == "ILIVE":
				count += 1
				print "Current count of copies : " + count
			elif message == "IEXIT":
				print "Current count of copies : " + count
				count -= 1
		except socket.timeout:
			print "No new messages in 2 seconds."
	time.sleep(1)
	sock.sendto("IEXIT", ('<broadcast>', port))
	print "Count at exit : " + count

if __name__ == "__main__":
    main()


import socket
import sys
import os
import time
from threading import Thread

ip = None
port = None


def load_page(conn, addr):
	data = conn.recv(1024)
	request = data.decode("utf-8").split(' ')
	print(request)
	if request[0] == 'GET':
		requested_site = request[1]
		http_str = "http://"
		start = requested_site.index(http_str) + len(http_str)
		end = requested_site.index("/", start)
		requested_site = requested_site[start:end]
		if "www" not in requested_site:
			requested_site = "www." + requested_site 
		try:
			ip = socket.gethostbyname(requested_site)
			forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("Trying to connect...")
			forward.connect((ip, 80))
			forward.send(data)
			while True:
				content = forward.recv(2048)
				print(content)
				if len(content) == 0:
					break
				conn.send(content)
		except Exception as e:
			headers = gen_headers(404)
			content = b"<html><body><p>Error 503:Connection problem</p><p>Python HTTP server</p></body></html>"
			response = headers.encode("utf-8") + content
			conn.send(response)
		print("Sending response..")
		conn.close()

def gen_headers(code):
	headers = ''
	if code == 200:
		headers = 'HTTP/1.1 200 OK\n'
	elif code == 404:
		headers = 'HTTP/1.1 404 Not Found\n'

	date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
	headers += 'Date: ' + date +'\n'
	headers += 'Server: HTTP Server\n'
	headers += 'Connection: close\n\n'
	return headers


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("usage : %s <port>" % sys.argv[0])
		sys.exit(1)
	port = int(sys.argv[1])
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((socket.gethostname(), port))
	serversocket.listen(5)
	while True:
		conn, addr = serversocket.accept()
		thread = Thread(target=load_page, args=(conn, addr))
		thread.daemon = True
		thread.start()

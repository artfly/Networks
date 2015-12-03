import socket
import sys
import os
import time
from threading import Thread

ip = None
port = None

def send_response(conn, addr):
	data = conn.recv(1024)
	request = data.decode("utf-8").split(' ')
	print(request)
	if request[0] == 'GET':
		requested_file = request[1].split('?')[0][1:]
		if requested_file == '':
			requested_file = '.'
		try:
			headers = gen_headers(200)
			if os.path.isdir(requested_file):
				print("Requested dir")
				content = show_dir(requested_file).encode("utf-8")
				response = headers.encode("utf-8") + content
				conn.send(response)
			else:
				with open(requested_file, 'rb') as f:
					response = headers.encode("utf-8")
					conn.send(response)
					# print(requested_file)
					while True:
						content = f.read(65536)
						if len(content) == 0:
							break
						conn.send(content)
		except FileNotFoundError as e:
			headers = gen_headers(404)
			content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
			response = headers.encode("utf-8") + content
			conn.send(response)
		print("Sending response..")
		conn.close()

def show_dir(path):
	html = '<!DOCTYPE html>\n<html>\n<body>\n'
	print([f for f in os.listdir(path)])
	for f in os.listdir(path):
		if path != '.':
			html += '<a href="http://{}:{}/{}">{}</a><br />\n'.format(ip, str(port), path + '/' + f, f)
		else:
			html += '<a href="http://{}:{}/{}">{}</a><br />\n'.format(ip, str(port), f, f)
	html += '</body>\n</html>\n'
	return html


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
	if len(sys.argv) != 3:
		print ("usage : %s <server_ip> <server_port>" % sys.argv[0])
		sys.exit(1)
	ip, port = sys.argv[1], int(sys.argv[2])
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((socket.gethostname(), port))
	serversocket.listen(5)
	while True:
		conn, addr = serversocket.accept()
		thread = Thread(target=send_response, args=(conn, addr))
		thread.daemon = True
		thread.start()

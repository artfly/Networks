import struct


STATION, LIST, EXIT = range(3)
MSG_FORMAT = '=b'

def parse_type(msg):
	return struct.unpack(MSG_FORMAT, msg[:1])[0]

def parse_station(msg):
	return msg[1:].decode('utf-8')

def parse_song(msg):
	msg_type = parse_type(msg)
	if msg_type == STATION:
		return parse_station(msg), None
	else:
		return parse_station(msg), msg_type

def exit_msg():
	return struct.pack(MSG_FORMAT, EXIT)

def list_msg():
	return struct.pack(MSG_FORMAT, LIST)

def station_msg(station):
	return struct.pack(MSG_FORMAT, STATION) + station.encode('utf-8')

def title_msg(title):
	return struct.pack(MSG_FORMAT, LIST) + title.encode('utf-8')

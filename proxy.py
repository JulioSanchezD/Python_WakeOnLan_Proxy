import socket, security, json, os

with open('config.json') as config_file:
	config = json.load(config_file)

UDP_IP = config.get('IP_ADDRESS')
UDP_PORT = 9
BROADCAST_ADDRESS = "192.168.1.255"

sock = socket.socket(socket.AF_INET, #Internet
		     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
 
while True:
	data, addr = sock.recvfrom(1024) 
	if data:
		print(data)
		if security.verify(data):
			sock.sendto(data, (BROADCAST_ADDRESS, UDP_PORT))
		else:
			os.system("sudo ufw delete allow 9/udp")
			break

import socket
import time


sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '10.0.0.2', 1000
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5) 

while True:
	currentTime = time.ctime(time.time()) + "\r\n"
	clientsocket.send(currentTime.encode('ascii'), (host, port))
	clientsocket.close()

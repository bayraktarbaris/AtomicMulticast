import socket
import time


sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '10.0.0.2', 1000
#sender_socket.bind((host, port))

# queue up to 5 requests
#sender_socket.listen(5) 
print 'sender'

while True:
	currentTime = time.ctime(time.time()) + "\r\n"
	sender_socket.sendto('fuck', (host, port))
#	sender_socket.close()
	exit()

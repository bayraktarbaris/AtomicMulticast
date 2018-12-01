import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# get local machine name
host, port = '10.0.0.1', 1000
s.bind((host, port))
print 'receiver'
b = True
#exit()
while b:
	print 'dsfadsfa'
	data, addr = s.recvfrom(1024)
	print "Message: ", data
	b = False

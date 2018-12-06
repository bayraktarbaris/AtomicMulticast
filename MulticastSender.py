import socket
import time
import sys
from message import Message
import pickle
from time import sleep

###################################			Given hostId and member count find the neighbors that will get the packets			#########################

hostId = sys.argv[1]
memberCount = int(sys.argv[2])

f = open("responses/host" + hostId + ".txt","w")

f.close()

neighbors = []

if hostId == '1':

	neighbors.append('2')

	neighbors.append(str(memberCount))

elif hostId == str(memberCount):

	neighbors.append('1')

	neighbors.append(str(memberCount - 1))

else:

	neighbors.append(str(int(hostId + 1)))

	neighbors.append(str(int(hostId - 1)))		

##########################################################################################################################################################

####################################		Adjust the Ip addresses of the neighbors #################################################

f = open("responses/host" + hostId + ".txt","a")

Ip = '10.0.0.'

neighborIPs = []

neighborIPs.append(Ip + neighbors[0])

neighborIPs.append(Ip + neighbors[1])	

########################################################################################################################################

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '10.0.0.' + hostId, 1000

currentTime = time.ctime(time.time()) + "\r"

message = Message(hostId, currentTime)

message = pickle.dumps(message)
# queue up to 5 requests
#sender_socket.listen(5) 
f.write("host" + hostId + "\n")
f.write(neighborIPs[0] + str(port) + "\n")
f.write(neighborIPs[1] + str(port) + "\n")
f.write(currentTime)

while True:

	f.write(neighborIPs[0] + " " + neighborIPs[1] + "\n")
	
	r1 = sender_socket.sendto(message, (neighborIPs[0], port))

	r2 = sender_socket.sendto(message, (neighborIPs[1], port))

	f.write("bytes sent r1 = " + str(r1) + " r2 = " + str(r2) + "\n")

	sender_socket.close()

	break

f.write("Sender sent all the packets to its neighbors!" + "\n")

f.close()
#	sender_socket.close()


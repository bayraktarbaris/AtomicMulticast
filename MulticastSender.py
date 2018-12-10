import socket
import time
import sys
from message import Message
import pickle
from time import sleep


###################################			Given hostId and member count find the neighbors that will get the packets			#########################

hostId = sys.argv[1]
memberCount = int(sys.argv[2])
clockOfInitiator = int(sys.argv[3])
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

	neighbors.append(str(int(hostId) + 1))

	neighbors.append(str(int(hostId) - 1))		

##########################################################################################################################################################

#################################### Adjust the Ip addresses of the neighbors #################################################

f = open("responses/host" + hostId + ".txt","a")

Ip = '10.0.0.'

neighborIPs = []

neighborIPs.append(Ip + neighbors[0])

neighborIPs.append(Ip + neighbors[1])	

########################################################################################################################################
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

hostIP, port = Ip + hostId, 1000

sender_socket.bind((hostIP,port))

heartBeatMessage1 = pickle.dumps(Message(multicastSenderId = hostId,message = "Heartbeat", clockOfInitiator = clockOfInitiator))

heartBeatMessage2 = pickle.dumps(Message(multicastSenderId = hostId,message = "Heartbeat", clockOfInitiator = clockOfInitiator))

for i in range(3):

	r1 = sender_socket.sendto(heartBeatMessage1, (neighborIPs[0], port))

	r2 = sender_socket.sendto(heartBeatMessage2, (neighborIPs[1], port))

	sender_socket.settimeout(1)

	try:

		message1, _ = sender_socket.recvfrom(1024)

		message2, _ = sender_socket.recvfrom(1024)

	except:

		continue 

	sender_socket.close()

	break

if i == 2:

	f.write("One of the hosts is not reachable")

	exit(-1)	

f.write("All hosts are reachable, Starting multicasting")





###########################################################################################################################################

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '10.0.0.' + hostId, 1000

message = Message(hostId, "currentTime", clockOfInitiator)

message.lastSender = Ip + hostId

message = pickle.dumps(message)
# queue up to 5 requests
#sender_socket.listen(5) 
f.write("host" + hostId + "\n")
f.write(neighborIPs[0] + str(port) + "\n")
f.write(neighborIPs[1] + str(port) + "\n")
f.write(currentTime)

book = {neighborIPs[0] + " ack": False, neighborIPs[0] + " safeAck": False, neighborIPs[1] + " ack": False, neighborIPs[1] + " safeAck": False}

while True:

	r1 = sender_socket.sendto(message, (neighborIPs[0], port))

	r2 = sender_socket.sendto(message, (neighborIPs[1], port))

	sender_socket.settimeout(1)

	try:

		message, (address,_) = sender_socket.recvfrom(1024)

	except:

		continue 

	book[address + message.message] = True
	flag = True
	for k, v in book:
		if v == False:
			flag = False
			break
	
	if flag == False:
		
		continue	

	sender_socket.close()

	break

#################################################################################################################################################################



sender_socket = scoket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '10.0.0.' + hostId, 1000

safemessage = pickle.dumps(Message(multicastSenderId = hostId,message = "safe", clockOfInitiator = clockOfInitiator))

for i in range(5):

	r1 = sender_socket.sendto(safemessage, (neighborIPs[0],port))

	r2 = sender_socket.sendto(safemessage, (neighborIPs[1], port))


f.write("Sender sent all the packets to its neighbors!" + "\n")

f.close()



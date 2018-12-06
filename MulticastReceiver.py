import socket
import sys
import pickle

hostId = sys.argv[1] # Gets the id of the host that executes this script
f = open("responses/host" + hostId + ".txt","w") ########## Create a file object to store all the printables related to multicastReceiver
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# get local machine name
hostIP, port = '10.0.0.' + hostId, 1000
s.bind((hostIP, port))
f = open("responses/host" + hostId + ".txt","w")
f.write("host" + hostId + "\n")
f.write(hostIP + " " + str(port) + "\n")
f.close()

messageQueue = []

f = open("responses/host" + hostId + ".txt","a")

while True:
	
	message, addr = s.recvfrom(1024)

	message = pickle.loads(message)

	f.write("Message: " + message.message + " , LastSender: " + str(message.lastSender) + "\n")

	#f.close()

	if message not in messageQueue:		#Somehow if I got the message from 2 other entities then I ignore the last 

		messageQueue.append(message)

	########################	Got the message forward it 		#########################################

	message.lastSender = addr

	neighborIP = hostIP[:7] + str(int(hostIP[7]) + 1) 

	message = pickle.dumps(message)

	f.write("sending message to " + neighborIP + "\n")

	r1 = s.sendto(message, (neighborIP, port))

	f.write("Message is sent by : host " + hostId + "\n") 

	s.close()

	break

for i in range(0,len(messageQueue)):

	f.write("Queue of %s, message %s"%(hostId,messageQueue[i].message))

f.close()	


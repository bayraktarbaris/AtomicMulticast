import socket
import sys
import pickle

hostId = sys.argv[1] # Gets the id of the host that executes this script
memberCount = int(sys.argv[2])

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

neighborIp = ""

f = open("responses/host" + hostId + ".txt","a")

while True:
	
	message, addr = s.recvfrom(1024)

	message = pickle.loads(message)

	f.write("Message: " + message.message + " , LastSender: " + str(message.lastSender) + "\n")

	if message not in messageQueue:		#Somehow if I got the message from 2 other entities then I ignore the last 

		messageQueue.append(message)

	########################	Got the message forward it 		#########################################

	if int(message.lastSender[7]) < int(hostId):		# If i get the packet from a neigbor with lower id i sent to other neighbor with higher id

		if int(hostId) - int(message.lastSender[7]) > 1:	# 1st sends to 5 5 should send to 4 not 6

			neighborIP = hostIP[:7] + str(int(hostIP[7]) - 1)

		else:	

			neighborIP = hostIP[:7] + str((int(hostIP[7]) % memberCount + 1))

	else:

		if int(message.lastSender[7]) - int(hostId) > 1:

			neighborIP = hostIP[:7] + str(int(hostIP[7]) + 1) #5th sends to 1 1 should send to 2 not 5

		else:	

			if hostId == '1':	# If my id is 1 but I got from 2 then i send to last member

				neighborIP = hostIP[:7] + str(memberCount)
		
			else:	

				neighborIP = hostIP[:7] + str(int(hostIP[7]) - 1)

	message.lastSender = hostIP

	message = pickle.dumps(message)

	f.write("sending message to " + neighborIP + "\n")

	r1 = s.sendto(message, (neighborIP, port))

	#f.write("Message is sent by : host " + hostId + "\n") 

	s.close()

	break

for i in range(0,len(messageQueue)):

	f.write("Queue of %s, message %s"%(hostId,messageQueue[i].message))

f.close()

exit()	


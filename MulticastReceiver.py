import socket
import sys
import pickle
from message import Message
from queue import Queue

print "amk"
hostId = sys.argv[1] # Gets the id of the host that executes this script

memberCount = int(sys.argv[2])
multicastInitiator = int(sys.argv[3])

f = open("responses/host" + hostId + ".txt","w+") ########## Create a file object to store all the printables related to multicastReceiverf.write(hostId)
hostTree = list(range(1, memberCount+1))
for i in range(int(len(hostTree)/2)+multicastInitiator):
	hostTree = hostTree[1:] + hostTree[:1]

for i in hostTree:
	f.write(str(i))

# create a socket object
f.write("1")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# get local machine name
f.write("2")
hostIP, port = '10.0.0.' + hostId, 1000
s.bind((hostIP, port))
f.write("3")
f = open("responses/host" + hostId + ".txt","w+")
f.write("host" + hostId + "\n")
f.write(hostIP + " " + str(port) + "\n")
f.close()

messageQueue = []

neighborIp = ""
#f.write(4)

f = open("responses/host" + hostId + ".txt","a+")

while True:

	s.settimeout(5)

	message, addr = s.recvfrom(1024)

	message = pickle.loads(message)

	f.write(message.message) 

	try:

		if message.fromChild == False:
			
			if hostTree.index(int(hostId)) < hostTree.index(multicastInitiator) and hostTree.index(int(hostId)) != 0:

				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])


				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))

			elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator) and hostTree.index(int(hostId)) != memberCount - 1:	

				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])


				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))

			elif hostTree.index(int(hostId)) == 0:
			
				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

				message.fromChild = True

				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))	
				break

			elif hostTree.index(int(hostId)) == memberCount - 1:
			
				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

				message.fromChild = True


				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))
				break

		elif message.fromChild == True:
			
			if hostTree.index(int(hostId)) < hostTree.index(multicastInitiator):

				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

				message = pickle.dumps(message)

				

				r = s.sendto(message,(childIP, port))

			elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator):	

				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))	
			break


	except Exception as e:
	
		continue


if i == 2:

	f.write("Parent or child is unreachable !")

	f.close()

	exit(-1)

f.close()	

#######################################################################################################

queue = Queue("responses/host" + hostId + "queue.txt")

while True:

	s.settimeout(5)
	
	message, addr = s.recvfrom(1024)

	message = pickle.loads(message)

	if message.message == "currentTime" and message not in queue.read():

		queue.append(str(message.multicastSenderId) + ' ' + str(message.clockOfInitiator))

		if hostTree.index(int(hostId)) < hostTree.index(multicastInitiator) and hostTree.index(int(hostId)) != 0:

			childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

			parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

			message = pickle.dumps(message)
			
			r = s.sendto(message,(childIP, port))

			ackMessage = pickle.dumps(Message(multicastSenderId = hostId,message = "ack", clockOfInitiator = message.clockOfInitiator))


			r2 = s.sendto(ackMessage, (parentIP,port))

		elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator) and hostTree.index(int(hostId)) != memberCount - 1:

			childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

			parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

			message = pickle.dumps(message)
			
			r = s.sendto(message,(childIP, port))

			ackMessage = pickle.dumps(Message(multicastSenderId = hostId,message = "ack", clockOfInitiator = message.clockOfInitiator))


			r2 = s.sendto(ackMessage, (parentIP,port))	

		elif hostTree.index(int(hostId)) == 0:
			
			parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

			safeAckmessage = pickle.dumps(Message(multicastSenderId = hostId,message = "safeAck", clockOfInitiator = message.clockOfInitiator))

			r2 = s.sendto(safeAckmessage, (parentIP,port))


		elif hostTree.index(int(hostId)) == memberCount - 1:
			
			parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

			safeAckmessage = pickle.dumps(Message(multicastSenderId = hostId,message = "safeAck", clockOfInitiator = message.clockOfInitiator))

			r2 = s.sendto(safeAckmessage, (parentIP,port))

	elif message.message == "safeAck":

		if hostTree.index(int(hostId)) < hostTree.index(multicastInitiator)

			parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

			message = pickle.dumps(message)
			
			r = s.sendto(message,(parentIP, port))

			break
	
		elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator)

			parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

			message = pickle.dumps(message)
			
			r = s.sendto(message,(parentIP, port))

			break

######################################################################################################################################################################

f = open("responses/host" + hostId + "delivery.txt")

message, addr = s.recvfrom(1024)

message = pickle.loads(message)

if message.message == "safe":

	popped =  queue.pop()

	f.write(popped + "\n")


f.close()

exit()	


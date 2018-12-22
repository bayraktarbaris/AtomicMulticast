import socket
import sys
import pickle
from message import Message
from queue import Queue

hostId = sys.argv[1] # Gets the id of the host that executes this script

memberCount = int(sys.argv[2])
multicastInitiator = int(sys.argv[3])
port = int(sys.argv[4])

f = open("responses/host" + hostId + ".txt","a+") ########## Create a file object to store all the printables related to multicastReceiverf.write(hostId)
hostTree = list(range(1, memberCount+1))
for i in range(int(len(hostTree)/2)+multicastInitiator):
	hostTree = hostTree[1:] + hostTree[:1]

for i in hostTree:
	f.write(str(i))

# create a socket object

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# get local machine name

hostIP = '10.0.0.' + hostId
s.bind((hostIP, port))
f = open("responses/host" + hostId + ".txt","a+")
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


#s.settimeout(5)

message, (addr,_) = s.recvfrom(1024)

f = open("responses/host" + hostId + ".txt","a+")

f.write("\ngot  message from " + str(addr))

f.close()

message = pickle.loads(message)

if message.message == "currentTime" and message not in queue.read():

	queue.append(str(message.multicastSenderId) + ' ' + str(message.clockOfInitiator))

	if hostTree.index(int(hostId)) < hostTree.index(multicastInitiator) and hostTree.index(int(hostId)) != 0:

		childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

		message = pickle.dumps(message)

		while True:

			s.settimeout(1)

			r = s.sendto(message,(childIP, port))

			f = open("responses/host" + hostId + ".txt","a+")

			f.write("\nsend  message to " + str(childIP) + pickle.loads(message).message)

			f.close()

			try:

				message, addr = s.recvfrom(1024)

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("\ngot  message from " + str(addr) + pickle.loads(message).message)

				f.close()

				message = pickle.loads(message)

			except:

				continue

			if message.message == "ack":

				break

		ackMessage = pickle.dumps(Message(multicastSenderId = hostId,message = "ack", clockOfInitiator = message.clockOfInitiator))


		r2 = s.sendto(ackMessage, (parentIP,port))

		f = open("responses/host" + hostId + ".txt","a+")

		f.write("\nsent message to " + parentIP + pickle.loads(ackMessage).message)

		f.close()	

	elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator) and hostTree.index(int(hostId)) != memberCount - 1:

		childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

		message = pickle.dumps(message)
		
		while True:

			s.settimeout(1)

			r = s.sendto(message,(childIP, port))

			try:

				message, addr = s.recvfrom(1024)

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("\ngot  message from " + str(addr) + pickle.loads(message).message)

				f.close()

				message = pickle.loads(message)

			except:

				continue

			if message.message == "ack":

				break

		ackMessage = pickle.dumps(Message(multicastSenderId = hostId,message = "ack", clockOfInitiator = message.clockOfInitiator))


		r2 = s.sendto(ackMessage, (parentIP,port))

		f = open("responses/host" + hostId + ".txt","a+")

		f.write("\nsent message to " + parentIP + pickle.loads(ackMessage).message)

		f.close()	

	elif hostTree.index(int(hostId)) == 0:

		f = open("responses/host" + hostId + ".txt","a+")

		f.write("\ngot  message from " + str(addr) + message.message)

		f.close()
		
		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

		ackMessage = pickle.dumps(Message(multicastSenderId = hostId,message = "ack", clockOfInitiator = message.clockOfInitiator))

		safeAckmessage = pickle.dumps(Message(multicastSenderId = hostId,message = "safeAck", clockOfInitiator = message.clockOfInitiator))

		r = s.sendto(ackMessage, (parentIP,port))

		r2 = s.sendto(safeAckmessage, (parentIP,port))


	elif hostTree.index(int(hostId)) == memberCount - 1:

		f = open("responses/host" + hostId + ".txt","a+")

		f.write("\ngot  message from " + str(addr) + message.message)

		f.close()
		
		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

		ackMessage = pickle.dumps(Message(multicastSenderId = hostId,message = "ack", clockOfInitiator = message.clockOfInitiator))

		safeAckmessage = pickle.dumps(Message(multicastSenderId = hostId,message = "safeAck", clockOfInitiator = message.clockOfInitiator))

		r = s.sendto(ackMessage, (parentIP,port))

		r2 = s.sendto(safeAckmessage, (parentIP,port))


message, addr = s.recvfrom(1024)


message = pickle.loads(message) 		

if message.message == "safeAck":

	if hostTree.index(int(hostId)) < hostTree.index(multicastInitiator):

		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

		message = pickle.dumps(message)

		while True:

			s.settimeout(1)

			r = s.sendto(message,(parentIP, port))

			try:

				message2, addr = s.recvfrom(1024)

				message2 = pickle.loads(message2)

			except:
			
				continue

			if message2.message == "safe":
				f= open("responses/host" + hostId + ".txt","a+")

				f.write("AAAAAA" + str(queue.read()))

				f.close()
				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

				message2 = pickle.dumps(message2)

				for i in range(0,5):

					r = s.sendto(message2,(childIP, port))

				while queue.read() != [] and queue.read() != ['']:

					f= open("responses/host" + hostId + ".txt","a+")

					f.write("\nBBBBB"+str(queue.read()) +" "+ str(multicastInitiator) +" "+ str(pickle.loads(message2).clockOfInitiator) +" "+"\n")

					f.close()

					if queue.read()[0].split()[0] == str(multicastInitiator) and str(pickle.loads(message2).clockOfInitiator) == queue.read()[0].split()[1]:



						f = open("responses/host" + hostId + "delivery.txt", "a+")
						
						popped =  queue.pop()

						f.write(popped + "\n")

						f.close()

						break

				break			


	elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator):

		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

		message = pickle.dumps(message)

		while True:

			s.settimeout(1)

			r = s.sendto(message,(parentIP, port))

			try:

				message2, addr = s.recvfrom(1024)

				message2 = pickle.loads(message2)

			except:
			
				continue

			if message2.message == "safe":
				f= open("responses/host" + hostId + ".txt","a+")

				f.write("safe received")

				f.close()
				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

				message2 = pickle.dumps(message2)

				for i in range(0,5):

					r = s.sendto(message2,(childIP, port))
				f= open("responses/host" + hostId + ".txt","a+")
				f.write("\n1\n")
				f.close()
				f= open("responses/host" + hostId + ".txt","a+")
				f.write("\n"+str(queue.read())+"\n")
				f.close()
				f= open("responses/host" + hostId + ".txt","a+")
				f.write("\n2\n")
				f.close()

				while queue.read() != [] and queue.read() != ['']:
					f= open("responses/host" + hostId + ".txt","a+")

					f.write("\nBBBBB"+str(queue.read()) +" "+ str(multicastInitiator) +" "+ str(pickle.loads(message2).clockOfInitiator) +" "+"\n")

					f.close()
					if queue.read()[0].split()[0]	== str(multicastInitiator)  and str(pickle.loads(message2).clockOfInitiator) == queue.read()[0].split()[1]:

						f = open("responses/host" + hostId + "delivery.txt", "a+")
						
						popped =  queue.pop()

						f.write(popped + "\n")

						f.close()

						break

				break					


elif message.message == "safe":
	f= open("responses/host" + hostId + ".txt","a+")

	f.write("safe received")

	f.close()
	while queue.read() != [] and queue.read() != ['']:
		f= open("responses/host" + hostId + ".txt","a+")

		f.write("\nBBBBB"+str(queue.read()) +" "+ str(multicastInitiator) +" "+ str(message.clockOfInitiator) +" "+"\n")

		f.close()
		if queue.read()[0].split()[0]	== str(multicastInitiator)  and str(message.clockOfInitiator) == queue.read()[0].split()[1]:

			f = open("responses/host" + hostId + "delivery.txt",'a+')
			
			popped =  queue.pop()

			f.write(popped + "\n")

			f.close()

			break

exit()					


######################################################################################################################################################################


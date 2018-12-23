import socket
import sys
import pickle
import time
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

counter = 0

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
				counter += 1

			elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator) and hostTree.index(int(hostId)) != memberCount - 1:	

				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])


				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))
				counter += 1

			elif hostTree.index(int(hostId)) == 0:
			
				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

				message.fromChild = True

				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))	
				counter += 1
				break

			elif hostTree.index(int(hostId)) == memberCount - 1:
			
				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

				message.fromChild = True


				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))
				counter += 1
				break

		elif message.fromChild == True:
			
			if hostTree.index(int(hostId)) < hostTree.index(multicastInitiator):

				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

				message = pickle.dumps(message)

				

				r = s.sendto(message,(childIP, port))
				counter += 1

			elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator):	

				childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

				message = pickle.dumps(message)
				

				r = s.sendto(message,(childIP, port))	
				counter += 1
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

f.write("got  message from " + str(addr) + "\n")

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
			counter += 1

			f = open("responses/host" + hostId + ".txt","a+")

			f.write("send  message to " + str(childIP) + pickle.loads(message).message + "\n")

			f.close()

			try:

				safeAckmessage, addr = s.recvfrom(1024)

				safeAckmessage = pickle.loads(safeAckmessage)

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("got  message from " + str(addr) + " message : " + safeAckmessage.message + "\n")

				f.close()

			except:

				continue

			if safeAckmessage.message == "safeAck":

				break

	
		while True:

			

			f = open("responses/host" + hostId + ".txt","a+")

			f.write("sending message to " + parentIP + safeAckmessage.message)

			f.close()

			safeAckmessage = pickle.dumps(safeAckmessage)

			r2 = s.sendto(safeAckmessage, (parentIP,port))
			counter += 1

			s.settimeout(1)

			try:

				safeMessage, addr = s.recvfrom(1024)

				safeMessage = pickle.loads(safeMessage)

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("got  message from " + str(addr) + " message : " + safeMessage.message + "\n")

				f.close()

			except:
			
				continue

			if safeMessage.message == "safe":
			
				f = open("responses/host" + hostId + ".txt","a+")

				f.write("Got the message" + safeMessage.message + " \n")

				f.close()

				safeMessage = pickle.dumps(safeMessage)

				for i in range(memberCount*2):

					

					r = s.sendto(safeMessage,(childIP, port))
					counter += 1

				while queue.read() != [] and queue.read() != ['']:

					f= open("responses/host" + hostId + ".txt","a+")

					f.write("Current queue: "+ str(queue.read()) + " multicastInitiator: "+ str(multicastInitiator) +" clockOfInitiator: "+ str(pickle.loads(safeMessage).clockOfInitiator) +" "+"\n")

					f.close()

					if queue.read()[0].split()[0] == str(multicastInitiator) and str(pickle.loads(safeMessage).clockOfInitiator) == queue.read()[0].split()[1]:



						f = open("responses/host" + hostId + "delivery.txt", "a+")
						
						popped =  queue.pop()

						f.write(popped + "\n")

						f.close()

						break

				break					

				

	elif hostTree.index(int(hostId)) > hostTree.index(multicastInitiator) and hostTree.index(int(hostId)) != memberCount - 1:

		childIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

		message = pickle.dumps(message)

		while True:



			s.settimeout(1)

			r = s.sendto(message,(childIP, port))
			counter += 1

			f = open("responses/host" + hostId + ".txt","a+")

			f.write("send  message to " + str(childIP) + pickle.loads(message).message + "\n")

			f.close()

			try:

				safeAckmessage, addr = s.recvfrom(1024)

				safeAckmessage = pickle.loads(safeAckmessage)

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("got  message from " + str(addr) + " message : " + safeAckmessage.message + "\n")

				f.close()

			except:

				continue

			if safeAckmessage.message == "safeAck":

				break

	
		while True:

			f = open("responses/host" + hostId + ".txt","a+")

			f.write("sending message to " + parentIP + safeAckmessage.message)

			f.close()

			safeAckmessage = pickle.dumps(safeAckmessage)

			r2 = s.sendto(safeAckmessage, (parentIP,port))
			counter += 1

			s.settimeout(1)

			try:

				safeMessage, addr = s.recvfrom(1024)

				safeMessage = pickle.loads(safeMessage)

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("got  message from " + str(addr) + " message : " + safeMessage.message + "\n")

				f.close()

			except:
			
				continue

			if safeMessage.message == "safe":
			
				f = open("responses/host" + hostId + ".txt","a+")

				f.write("Got the message" + safeMessage.message + " \n")

				f.close()

				safeMessage = pickle.dumps(safeMessage)

				for i in range(memberCount*2):

					r = s.sendto(safeMessage,(childIP, port))
					counter += 1

				while queue.read() != [] and queue.read() != ['']:

					f= open("responses/host" + hostId + ".txt","a+")

					f.write("Current queue: "+ str(queue.read()) + " multicastInitiator: "+ str(multicastInitiator) +" clockOfInitiator: "+ str(pickle.loads(safeMessage).clockOfInitiator) +" "+"\n")

					f.close()

					if queue.read()[0].split()[0] == str(multicastInitiator) and str(pickle.loads(safeMessage).clockOfInitiator) == queue.read()[0].split()[1]:



						f = open("responses/host" + hostId + "delivery.txt", "a+")
						
						popped =  queue.pop()

						f.write(popped + "\n")

						f.close()

						break

				break	

	elif hostTree.index(int(hostId)) == 0:

		f = open("responses/host" + hostId + ".txt","a+")

		f.write("got  message from " + str(addr) + message.message + "\n")

		f.close()
		
		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) + 1])

		safeAckmessage = pickle.dumps(Message(multicastSenderId = hostId,message = "safeAck", clockOfInitiator = message.clockOfInitiator))

		while True:	

			r2 = s.sendto(safeAckmessage, (parentIP,port))
			counter += 1

			s.settimeout(2)

			startingTime = time.time()

			try:

				safeMessage, addr = s.recvfrom(1024)

				safeMessage = pickle.loads(safeMessage)

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("got  message from " + str(addr) + " message : " + safeMessage.message + "\n")

				f.close()

			except: 
			
				continue

			if 	safeMessage.message == "safe":

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("Got the message" + safeMessage.message + " \n")

				f.close()

				while queue.read() != [] and queue.read() != ['']:

					f= open("responses/host" + hostId + ".txt","a+")

					f.write("Current queue: "+ str(queue.read()) + " multicastInitiator: "+ str(multicastInitiator) +" clockOfInitiator: "+ str(safeMessage.clockOfInitiator) +" "+"\n")

					f.close()

					if queue.read()[0].split()[0] == str(multicastInitiator) and str(safeMessage.clockOfInitiator) == queue.read()[0].split()[1]:



						f = open("responses/host" + hostId + "delivery.txt", "a+")
						
						popped =  queue.pop()

						endingTime = time.time()

						f.write(popped + "\n" )

						f.close()

						f = open("responses/leaftime" + str(memberCount)+ ".txt", "a+")

						f.write(str(endingTime - startingTime) + "\n" )

						f.close()

						break

				break		




	elif hostTree.index(int(hostId)) == memberCount - 1:

		f = open("responses/host" + hostId + ".txt","a+")

		f.write("got  message from " + str(addr) + message.message + "\n")

		f.close()
		
		parentIP = '10.0.0.' + str(hostTree[hostTree.index(int(hostId)) - 1])

		safeAckmessage = pickle.dumps(Message(multicastSenderId = hostId,message = "safeAck", clockOfInitiator = message.clockOfInitiator))

		while True:	

			r2 = s.sendto(safeAckmessage, (parentIP,port))
			counter += 1

			s.settimeout(2)

			try:

				safeMessage, addr = s.recvfrom(1024)

				safeMessage = pickle.loads(safeMessage)

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("got  message from " + str(addr) + " message : " + safeMessage.message + "\n")

				f.close()

			except: 
			
				continue

			if 	safeMessage.message == "safe":

				f = open("responses/host" + hostId + ".txt","a+")

				f.write("Got the message" + safeMessage.message + " \n")

				f.close()

				while queue.read() != [] and queue.read() != ['']:

					f= open("responses/host" + hostId + ".txt","a+")

					f.write("Current queue: "+ str(queue.read()) + " multicastInitiator: "+ str(multicastInitiator) +" clockOfInitiator: "+ str(safeMessage.clockOfInitiator) +" "+"\n")

					f.close()

					if queue.read()[0].split()[0] == str(multicastInitiator) and str(safeMessage.clockOfInitiator) == queue.read()[0].split()[1]:



						f = open("responses/host" + hostId + "delivery.txt", "a+")
						
						popped =  queue.pop()

						f.write(popped + "\n")

						f.close()

						break

				break		


f = open("experiments/counter" + str(memberCount) + ".txt", "a+")
						

f.write(str(counter) + " ")

f.close()

exit()					


######################################################################################################################################################################

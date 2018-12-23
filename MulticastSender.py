import socket
import time
import sys
from message import Message
import pickle
from queue import Queue
from time import sleep

###################################			Given hostId and member count find the neighbors that will get the packets			#########################

hostId = sys.argv[1]
memberCount = int(sys.argv[2])
clockOfInitiator = int(sys.argv[3])
port = int(sys.argv[4])
f = open("responses/host" + hostId + ".txt", "a+")

f.close()

neighbors = []

if hostId == '1':

    neighbors.append('2')

    neighbors.append(str(memberCount))

elif hostId == str(memberCount):

    neighbors.append(str(memberCount - 1))

    neighbors.append('1')

else:

    neighbors.append(str(int(hostId) - 1))

    neighbors.append(str(int(hostId) + 1))

##########################################################################################################################################################

#################################### Adjust the Ip addresses of the neighbors #################################################

f = open("responses/host" + hostId + ".txt", "a+")

Ip = '10.0.0.'

neighborIPs = []

neighborIPs.append(Ip + neighbors[0])

neighborIPs.append(Ip + neighbors[1])

########################################################################################################################################
counter = 0

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

hostIP = Ip + hostId

sender_socket.bind((hostIP, port))

heartBeatMessage1 = pickle.dumps(
    Message(multicastSenderId=hostId, message="Heartbeat", clockOfInitiator=clockOfInitiator))

heartBeatMessage2 = pickle.dumps(
    Message(multicastSenderId=hostId, message="Heartbeat", clockOfInitiator=clockOfInitiator))

for i in range(memberCount*6):

    r1 = sender_socket.sendto(heartBeatMessage1, (neighborIPs[0], port))
    counter += 1

    r2 = sender_socket.sendto(heartBeatMessage2, (neighborIPs[1], port))
    counter += 1

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

sender_socket.bind((hostIP, port))

host = '10.0.0.' + hostId

message = Message(hostId, "currentTime", clockOfInitiator)

message.lastSender = Ip + hostId

message = pickle.dumps(message)
# queue up to 5 requests
# sender_socket.listen(5)
f.write("host" + hostId + "\n")
f.write(neighborIPs[0] + str(port) + "\n")
f.write(neighborIPs[1] + str(port) + "\n")
f.write("currentTime")
f.close()

book = {neighborIPs[0] + " safeAck": False, neighborIPs[1] + " safeAck": False}

queue = Queue("responses/host" + hostId + "queue.txt")

queue.append(str(pickle.loads(message).multicastSenderId) + ' ' + str(pickle.loads(message).clockOfInitiator))

startingTime = time.time()

while True:
    r1 = sender_socket.sendto(message, (neighborIPs[0], port))
    counter += 1

    r2 = sender_socket.sendto(message, (neighborIPs[1], port))
    counter += 1

    sender_socket.settimeout(5)

    try:
        f = open("responses/host" + hostId + ".txt", "a+")

        f.write("Waiting to receive SafeAck from childs \n")

        f.close()
        message2, address1 = sender_socket.recvfrom(1024)
        message3, address2 = sender_socket.recvfrom(1024)

        message2 = pickle.loads(message2)
        message3 = pickle.loads(message3)

        f = open("responses/host" + hostId + ".txt", "a+")

        f.write("Got the message :" + message2.message + " from child " + str(address1) + " \n")
        f.write("Got the message :" + message3.message + " from child " + str(address2) + " \n")

        f.close()

    except:

        continue

    if message2.message == "safeAck":
        book[address1[0] + " " + message2.message] = True

    if message3.message == "safeAck":
        book[address2[0] + " " + message3.message] = True

    f = open("responses/host" + hostId + ".txt", "a+")

    f.write("received from " + "\n" + str(book) + str(port) + "\n")

    f.close()
    flag = True
    for k, v in book.items():
        if v == False:
            flag = False
            break

    if flag == False:
        continue

    break

#################################################################################################################################################################

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = '10.0.0.' + hostId

safeMessage = pickle.dumps(Message(multicastSenderId=hostId, message="safe", clockOfInitiator=clockOfInitiator))

for i in range(memberCount*2):

    r1 = sender_socket.sendto(safeMessage, (neighborIPs[0], port))
    counter += 1

    r2 = sender_socket.sendto(safeMessage, (neighborIPs[1], port))
    counter += 1

endingTime = time.time()

safeMessage = pickle.loads(safeMessage)

while queue.read() != [] and queue.read() != ['']:

	f = open("responses/host" + hostId + ".txt","a+")

	f.write("Current queue: "+ str(queue.read()) + " multicastInitiator: "+ hostId +" clockOfInitiator: "+ str(safeMessage.clockOfInitiator) +" "+"\n")

	f.close()

	if queue.read()[0].split()[0] == hostId and str(safeMessage.clockOfInitiator) == queue.read()[0].split()[1]:



		f = open("responses/host" + hostId + "delivery.txt", "a+")
		
		popped =  queue.pop()

		f.write(popped + "\n")

		f.close()

		break


f = open("responses/initiatorTime" +str(memberCount) + ".txt", "a+")

f.write(str(endingTime - startingTime) + "\n" )

f.close()

f = open("experiments/counter" + str(memberCount) + ".txt", "a+")
						

f.write(str(counter) + " ")

f.close()

f = open("responses/host" + hostId + ".txt", "a+")
f.write("Sender sent all the packets to its neighbors!\n")

f.close()

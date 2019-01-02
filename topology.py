## Name: Orhun Bugra BARAN No: 2035699
## Name: Baris Bayraktar No:2035715

from mininet.topo import Topo
import sys
from mininet.net import Mininet                                                                        
from mininet.node import Controller
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
from mininet.link import TCLink
from multicastStart import multicastStart
import time
from time import sleep
import os
import timeGenerator

## Some comments : multicastStart.py sets up the hosts that are sender and receivers for a particular simulation of multicast
## It runs multicastReceiver.py in hosts that will be receiving the message, multicastSender.py on the host that will send the multicast message
## clock is used for keeping track of logical clock of different hosts.

class SingleSwitchTopo(Topo):

	def build(self, numberOfNodes, loss, delay):

		hosts = []

		#Create hosts given hostCount

		for i in range(1, numberOfNodes + 1):

			hosts.append(self.addHost("host" + str(i)))


		#Create the single switch

		switch = self.addSwitch("s1")

		#Add links between switch and hosts

		for i in range(0, numberOfNodes):

			self.addLink(hosts[i], switch,loss = loss, delay=str(delay) + "ms")


if len(sys.argv) < 4:

	print("Usage: python topology.py numberOfNodes lossRate multicastInitiator experimentNo")

	exit(-1)


numberOfNodes = int(sys.argv[1])
loss = float(sys.argv[2])
multicastInitiator = int(sys.argv[3])
experiment = int(sys.argv[4])

																			   
if __name__ == '__main__':
	os.system("rm -rf responses/host*")
	f = open("experiments/counter" + str(numberOfNodes) + ".txt", "a+")
						

	f.write("\n")

	f.close()
	if experiment == 1: # Group size vs stable deliver time you need to run it for different numberOfNodes
		loss = 0.0
		delay = 0
		numberOfNodes = 5 # For different topologies you need to set it different numbers
		net = Mininet( topo=SingleSwitchTopo(numberOfNodes, loss, delay) , link = TCLink)
		net.start()
		clocks = {}
		port = 11000
		for j in range(1,numberOfNodes+1):
			clocks['host' + str(j)] = 0
			f = open("responses/host" + str(j) + "delivery.txt",'a+')
			f.close()
		for i in range(100):	
			clocks['host' + str(multicastInitiator)] += 1
			multicastStart(net, multicastInitiator, numberOfNodes,clocks['host' + str(multicastInitiator)], port)
			port += 1
			clocks['host' + str(multicastInitiator - 1)] += 1
			multicastStart(net, multicastInitiator - 1, numberOfNodes,clocks['host' + str(multicastInitiator - 1)], port)
			port += 1
	elif experiment == 2: # Lambda vs stable delivery time, under the folder responses two files are important, initiatorTime + groupsize + poisson + poissonVariable and leaftime  + groupsize + poisson + poissonVariable these are added to give total time that has passed upon creation and delivery of multicast message
		loss = 0.0
		delay = 6 # Increasing the delay increases number of process running on a particular host therefore after some point the logs are crashing, even VM is crashed couple of times for huge delays
		net = Mininet( topo=SingleSwitchTopo(numberOfNodes, loss, delay) , link = TCLink)
		net.start()
		clocks = {}
		for i in range(1,numberOfNodes+1):
			clocks['host' + str(i)] = 0
			f = open("responses/host" + str(i) + "delivery.txt",'a+')
			f.close()
		print(clocks)
		port = 11000
		for i in range(100):
			poissonVariable = 4		# Set for different rates of packets/ sec
			for j in range(int(poissonVariable / 2)):
				clocks['host' + str(multicastInitiator -1)] += 1
				multicastStart(net, multicastInitiator -1, numberOfNodes,clocks['host' + str(multicastInitiator -1)], port)
				port += 1
				clocks['host' + str(multicastInitiator)] += 1
				multicastStart(net, multicastInitiator, numberOfNodes,clocks['host' + str(multicastInitiator)], port)
				port += 1
			sleep(timeGenerator.nextInterval(poissonVariable))
	elif experiment == 3: # Group size vs Efficiency,  Number of nodes states the group size under experiments folder counter counts the total number of transmissions, all messages are assumed to be of the same size(bytes)
		loss = 0.0
		delay = 0
		numberOfNodes = 10 # For different topologies you need to set it different numbers
		net = Mininet( topo=SingleSwitchTopo(numberOfNodes, loss, delay) , link = TCLink)
		net.start()
		clocks = {}
		port = 11000
		for j in range(1,numberOfNodes+1):
			clocks['host' + str(j)] = 0
			f = open("responses/host" + str(j) + "delivery.txt",'a+')
			f.close()
		for i in range(100):	
			clocks['host' + str(multicastInitiator)] += 1
			multicastStart(net, multicastInitiator, numberOfNodes,clocks['host' + str(multicastInitiator)], port)
			port += 1
			clocks['host' + str(multicastInitiator - 1)] += 1
			multicastStart(net, multicastInitiator - 1, numberOfNodes,clocks['host' + str(multicastInitiator - 1)], port)
			port += 1
	elif experiment == 4: # Lambda vs efficiency for efficiency refer to the counter + groupsize.txt under experiments folder
	
		loss = 0.0
		delay = 0
		net = Mininet( topo=SingleSwitchTopo(numberOfNodes, loss, delay) , link = TCLink)
		net.start()
		clocks = {}
		for i in range(1,numberOfNodes+1):
			clocks['host' + str(i)] = 0
			f = open("responses/host" + str(i) + "delivery.txt",'a+')
			f.close()
		print(clocks)
		port = 11000
		for i in range(100):
			poissonVariable = 4		
			for j in range(int(poissonVariable)):
				clocks['host' + str(multicastInitiator)] += 1
				multicastStart(net, multicastInitiator, numberOfNodes,clocks['host' + str(multicastInitiator)], port)
				port += 1
			sleep(timeGenerator.nextInterval(poissonVariable))		

	sleep(4) # Program ends without waiting sender to send 

	################### Sometimes after trying many consecutive experiments back to back the results are getting ambiguos some errors occuring etc, in this case close the VM and try again #######
	################### Note that we experimented with the delays, losses mentioned in the report, here before submission we just set it those things such that they finish asap to check whether everything is fine before submitting ###########
	net.stop()

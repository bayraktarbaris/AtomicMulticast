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


class SingleSwitchTopo(Topo):

	def build(self, numberOfNodes, loss):

		hosts = []

		#Create hosts given hostCount

		for i in range(1, numberOfNodes + 1):

			hosts.append(self.addHost("host" + str(i)))


		#Create the single switch

		switch = self.addSwitch("s1")

		#Add links between switch and hosts

		for i in range(0, numberOfNodes):

			self.addLink(hosts[i], switch,loss = loss)


if len(sys.argv) < 3:

	print("Usage: python topology.py numberOfNodes lossRate multicastInitiator")

	exit(-1)


numberOfNodes = int(sys.argv[1])
loss = float(sys.argv[2])
multicastInitiator = int(sys.argv[3])

																			   
if __name__ == '__main__':
	net = Mininet( topo=SingleSwitchTopo(numberOfNodes, loss) , link = TCLink)
	net.start()
	clocks = {}
	for i in (1,numberOfNodes+1):
		clocks['host' + str(i)] = 0
	clocks['host' + str(multicastInitiator)] += 1
	multicastStart(net, multicastInitiator, numberOfNodes,clocks['host' + str(multicastInitiator)])  # Later on we can create multiple instances each of them acting as a different multicast process
	
 #  print host1.cmd('ping 127.0.0.1')
 #  print host2.cmd('ifconfig')
	#net.pingAll()
	#time.sleep(5)
	#net.configLinkStatus("host" + str(numberOfNodes - 1),"s1","down")
	#net.pingAll()
	#net.configLinkStatus("host" + str(numberOfNodes - 1),"s1","up")
	#net.pingAll()
	sleep(4) # Program ends without waiting sender to send 
	net.stop()

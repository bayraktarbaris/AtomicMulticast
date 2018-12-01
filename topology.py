from mininet.topo import Topo
import sys
from mininet.net import Mininet                                                                        
from mininet.node import Controller
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
from mininet.link import TCLink
import time
import os


class SingleSwitchTopo(Topo):

	def build(self, numberOfNodes, loss):

		hosts = []

		#Create hosts given hostCount

		for i in range(0, numberOfNodes):

			hosts.append(self.addHost("host" + str(i)))

		#Create the single switch

		switch = self.addSwitch("s1")

		#Add links between switch and hosts

		for i in range(0, numberOfNodes):

			self.addLink(hosts[i], switch,loss = loss)

if len(sys.argv) < 3:

	print("Usage: python topology.py numberOfNodes lossRate")

	exit(-1)


numberOfNodes = int(sys.argv[1])
loss = float(sys.argv[2])

                                                                               
if __name__ == '__main__':
    net = Mininet( topo=SingleSwitchTopo(numberOfNodes, loss) , link = TCLink)
    net.start()
    net.pingAll()
    time.sleep(5)
    net.configLinkStatus("host" + str(numberOfNodes - 1),"s1","down")
    net.pingAll()
    net.configLinkStatus("host" + str(numberOfNodes - 1),"s1","up")
    net.pingAll()
    net.stop()
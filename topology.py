from mininet.topo import Topo
import sys
from mininet.net import Mininet                                                                        
from mininet.node import Controller
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
from mininet.link import TCLink
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

	print("Usage: python topology.py numberOfNodes lossRate")

	exit(-1)


numberOfNodes = int(sys.argv[1])
loss = float(sys.argv[2])

                                                                               
if __name__ == '__main__':
    net = Mininet( topo=SingleSwitchTopo(numberOfNodes, loss) , link = TCLink)
    net.start()
    host1 = net.get('host1')
    host2 = net.get('host2')
    host3 = net.get('host3')
    host4 = net.get('host4')
    host5 = net.get('host5')
    print host1.IP(), host2.IP(), host3.IP(), host4.IP(), host5.IP()
    response2 = host2.cmd('python MulticastReceiver.py 2 &')
    response3 = host3.cmd('python MulticastReceiver.py 3 &')
    response4 = host4.cmd('python MulticastReceiver.py 4 &')
    response5 = host5.cmd('python MulticastReceiver.py 5 &')
    sleep(10)

    response1 = host1.cmd('python MulticastSender.py 1 ' + str(numberOfNodes) +  ' ')
    #print response1
    #print response2
    #print response3
    #print response4
    #print response5
 #   print host1.cmd('ping 127.0.0.1')
#    print host2.cmd('ifconfig')
    #net.pingAll()
    #time.sleep(5)
    #net.configLinkStatus("host" + str(numberOfNodes - 1),"s1","down")
    #net.pingAll()
    #net.configLinkStatus("host" + str(numberOfNodes - 1),"s1","up")
    #net.pingAll()
    net.stop()

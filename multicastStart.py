from time import sleep

#Script that runs the MulticastSender.py, MulticastReceiver.py on the appropriate hosts(servers)

class multicastStart:

	def __init__(self, net, multicastInitiator, numberOfNodes, logicalClock, port):

		hosts = []
		
		for i in range(1,numberOfNodes+1):

			hosts.append(net.get('host' + str(i)))

	

		print hosts

		for i in range(1,numberOfNodes+1):

			if i != multicastInitiator:

				print 'python MulticastReceiver.py ' + str(i)  +  ' ' + str(numberOfNodes) + ' ' + str(multicastInitiator) + ' &'
				
				resp1  = hosts[i - 1].cmd('python MulticastReceiver.py ' + str(i)  +  ' ' + str(numberOfNodes) + ' ' + str(multicastInitiator) + ' ' + str(port) + ' &')

		sleep(0.25)		# Wait for receivers to be set up

		print 'python MulticastSender.py ' + str(multicastInitiator) + ' ' + str(numberOfNodes) + ' &'       

		resp = hosts[multicastInitiator - 1].cmd('python MulticastSender.py ' + str(multicastInitiator) + ' ' + str(numberOfNodes) + ' ' + str(logicalClock) + ' ' + str(port) + ' &')

		print resp
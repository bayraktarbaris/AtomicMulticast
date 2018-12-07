from time import sleep

class multicastStart:

	def __init__(self, net, multicastInitiator, numberOfNodes):

		hosts = []
		
		for i in range(1,numberOfNodes+1):

			hosts.append(net.get('host' + str(i)))

		multicastInitiator = 1

		print hosts

		for i in range(1,numberOfNodes+1):

			if i != multicastInitiator:

				print 'python MulticastReceiver.py ' + str(i) + ' ' + str(numberOfNodes) + ' &'
			
				hosts[i - 1].cmd('python MulticastReceiver.py ' + str(i) + ' ' + str(numberOfNodes) + ' &')

		sleep(0.25)		# Wait for receivers to be set up

		print 'python MulticastSender.py ' + str(multicastInitiator) + ' ' + str(numberOfNodes) + ' &'       

		hosts[multicastInitiator - 1].cmd('python MulticastSender.py ' + str(multicastInitiator) + ' ' + str(numberOfNodes) + ' &')
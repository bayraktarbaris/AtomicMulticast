class Message:

	def __init__(self, multicastSenderId, message, clockOfInitiator):

		self.multicastSenderId = multicastSenderId

		self.message = message 

		self.lastSender = "10.0.0." + multicastSenderId # By default it is not yet sent by someone other than multicastSender

		self.clockOfInitiator = clockOfInitiator

		self.fromChild = False

	def sentBySomeOneOtherThanMulticastSenderId(self, lastSender):	# Someone is forwarded the message that is not the multicastSender
	
		self.lastSender = lastSender	
						
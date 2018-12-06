class Message:

	def __init__(self, multicastSenderId, message):

		self.multicastSenderId = multicastSenderId

		self.message = message 

		self.lastSender = 0 # By default it is not yet sent by someone other than multicastSender

	def sentBySomeOneOtherThanMulticastSenderId(self, lastSender):	# Someone is forwarded the message that is not the multicastSender
	
		self.lastSender = lastSender	
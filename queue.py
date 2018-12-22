class Queue:
	def __init__(self, file_path):
		self.file_path = file_path
		f = open(self.file_path,'a+')
		f.close()
		self.queue = []

	def read(self):
		try:
			ret = []
			f = open(self.file_path, "r")
			for line in f:
				ret.append(" ".join(map(lambda x: x.strip(), line[1:-2].split(','))))
			f.close()
		except:
			pass
		return ret

	def write(self):
		f = open(self.file_path, "w+")
		for element in self.queue:
			f.write(str(element) + "\n")
		f.close()
		self.queue = []

	def pop(self):
		ret = self.read()
		popped = ret.pop(0)
		self.queue = ret
		self.write()
		return popped

	def append(self, element):
		ret = self.read()
		ret.append(element)
		ret = list(map(lambda x: [int(x.split()[0]), int(x.split()[1])], ret))
		sorted(ret, key = lambda x: (x[1], x[0]))
		self.queue = ret
		self.write()
		ret = self.read()
		return ret

"""
q = Queue("11.txt")
print q.read()
q.append('1')
q.append('2')
q.append('3')
print q.read()
q.append('4')
print q.read()
q.pop()
print q.read()
"""
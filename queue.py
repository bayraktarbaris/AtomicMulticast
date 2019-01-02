### Our queue implementation for simplicity in the code

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
				if line != "\n":
					ret.append(" ".join(map(lambda x: x.strip(), line[1:-2].split(','))))
			f.close()
		except:
			print("Exception")
		return ret

	def myWrite(self, pop):
		f = open(self.file_path, "w+")
		for element in self.queue:
			f.write(str(element) + "\n")	
		f.close()
		#self.queue = []

	def pop(self):
		ret = self.read()
		popped = ret.pop(0)
		tmp = []
		j = 0
		for i in range(len(ret)):
			m,n = (int(var) for var in ret[i].split(" "))
			e =  [m,n]
			tmp.append(e)
		self.queue = tmp
		self.myWrite(True)
		return popped

	def append(self, element):
		ret = self.read()
		ret.append(element)
		ret = list(map(lambda x: [int(x.split()[0]), int(x.split()[1])], ret))
		ret = sorted(ret, key = lambda x: (x[1], x[0]))
		self.queue = ret
		self.myWrite(False)
		ret = self.read()
		return ret

class HostMlNode:
	def __init__(self, name, data):
		self.name = name
		self.data = data

	def getAsDict(self):
		return {self.name: self.data}

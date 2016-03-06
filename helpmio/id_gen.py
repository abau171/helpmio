class IdGenerator:
	def __init__(self):
		self.next_id = 1
	def gen_id(self):
		return_id = self.next_id
		self.next_id += 1
		return return_id

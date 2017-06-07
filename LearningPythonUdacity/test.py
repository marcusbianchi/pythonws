class Animal:
	def __init__(self,name=""):
		self.name = name

	@property
	def name(self):
		print('gay')
		return self.__name





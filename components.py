from satellite import *
import time

class Clock(Component):
	def __init__(self):
		super(Clock, self).__init__(1, 'C')

	def tick(self):
		self.registers[0] = c_ushort(int(time.time())%BIGGEST)

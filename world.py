from random import random
import Queue
from bfcpu import *
from satellite import *
from components import *

class World(object):
	def __init__(self, width, height, depth):
		self.width = width
		self.height = height
		self.depth = depth

		self.sats = []

		self.radiobands = [Queue.Queue(32)]*32

		print "done"
	
	def radio(self, band, val):
		if not isinstance(band, int): raise Exception("Band should be integer.")
		if(abs(band)<len(self.radiobands)):
			self.radiobands[band].put_nowait(val)

	def getByAddr(self, addr):
		for sat in self.sats:
			if(sat.bios.address==addr): return sat
		return None

	def addRandom(self, x, y, z):
		cpu = BFCPU(512)

		#p = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
		p = "[.>.>,<<]" # continuously read radio
		d = [1, 0, 0]
		for i, c in enumerate(p):
			cpu.write(i, ord(c))
		for i, v in enumerate(d):
			cpu.write(128 + i, v)

		sat = Satellite(self, cpu, (x, y, z), (random(), random(), random()))
		cpu.bus.add(Radio(sat))

		self.sats.append(sat)

	def tick(self):
		for sat in self.sats:
			sat.tick()

		#for i in range(0, len(self.radiobands)):
		#	if not self.radiobands[i].empty():
		#		a = self.radiobands[i].get_nowait()

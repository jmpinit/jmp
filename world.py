from random import random

from bfcpu import *
from satellite import *

class World(object):
	def __init__(self, width, height, depth):
		self.width = width
		self.height = height
		self.depth = depth

		self.sats = []

	def getByAddr(self, addr):
		for sat in self.sats:
			if(sat.bios.address==addr): return sat
		return None

	def addRandom(self, x, y, z):
		cpu = BFCPU(512)

		p = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
		for i, c in enumerate(p):
			cpu.write(i, ord(c))

		sat = Satellite(cpu, (x, y, z), (random(), random(), random()))
		self.sats.append(sat)

	def tick(self):
		for sat in self.sats:
			sat.tick()

from abc import *
from ctypes import *
from satellite import *
import time

BIGGEST = 2**16

sprites = {}

class Component(object):
	def __init__(self, sat, numregs, sprite=[]):
		self.sat = sat

		self.sprite = sprite
		# add ourselves to the global list under this symbol
		if(self.sprite):
			pt = {}
			for s in self.sprite:
				pt[s] = self
			global sprites
			sprites.update(pt)

		self.registers = [c_ushort(0)] * numregs

	def read(self, addr):
		if(addr < 0): raise Exception("Component read: addresses should be greater than or equal to zero")
		if(addr<len(self.registers)):
			return self.registers[addr]
		else:
			return c_ushort(0)

	def write(self, addr, val):
		if(addr < 0): raise Exception("Component read: addresses should be greater than or equal to zero")
		if(addr<len(self.registers)):
			if not isinstance(val, c_ushort): val = c_ushort(val)
			self.registers[addr] = c_ushort(val.value%BIGGEST)

	@abstractmethod
	def tick(self):
		return


class Clock(Component):
	def __init__(self, sat):
		super(Clock, self).__init__(sat, 1, ['C'])

	def tick(self):
		self.registers[0] = c_ushort(int(time.time())%BIGGEST)


class SolarPanel(Component):
	def __init__(self, sat):
		super(SolarPanel, self).__init__(sat, 1, ['#'])

	def tick(self):
		self.registers[0] = c_ushort(self.power())

	def power(self):
		# TODO
		return 0xFF


class Thruster(Component):
	def __init__(self, sat):
		super(Thruster, self).__init__(sat, 3, ['>'])
		self.thrustscale = 1.0

	def tick(self):
		self.sat.vx += self.thrustscale*c_short(self.registers[0].value).value/float(2**15);
		self.sat.vy += self.thrustscale*c_short(self.registers[1].value).value/float(2**15);
		self.sat.vz += self.thrustscale*c_short(self.registers[2].value).value/float(2**15);

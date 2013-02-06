from abc import *
import Queue
from ctypes import *
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


# capable of generating a satellite from a schematic
class MOV:
	def __init__(self, sat):
		self.sat = sat


class CPU(Component):
	def __init__(self, ramsize):
		self.paused = False

		self.data = [c_ushort(0)] * ramsize
		self.pc = 0

		self.bus = None

	def start(self):
		self.paused = False
	
	def stop(self):
		self.paused = True

	def read(self, addr):
		return self.data[addr % len(self.data)]

	def write(self, addr, val):
		if not isinstance(val, c_ushort): val = c_ushort(int(val))
		self.data[addr % len(self.data)] = val

	@abstractmethod
	def tick(self):
		"""move the simulation forward one step"""
		return


class BusController(object):
	def __init__(self):
		self.slaves = []
	
	def read(self, device_addr, reg_addr):
		if device_addr<len(self.slaves):
			return self.slaves[device_addr].read(reg_addr)
		else:
			return 0

	def write(self, device_addr, reg_addr, val):
		if not isinstance(val, c_ushort): val = c_ushort(val)
		
		if device_addr<len(self.slaves):
			self.slaves[device_addr].write(reg_addr, val)

	# clocks all hardware on the bus
	def tick(self):
		for slave in self.slaves:
			slave.tick()

	# add a slave
	def add(self, slave):
		self.slaves.append(slave)


class Clock(Component):
	def __init__(self, sat):
		super(Clock, self).__init__(sat, 1, ['C'])

	def tick(self):
		self.registers[0] = c_ushort(int(time.time())%BIGGEST)

# FIFO buffered radio
# register 0 = received data
# register 1 = data to send
# register 2 = band
# register 3 = clear
class Radio(Component):
	def __init__(self, sat):
		super(Radio, self).__init__(sat, 4, ['R'])
		self.buf = Queue.Queue()
	
	# hook reading to update the buffer
	def read(self, addr):
		val = super(Radio, self).read(addr)
		if(addr == 0):
			if(not self.buf.empty()):
				self.registers[0] = self.buf.get_nowait()
			else:
				self.registers[0] = 0
		return val

	def write(self, addr, val):
		super(Radio, self).write(addr, val)

	def tick(self):
		# read from old radiobands
		if not self.sat.world.radiobands[self.registers[2].value].empty():
			print "i see in queue"
			val = self.sat.world.radiobands[self.registers[2].value].get_nowait()
			self.sat.world.radiobands[self.registers[2].value].put_nowait(val)
			print val
			self.buf.put_nowait(val)

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

from ctypes import *
import abc

BIGGEST = 2**16

class Satellite(object):
	def __init__(self, cpu, pos, vel):
		# hardware things
		self.bios = SatBIOS(self)
		self.cpu = cpu
		self.mov = MOV(self)

		# world
		self.x = pos[0]
		self.y = pos[1]
		self.z = pos[2]

		self.vx = vel[0]
		self.vy = vel[1]
		self.vz = vel[2]

		self.paused = True

	def tick(self):
		if(not self.paused):
			self.cpu.tick()

	def start(self):
		self.paused = False
	
	def stop(self):
		self.paused = True


class SatBIOS:
	def __init__(self, sat):
		self.sat = sat


class MOV:
	def __init__(self, sat):
		self.sat = sat


class Component(object):
	def __init__(self, numregs, sprite=' '):
		self.sprite = sprite
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
			self.registers[addr] = val%BIGGEST

class CPU(Component):
	def __init__(self, ramsize):
		self.data = [c_ushort(0)] * ramsize
		self.pc = 0

		self.bus = None

	def read(self, addr):
		return self.data[addr % len(self.data)]

	def write(self, addr, val):
		if not isinstance(val, c_ushort): val = c_ushort(val)
		self.data[addr % len(self.data)] = val

	@abc.abstractmethod
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
		if not isinstance(device_addr, c_ushort) or not isinstance(reg_addr, c_ushort) or not isinstance(val, c_ushort):
			raise Exception("Arguments must be shorts.")
		
		if device_addr<len(self.slaves):
			self.slaves[device_addr].write(reg_addr, val)

	# clocks all hardware on the bus
	def tick(self):
		for slave in self.slaves:
			slave.tick()

	# add a slave
	def add(self, slave):
		self.slaves.append(slave)

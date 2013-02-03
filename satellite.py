from components import Component
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

		self.fx = pos[0]
		self.fy = pos[1]
		self.fz = pos[2]

		self.vx = vel[0]
		self.vy = vel[1]
		self.vz = vel[2]

	def tick(self):
		# laws of physics
		if(self.vx>1): self.vx = 1
		if(self.vx<-1): self.vx = -1
		if(self.vy>1): self.vy = 1
		if(self.vy<-1): self.vy = -1
		if(self.vz>1): self.vz = 1
		if(self.vz<-1): self.vz = -1

		# move
		self.fx += self.vx
		self.fy += self.vy
		self.fz += self.vz

		self.x = int(self.fx)
		self.y = int(self.fy)
		self.z = int(self.fz)

		self.cpu.tick()


class SatBIOS:
	def __init__(self, sat):
		self.sat = sat

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

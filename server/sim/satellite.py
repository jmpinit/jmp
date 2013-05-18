from components.base import *

from ctypes import *
import abc

BIGGEST = 2**16

class Satellite(object):
	def __init__(self, world, cpu, pos, vel):
		self.world = world

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
		self.address = "0000000000000000" # TODO make 64 bit instead of string
		self.sat = sat

	def start(self):
		self.sat.cpu.start()

	def stop(self):
		self.sat.cpu.stop()

	def peek(self, addr):
		return self.sat.cpu.read(addr)

	def poke(self, addr, val):
		self.sat.cpu.write(addr, val)

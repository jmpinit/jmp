from satellite import *
import collections
import time
from sys import stdout
from ctypes import *

class BFCPU(CPU):
	instructions = ['>', '<', '+', '-', '.', ',', '[', ']']

	def __init__(self, ramsize):
		self.sprite = 'B'

		super(BFCPU, self).__init__(ramsize)
		self.dc = 128

		self.bus = BFCPU_Bus()

		self.ops = [self.right, self.left, self.inc, self.dec, self.out, self.into, self.jmpzero, self.jmpnonzero]

	def tick(self):
		self.bus.tick()

		# execute the next instruction
		instr = chr(self.read(self.pc).value)

		# execute if known, nop otherwise
		if instr in BFCPU.instructions:
			self.ops[BFCPU.instructions.index(instr)]()

		self.pc += 1

		if(self.pc>=128):
			print "into data"
			exit()

	def reset():
		super(BFCPU, self).__init__(len(self.data))
		self.dc = 128

	# instructions
	def right(s):	s.dc += 1; #print "> "+str(s.dc)
	def left(s):	s.dc -= 1; ##print "< "+str(s.dc)
	def inc(s):		s.write(s.dc, s.read(s.dc).value+1); #print "+ "+str(s.read(s.dc))
	def dec(s):		s.write(s.dc, s.read(s.dc).value-1); #print "- "+str(s.read(s.dc))
	# def out(s):		stdout.write(chr(s.read(s.dc).value)); #print "out!"
	# def into(s):	s.write(s.dc, ord(raw_input()[0]));
	def out(s):		s.bus.tx(s.read(s.dc).value); #print "out!"
	def into(s):	s.write(s.dc, s.bus.rx()); print str(s.read(s.dc))
	def jmpzero(s):
		#print "["
		unmatched = 0
		if s.read(s.dc)==0:
			while(True):
				s.pc += 1
				curr = chr(s.read(s.pc))
				if(curr=='['): unmatched += 1
				if(curr==']'):
					if(unmatched > 0):
						unmatched -= 1
					else:
						break

	def jmpnonzero(s):
		#print "]"
		unmatched = 0
		if not s.read(s.dc).value==0:
			while(True):
				s.pc -= 1
				curr = chr(s.read(s.pc).value)
				if(curr==']'): unmatched += 1
				if(curr=='['):
					if(unmatched > 0):
						unmatched -= 1
					else:
						break

class BFCPU_Bus(BusController):
	def __init__(self):
		super(BFCPU_Bus, self).__init__()
		self.buf = collections.deque([])
		self.state = 'CMD'

		self.addr = 0

	def tx(self, val):
		if(self.state == 'CMD'):
			if(val == 0):
				self.clear()
			elif(val == 1):
				self.state = 'READ'
			elif(val == 2):
				self.state = 'WRITE'
		elif(self.state == 'READ'):
			self.buf.append(self.read((val&0xFF00)>>8, val&0xFF))
		elif(self.state == 'WRITE_ADDR'):
			self.addr = val
			self.state = 'WRITE_VAL'
		elif(self.state == 'WRITE_VAL'):
			self.buf.append(self.write((self.addr&0xFF00)>>8, self.addr&0xFF, val))
			self.state = 'CMD'

	def rx(self):
		val = self.buf[0]
		self.buf.rotate(-1)
		del self.buf[-1]
		return val

	def clear(self):
		del self.buf[:] 
		self.state = 'CMD'

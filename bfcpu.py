from satellite import *
from sys import stdout

class BFCPU(CPU):
	instructions = ['>', '<', '+', '-', '.', ',', '[', ']']

	def __init__(self, ramsize):
		self.sprite = 'B'

		super(BFCPU, self).__init__(ramsize)
		self.dc = 128

		self.ops = [self.right, self.left, self.inc, self.dec, self.out, self.into, self.jmpzero, self.jmpnonzero]

	def tick(self):
		# execute the next instruction
		instr = chr(self.read(self.pc))

		# execute if known, nop otherwise
		if instr in BFCPU.instructions:
			self.ops[BFCPU.instructions.index(instr)]()

		self.pc += 1

		if(self.pc>=128):
			exit()

	def reset():
		super(BFCPU, self).__init__(len(self.data))
		self.dc = 128

	# instructions
	def right(s):	s.dc += 1;
	def left(s):	s.dc -= 1;
	def inc(s):		s.write(s.dc, s.read(s.dc)+1);
	def dec(s):		s.write(s.dc, s.read(s.dc)-1);
	def out(s):		stdout.write(chr(s.read(s.dc)));
	def into(s):	s.write(s.dc, ord(raw_input()[0]));
	def jmpzero(s):
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
		unmatched = 0
		if not s.read(s.dc)==0:
			while(True):
				s.pc -= 1
				curr = chr(s.read(s.pc))
				if(curr==']'): unmatched += 1
				if(curr=='['):
					if(unmatched > 0):
						unmatched -= 1
					else:
						break

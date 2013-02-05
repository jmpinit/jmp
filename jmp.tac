from twisted.application.internet import TCPServer
from twisted.application.service import Application

from twisted.conch.insults import insults
from twisted.conch.insults.helper import CharacterAttribute
from twisted.conch.insults.text import flatten, attributes as A
from twisted.conch.telnet import TelnetTransport, TelnetProtocol

from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver

from twisted.internet.task import LoopingCall

from world import *

world = World(128, 128, 32)

class JMPServerTelnet(TelnetProtocol, insults.TerminalProtocol, LineReceiver):
	delimiter = '\n'

	def __init__(self):
		self.commands = {
				'connect':self.connect,
				'peek':self.peek,
				'poke':self.poke,
				'start':self.start,
				'stop':self.stop,
				'dump':self.dump,
				'rxtx':self.rxtx
		}

	def success(self, msg):
		self.terminal.write(flatten(A.fg.green[msg+'\n\r'], CharacterAttribute()))

	def error(self, msg):
		self.terminal.write(flatten(A.fg.red[msg+'\n\r'], CharacterAttribute()))

	def printn(self, msg):
		self.terminal.write(flatten(msg, CharacterAttribute()))

	def rxtx(self, argument):
		argument = argument.replace(" ", "")
		if(len(argument)==4):
			self.band = int(argument, 16)
			self.state = 'RXTX'
			self.terminal.write('=>')
		else:
			self.error("error. usage: rxtx <4 character frequency (hex)>")
	
	def telnet_RXTX(self, data):
		self.clearFormatting()

		if(data=='`'):
			self.state = 'CMD'
		else:
			for c in data:
				if c == '\r' or c == '\n': world.radio(self.band, ord(c))
				if ord(c) >= 32 and ord(c) <= 127: world.radio(self.band, ord(c))
		self.terminal.write('=>')

	def start(self, argument):
		if(len(argument)==0):
			sat = self.target
			if not sat:
				self.error("error. not connected to satellite. use the connect command.")
			else:
				sat.bios.start()
				self.success("satellite cpu ticking.")
		else:
			self.error("error. usage: start")

	def stop(self, argument):
		if(len(argument)==0):
			sat = self.target
			if not sat:
				self.error("error. not connected to satellite. use the connect command.")
			else:
				sat.bios.stop()
				self.success("satellite cpu stopped.")
		else:
			self.error("error. usage: stop")

	def peek(self, argument):
		parts = argument.split(" ")
		if(len(parts)==1):
			try:
				address = int(parts[0])
			except:
				self.error("error. usage: peek <16 bit address>")
			
			sat = self.target
			if not sat:
				self.error("error. not connected to satellite. use the connect command.")
			else:
				self.success("value=%0.4X" % sat.bios.peek(address).value)
		else:
			self.error("error. usage: peek <16 bit address>")

	def poke(self, argument):
		parts = argument.split(" ")
		if(len(parts)==2):
			try:
				address = int(parts[0])
				value = int(parts[1])
			except:
				self.error("error. usage: poke <16 bit address> <16 bit data>")
			
			sat = self.target
			if not sat:
				self.error("error. not connected to satellite. use the connect command.")
			else:
				sat.bios.poke(address, value)
				self.success("poked the satellite.")
		else:
			self.error("error. usage: poke <16 bit address> <16 bit data>")

	def dump(self, argument):
		parts = argument.split(" ")
		if(len(parts)==2):
			try:
				address = int(parts[0])
				length = int(parts[1])
			except:
				self.error("error. usage: dump <start address> <length>")

			sat = self.target
			if not sat:
				self.error("error. not connected to satellite. use the connect command.")
			else:
				self.terminal.write(flatten(A.fg.blue["PC  | ", A.fg.green["%0.4X" % sat.cpu.pc]], CharacterAttribute()))
				if(not sat.cpu.paused):
					self.terminal.write(flatten(A.bold[" RUNNING"], CharacterAttribute())) 
					self.clearFormatting()
				self.terminal.write("\n\r")
				self.terminal.write(flatten(A.fg.blue["ADDR| DATA                                     | ASCII\n\r"], CharacterAttribute()))
				self.terminal.write(flatten(A.fg.blue["=========================================================\n\r"], CharacterAttribute()))
				
				for section in range(address, address+length, 8):
					self.terminal.write(flatten(A.fg.blue["%0.4X| " % section], CharacterAttribute()))
					for i in range(0, 8):
						if sat.cpu.pc == section+i:
							self.terminal.write(flatten(A.fg.magenta["%0.4X " % sat.bios.peek(section+i).value], CharacterAttribute()))
						else:
							self.terminal.write(flatten(A.fg.green["%0.4X " % sat.bios.peek(section+i).value], CharacterAttribute()))
					self.terminal.write(flatten(A.fg.blue["| "], CharacterAttribute()))
					for i in range(0, 8):
						c = sat.bios.peek(section+i).value
						if(c>=32 and c<=126):
							if sat.cpu.pc == section+i:
								self.terminal.write(flatten(A.fg.magenta[chr(c)], CharacterAttribute()))
							else:
								if sat.cpu.pc == section+i:
									self.terminal.write(flatten(A.fg.magenta[chr(c)], CharacterAttribute()))
								else:
									self.terminal.write(flatten(A.fg.green[chr(c)], CharacterAttribute()))
						else:
							self.terminal.write(flatten(A.fg.green["."], CharacterAttribute()))
					self.terminal.write(flatten(A.fg.green["\n\r"], CharacterAttribute()))
		else:
			self.error("error. usage: dump <start address> <length>")

	def connect(self, argument):
		argument = argument.replace(" ", "")
		if(len(argument)==16):
			sat = world.getByAddr(argument)
			if not sat:
				self.error("error. no sat at address.")
			else:
				self.success("success. connected to satellite.")
				self.target = sat
		else:
			self.error("error. usage: connect <16 character address (hex)>")

	def parse(self, line):
		parts = line.split(' ')
		
		try:
			self.commands[parts[0]](' '.join(parts[1:]))
		except KeyError:
			self.error("error. syntax")

	"""UTILITIES"""
	def clearFormatting(self):
		self.terminal.write("\033[0m")

	"""COMM FUNCTIONS"""
	def connectionMade(self):
		self.terminal.write("WELCOME TO THE JMPSERVER\n\r")

		world.addRandom(0, 0, 0)
		print "there are "+str(len(world.sats))+" satellites"
		self.target = None

		self.terminal.write("satellite generated\n\r")

		self.terminal.write("> ")
		self.state = 'CMD'

	def lineReceived(self, line):
		getattr(self, 'telnet_' + self.state)(line)

	def telnet_CMD(self, line):
		self.parse(line)
		if(self.state == 'CMD'):
			self.clearFormatting();
			self.terminal.write("> ")

manager = LoopingCall(world.tick)
manager.start(1)

factory = ServerFactory()
factory .protocol = lambda: TelnetTransport(JMPServerTelnet)
the_server = TCPServer(9999, factory)

application = Application("JMP")
the_server.setServiceParent(application)

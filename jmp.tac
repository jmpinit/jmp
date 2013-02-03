from twisted.application.internet import TCPServer
from twisted.application.service import Application

from twisted.conch.insults import insults
from twisted.conch.insults.helper import CharacterAttribute
from twisted.conch.insults.text import flatten, attributes as A
from twisted.conch.telnet import TelnetTransport, TelnetProtocol

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

from world import *

world = World(128, 128, 32)

class TelnetTest(TelnetProtocol, insults.TerminalProtocol, LineReceiver):
	delimiter = '\n'

	def __init__(self):
		self.commands = {'connect':self.connect, 'dump':self.dump, 'rxtx':self.rxtx}

	def success(self, msg):
		self.terminal.write(flatten(A.fg.green[msg+'\n\r'], CharacterAttribute()))

	def error(self, msg):
		self.terminal.write(flatten(A.fg.red[msg+'\n\r'], CharacterAttribute()))

	def printn(self, msg):
		self.terminal.write(flatten(msg, CharacterAttribute()))

	def rxtx(self, argument):
		argument = argument.replace(" ", "")
		if(len(argument)==16):
			self.error("error. rxtx tool doesn't exist!")
		else:
			self.error("error. rxtx: connect <4 character frequency (hex)>")

	def dump(self, argument):
		argument = argument.replace(" ", "")
		if(len(argument)==0):
			sat = self.target
			if not sat:
				self.error("error. not connected to satellite. use the connect command.")
			else:
				self.terminal.write(flatten(A.fg.blue["ADDR| DATA                                     | ASCII\n\r"], CharacterAttribute()))
				self.terminal.write(flatten(A.fg.blue["=========================================================\n\r"], CharacterAttribute()))
				
				for section in range(0, 512, 8):
					self.terminal.write(flatten(A.fg.blue["%0.4X| " % section], CharacterAttribute()))
					for i in range(0, 8):
						self.terminal.write(flatten(A.fg.green["%0.4X " % sat.bios.peek(section+i).value], CharacterAttribute()))
					self.terminal.write(flatten(A.fg.blue["| "], CharacterAttribute()))
					for i in range(0, 8):
						c = sat.bios.peek(section+i).value
						if(c>=32 and c<=126):
							self.terminal.write(flatten(A.fg.green[chr(c)], CharacterAttribute()))
						else:
							self.terminal.write(flatten(A.fg.green["."], CharacterAttribute()))
					self.terminal.write(flatten(A.fg.green["\n\r"], CharacterAttribute()))
		else:
			self.error("error. usage: dump")

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

		self.terminal.write("satellite generated\n\r")

		self.terminal.write("> ")
		self.state = 'CMD'

	def lineReceived(self, line):
		getattr(self, 'telnet_' + self.state)(line)

	def telnet_CMD(self, line):
		self.parse(line)
		self.clearFormatting();
		self.terminal.write("> ")

factory = ServerFactory()
factory .protocol = lambda: TelnetTransport(TelnetTest)
the_server = TCPServer(9999, factory)

application = Application("JMP")
the_server.setServiceParent(application)

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
		self.commands = {'connect':self.connect, 'rxtx':self.rxtx}

	def error(self, msg):
		self.terminal.write(flatten(A.fg.red[msg+'\n\r'], CharacterAttribute()))

	def rxtx(self, argument):
		argument = argument.replace(" ", "")
		if(len(argument)==16):
			self.error("error. rxtx tool doesn't exist!")
		else:
			self.error("error. rxtx: connect <4 character frequency (hex)>")

	def connect(self, argument):
		argument = argument.replace(" ", "")
		if(len(argument)==16):
			self.error("error. connect tool doesn't exist!")
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

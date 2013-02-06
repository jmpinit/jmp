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

from ansi import Ansi
from cmds import *
from world import *

world = World(128, 128, 32)

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class JMPServerTelnet(TelnetProtocol, insults.TerminalProtocol, LineReceiver):
	delimiter = '\n'

	def __init__(self):
		self.commands = {
			'connect':connect.Connect,
			'dump':hexdump.Hexdump,
			'man':man.Man,
			'peek':peek.Peek,
			'poke':poke.Poke,
			'rxtx':rxtx.Rxtx,
			'start':start.Start,
			'stop':stop.Stop,
		}


	def connectionMade(self):
		self.ansi = Ansi(self.terminal)
		self.player = Bunch(world = world, sat = world.addRandom(0, 0, 0))

		for cmdkey in self.commands.keys():
			self.commands[cmdkey] = self.commands[cmdkey](self.player, self.ansi)

		self.ansi.out("WELCOME TO THE JMPSERVER\n\r")

		print "there are "+str(len(world.sats))+" satellites"

		self.ansi.out("satellite generated\n\r")

		self.ansi.out("> ")
		self.state = 'CMD'

	def lineReceived(self, line):
		getattr(self, 'telnet_' + self.state)(line)

	def telnet_CMD(self, line):
		parts = line.split(" ")

		try:
			bin = self.commands[parts[0]]
			bin.execute(parts[1])
		except KeyError:
			self.ansi.out("unrecognized")

		if(self.state == 'CMD'):
			self.ansi.clear();
			self.ansi.out("> ")

manager = LoopingCall(world.tick)
manager.start(1)

factory = ServerFactory()
factory .protocol = lambda: TelnetTransport(JMPServerTelnet)
the_server = TCPServer(9999, factory)

application = Application("JMP")
the_server.setServiceParent(application)

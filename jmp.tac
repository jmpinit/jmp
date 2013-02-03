from twisted.application.internet import TCPServer
from twisted.application.service import Application

from twisted.conch.insults import insults
from twisted.conch.insults.helper import CharacterAttribute
from twisted.conch.insults.text import flatten, attributes as A
from twisted.conch.telnet import TelnetTransport, TelnetProtocol

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver


class TelnetTest(TelnetProtocol, insults.TerminalProtocol, LineReceiver):
    delimiter = '\n'

    def parse(self, line):
        self.terminal.write(line)

    def connectionMade(self):
        self.terminal.write("WELCOME TO THE JMPSERVER")
        self.terminal.write("> ")
        self.state = 'CMD'

    def lineReceived(self, line):
        getattr(self, 'telnet_' + self.state)(line)

    def telnet_CMD(self, line):
        self.parse(line)

factory = ServerFactory()
factory .protocol = lambda: TelnetTransport(TelnetTest)
the_server = TCPServer(9999, factory)

application = Application("JMP")
the_server.setServiceParent(application)

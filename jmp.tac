from twisted.conch.insults import insults

from twisted.internet.protocol import ServerFactory
from twisted.application.service import Application
from twisted.application.internet import TCPServer
from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from twisted.protocols.basic import LineReceiver


class TelnetTest(TelnetProtocol, insults.TerminalProtocol, LineReceiver):
    delimiter = '\n'

    def connectionMade(self):
        self.terminal.write("hello")

factory = ServerFactory()
factory .protocol = lambda: TelnetTransport(TelnetTest)
the_server = TCPServer(9999, factory)

application = Application("JMP")
the_server.setServiceParent(application)

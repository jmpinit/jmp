import command
from command import Cmd

man = {
	'NAME':'rxtx - transmit and receive isotropically on a specified radio band.',
	'SYNOPSIS':'rxtx [-h] band',
	'DESCRIPTION':'rxtx allows two-way communication on the 2^16 unencryped radio bands permeating space. It is a raw interface and does not implement any form of encryption or noise cancellation.',
	'OPTIONS': {
		'-h':'prints info about the command',
	}
}

class Rxtx(Cmd):
	def __init__(self, player, ansi): super(type(self), self).__init__(player, ansi); self.man = man

	def execute(self, arguments):
		if(not super(type(self), self).execute(arguments)): return

		try:
			band = int(self.args[0], 0)
		except:
			self.error("invalid argument(s)")

		while(True):
			msg = self.ansi.input("> ")

			if msg == '`': break

			for c in msg:
				self.player.world.tx(int(c_ushort(c)))


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
	def execute(self, arguments):
		sat = self.player.sat
		bios = sat.bios

		if not sat:
			self.error("not connected to satellite")
			return

		cleaned = command.decode(arguments)
		opts = cleaned['options']
		args = cleaned['args']

		if opts['h']:
			self.out(man['SYNOPSIS']+'\n\r')
			return

		try:
			band = int(args[0], 0)
		except:
			self.error("invalid argument(s)")

		while(True):
			msg = self.ansi.input("> ")

			if msg == '`': break

			for c in msg:
				self.player.world.tx(int(c_ushort(c)))


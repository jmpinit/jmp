import command
from command import SatCmd

man = {
	'NAME':'peek - print hexadecimal or ASCII representations of satellite memory at a specific address.',
	'SYNOPSIS':'peek [-AhH] address',
	'DESCRIPTION':'peek uses the SatBIOS of the currently connected satellite to dump the specified memory from the satellite CPU in human-readable form.',
	'OPTIONS': {
		'-A':'prints only the ASCII form',
		'-h':'prints info about the command',
		'-H':'prints only the hex form',
	}
}

class Peek(SatCmd):
	def __init__(self, player, ansi): super(type(self), self).__init__(player, ansi); self.man = man

	def execute(self, arguments):
		if(not super(type(self), self).execute(arguments)): return

		try:
			address = int(self.args[0], 0)
		except(IndexError):
			self.error("invalid argument(s)")
			return

		v = self.player.sat.bios.peek(address).value

		if(not 'A' in self.opts and not 'H' in self.opts):
			self.out("%0.4X\r\n" % v)
			if(v>=32 and v<=126):
				self.out("ASCII: "+chr(v)+"\n\r")
			else:
				self.out("ASCII: nonprintable\n\r")
		else:
			# print hex
			if('H' in self.opts): self.out("%0.4X\r\n" % v)

			if 'A' in self.opts:
				# printable?
				if(v>=32 and v<=126):
					self.out("ASCII: \n\r"+chr(v))
				else:
					self.out("ASCII: nonprintable\n\r")

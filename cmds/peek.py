import command
from command import Cmd

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

class Peek(Cmd):
	def execute(self, arguments):
		sat = self.player.sat
		bios = sat.bios

		if not sat:
			self.error("not connected to satellite")
			return

		cleaned = command.decode(arguments)
		opts = cleaned['options']
		args = cleaned['args']

		try:
			address = int(args[0], 0)
		except:
			self.error("invalid argument(s)")
			return

		v = bios.peek(address).value

		# print hex
		if(opts['H']): self.out("%0.4X\r\n" % v)

		# printable?
		if(v>=32 and v<=126):
			self.out("ASCII: \n\r"+chr(v))
		else:
			self.out("ASCII: nonprintable\n\r")

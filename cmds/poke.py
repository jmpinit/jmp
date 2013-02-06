import command
from command import Cmd

man = {
	'NAME':'poke - set the value of satellite memory at a specific address.',
	'SYNOPSIS':'poke [-AhH] address value',
	'DESCRIPTION':'poke uses the SatBIOS of the currently connected satellite to set the specified memory from the satellite.',
	'OPTIONS': {
		'-A':'set to an ASCII character',
		'-h':'prints info about the command',
		'-H':'prints only the hex form',
	}
}

class Poke(Cmd):
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

		if(opts['A']):
			try:
				address = int(args[0], 0)
				value = args[1]
				if(not len(value)==1):
					raise
			except:
				self.error("invalid argument(s)")
				return
		else:
			try:
				address = int(args[0], 0)
				value = int(args[1], 0)
			except:
				self.error("invalid argument(s)")
				return

		bios.poke(address, value)

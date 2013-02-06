import command
from command import SatCmd

man = {
	'NAME':'poke - set the value of satellite memory at a specific address.',
	'SYNOPSIS':'poke [-Ah] address value',
	'DESCRIPTION':'poke uses the SatBIOS of the currently connected satellite to set the specified memory from the satellite.',
	'OPTIONS': {
		'-A':'set to an ASCII character',
		'-h':'prints info about the command',
	}
}

class Poke(SatCmd):
	def __init__(self, player, ansi): super(type(self), self).__init__(player, ansi); self.man = man

	def execute(self, arguments):
		if(not super(type(self), self).execute(arguments)): return

		if('A' in self.opts):
			try:
				address = int(self.args[0], 0)
				value = self.args[1]
				if(not len(value)==1):
					raise
				value = ord(value)
			except:
				self.error("invalid argument(s)")
				return
		else:
			try:
				address = int(self.args[0], 0)
				value = int(self.args[1], 0)
			except:
				self.error("invalid argument(s)")
				return

		self.player.sat.bios.poke(address, value)

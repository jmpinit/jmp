import command
from command import Cmd

man = {
	'NAME':'connect - connects to a known satellite\'s SatBIOS given the satellite\'s unique address.',
	'SYNOPSIS':'connect [-h] address',
	'DESCRIPTION':'connects to a known satellite\'s SatBIOS. Takes advantage of the standardized recovery system present on most satellites in orbit. Once the connection is made the target satellite can be manipulated in many interesting ways. Expects the address to be expressed as a 64 bit hexadecimal number.',
	'OPTIONS': {
		'-h':'prints info about the command',
	}
}

class Connect(Cmd):
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
			address = int(args[0], 16)
		except:
			self.error("invalid argument(s)")
			return

		self.player.sat = self.player.world.getByAddress(address)

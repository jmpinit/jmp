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
	def __init__(self, player, ansi): super(type(self), self).__init__(player, ansi); self.man = man

	def execute(self, arguments):
		if(not super(type(self), self).execute(arguments)): return

		sat = self.player.sat
		bios = sat.bios

		address = int(self.args[0], 16)
		try:
			address = int(self.args[0], 16)
		except:
			self.error("invalid argument(s)")
			return

		self.player.sat = self.player.world.getByAddress(address)

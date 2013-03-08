import command
from command import SatCmd

man = {
	'NAME':'regdump - print hexadecimal representation of satellite CPU\'s registers.',
	'SYNOPSIS':'regdump [-hP]',
	'DESCRIPTION':'regdump uses the SatBIOS of the currently connected satellite to dump the current state of the registers from the satellite CPU in human-readable form.',
	'OPTIONS': {
		'-h':'prints info about the command',
		'-P':'prints only the PC'
	}
}

class Regdump(SatCmd):
	def __init__(self, player, ansi): super(type(self), self).__init__(player, ansi); self.man = man

	def execute(self, arguments):
		if(not super(type(self), self).execute(arguments)): return

		sat = self.player.sat

		if('P' in self.opts):
			self.out("%0.4X\r\n" % sat.cpu.pc)
			return

		v = sat.bios.peek(section+i).value

		for key in sat.cpu.registers.keys():
			# print hex
			self.out(key+"=%0.4X\r\n" % sat.cpu.registers[key])

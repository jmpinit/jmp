import command
from command import Cmd

man = {
	'NAME':'regdump - print hexadecimal representation of satellite CPU\'s registers.',
	'SYNOPSIS':'regdump [-hP]',
	'DESCRIPTION':'regdump uses the SatBIOS of the currently connected satellite to dump the current state of the registers from the satellite CPU in human-readable form.',
	'OPTIONS': {
		'-h':'prints info about the command',
		'-P':'prints only the PC'
	}
}

class Regdump(Cmd):
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

		if(opts['P']):
			self.out("%0.4X\r\n" % sat.cpu.pc)
			return

		v = bios.peek(section+i).value

		for key in sat.cpu.registers.keys():
			# print hex
			self.out(key+"=%0.4X\r\n" % sat.cpu.registers[key])

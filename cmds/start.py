import command
from command import Cmd

man = {
	'NAME':'start - starts clocking the CPU on the connected satellite.',
	'SYNOPSIS':'start [-h]',
	'DESCRIPTION':'starts clocking the CPU on the connected satellite.',
	'OPTIONS': {
		'-h':'prints info about the command',
	}
}

class Start(Cmd):
	def execute(self, arguments):
		sat = self.player.sat
		bios = sat.bios

		if not sat:
			self.error("not connected to satellite")
			return

		cleaned = command.decode(arguments)
		opts = cleaned['options']
		args = cleaned['args']

		sat.cpu.start()

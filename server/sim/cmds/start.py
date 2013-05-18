import command
from command import SatCmd

man = {
	'NAME':'start - starts clocking the CPU on the connected satellite.',
	'SYNOPSIS':'start [-h]',
	'DESCRIPTION':'starts clocking the CPU on the connected satellite.',
	'OPTIONS': {
		'-h':'prints info about the command',
	}
}

class Start(SatCmd):
	def __init__(self, player, ansi): super(type(self), self).__init__(player, ansi); self.man = man

	def execute(self, arguments):
		if(not super(type(self), self).execute(arguments)): return

		sat.cpu.start()

import command
from command import SatCmd

man = {
	'NAME':'stop - stops clocking the CPU on the connected satellite.',
	'SYNOPSIS':'stop [-h]',
	'DESCRIPTION':'stop clocking the CPU on the connected satellite.',
	'OPTIONS': {
		'-h':'prints info about the command',
	}
}

class Stop(SatCmd):
	def __init__(self, player, ansi): super(type(self), self).__init__(player, ansi); self.man = man

	def execute(self, arguments):
		if(not super(type(self), self).execute(arguments)): return

		sat.cpu.stop()

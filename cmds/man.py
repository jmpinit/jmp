import cmds
import sys
import command
from command import Cmd

man = {
	'NAME':'man - prints extended information about commands.',
	'SYNOPSIS':'man [-h] command',
	'DESCRIPTION':'.',
	'OPTIONS': {
		'-h':'prints info about the command',
	}
}

class Man(Cmd):
	def printdict(self, m, level = 0):
		for key in m.keys():
			self.out(('\t'*level)+key+':\n\r')
			if type(m[key]) == dict:
				self.printdict(m[key], level + 1)
			else:
				self.out(('\t'*level)+'\t'+str(m[key])+'\n\r')

	def execute(self, arguments):
		sat = self.player.sat
		bios = sat.bios

		if not sat:
			self.error("not connected to satellite")
			return

		cleaned = command.decode(arguments)
		opts = cleaned['options']
		args = cleaned['args']

		# get the command
		try:
			cmd = getattr(cmds, args[0])
			if(cmd): self.printdict(cmd.man)
		except AttributeError:
			self.error("unknown command")


from abc import *
import shlex

man = {
	'NAME':'',
	'SYNOPSIS':'',
	'DESCRIPTION':'',
	'OPTIONS': {
		'-h':'prints info about the command.'
	},
	'CAT':'',
	'BUGS':''
}

# breaks string into individual options and arguments
def decode(raw):
	tokens = shlex.split(raw)

	opts = []
	args = []
	for t in tokens:
		if(t.startswith('-')):
			opts.append(t[1:])
		else:
			args.append(t)

	return {'options':opts, 'args':args}


class Cmd(object):
	def __init__(self, player, ansi):
		self.player = player	# commands act on players
		self.ansi = ansi		# input/output

	# actually runs the command
	def execute(self, raw_args):
		cleaned = decode(raw_args)
		self.opts = cleaned['options']
		self.args = cleaned['args']

		if('h' in self.opts):
			self.out(self.man['SYNOPSIS']+'\n\r')
			return False

		return True

	def error(self, msg):
		self.ansi.color("red")
		self.out("error: "+msg+"\n\r")
		self.ansi.clear()

	def out(self, msg):
		self.ansi.out(msg)


# command that requires active satellite connection
class SatCmd(Cmd):
	def execute(self, raw_args):
		if(not super(SatCmd, self).execute(raw_args)): return False

		if not self.player.sat:
			self.error("not connected to satellite")
			return False

		return True

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

	# actuallly runs the command
	@abstractmethod
	def execute(self, raw_args):
		arguments = decode(raw_args)
		return

	def error(self, msg):
		self.ansi.color("red")
		self.out("error: "+msg+"\n\r")
		self.ansi.clear()

	def out(self, msg):
		self.ansi.out(msg)

class Ansi(object):
	colors = { 'black':'30', 'red':'31', 'green':'32', 'yellow':'33', 'blue':'34', 'magenta':'35', 'cyan':'36', 'white':'37' }

	def __init__(self, terminal):
		self.terminal = terminal

	def out(self, msg):
		self.terminal.write(msg)

	def color(self, name):
		c = Ansi.colors[name]
		if c: self.terminal.write("\033["+c+"m")

	def clear(self):
		self.terminal.write("\033[0m")

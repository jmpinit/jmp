from command import Cmd

man = {
	'NAME':'hexdump - print hexadecimal and ASCII representations of satellite memory.',
	'SYNOPSIS':'hexdump [-AhH] start length',
	'DESCRIPTION':'hexdump uses the SatBIOS of the currently connected satellite to dump the specified memory from the satellite CPU in human-readable form.',
	'OPTIONS': {
		'-A':'prints only the ASCII form',
		'-h':'prints info about the command',
		'-H':'prints only the hex form',
	}
}

class Hexdump(Cmd):
	def execute(self, arguments):
		sat = self.player.sat
		bios = sat.bios
		cpu = sat.cpu

		cleaned = self.decode(arguments)
		opts = cleaned['options']
		args = cleaned['args']

		try:
			address = int(args[0], 0)
			length = int(args[1], 0)
		except:
			self.error("invalid arguments")

		if not sat:
			self.error("not connected to satellite")
			return

		self.out("PC  | %0.4X\n\r" % sat.cpu.pc)
		self.out("ADDR| DATA                                     | ASCII\n\r")
		self.out("=========================================================\n\r")

		chunksize = 8
		for chunk in range(address, address+length, chunksize):
			# print the address
			self.out("%0.4X| " % section)

			# print the data as hex
			for i in range(0, 8):
				if cpu.pc == section+i:
					self.ansi.color("magenta")
				self.out("%0.4X " % sat.bios.peek(section+i).value)
				self.ansi.clear()

			self.out("| ")

			# print the data as ASCII
			for i in range(0, 8):
				c = bios.peek(section+i).value

				# printable?
				if(c>=32 and c<=126):
					if cpu.pc == section+i:
						self.ansi.color("magenta")
					self.out(chr(c))
					self.ansi.clear()
				else:
					self.out(".")

			self.out("\n\r")
		else:
			self.error(man['SYNOPSIS'])

import bfcpu
import satellite 
import components

#p = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
p = ".>.,"
d = [1]

b = bfcpu.BFCPU(512)

# load program
for i, c in enumerate(p):
	b.write(i, ord(c))

# load data
for i, v in enumerate(d):
	b.write(i+128, v)

b.bus.add(components.Clock())

sat = satellite.Satellite(b)

while(True):
	sat.tick()

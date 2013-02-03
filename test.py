import bfcpu

p = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
b = bfcpu.BFCPU(512)

for i, c in enumerate(p):
	b.write(i, ord(c))

while(True):
	b.tick()

import bfcpu
from world import *
import satellite 
import components

import pygame

screen = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)

""" CPU STUFF """
#p = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
p = ".>.>."
d = [2, 0, 32000]

cpu = bfcpu.BFCPU(512)

# load program
for i, c in enumerate(p):
	cpu.write(i, ord(c))

# load data
for i, v in enumerate(d):
	cpu.write(i+128, v)

""" CONSTRUCT SAT """
world = World(128, 128, 128)


sat = Satellite(cpu, (0, 0, 0), (0, 0, 0))
cpu.bus.add(components.Thruster(sat))

world.sats.append(sat)

while(True):
	world.tick()
	pygame.draw.circle(screen, (255, 255, 255), (sat.x+512, sat.y+300), 16, 3)
	pygame.display.flip()

	for event in pygame.event.get():
		if(event.type==pygame.KEYDOWN):
			exit()

import pygame, math, time
from three import *
import numpy as np
from random import random

width = 1024
height = 600

timescale = 10

screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

class Plane(object):
	def __init__(self, p0, p1, p2):
		self.p0 = p0
		self.p1 = p1
		self.p2 = p2

class Line(object):
	def __init__(self, p0, p1):
		self.p0 = p0
		self.p1 = p1

class Pt(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class Camera(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

def intersect(p, l):
	xa = l.p0.x
	ya = l.p0.y
	za = l.p0.z

	xb = l.p1.x
	yb = l.p1.y
	zb = l.p1.z

	x0, y0, z0 = (p.p0.x, p.p0.y, p.p0.z)
	x1, y1, z1 = (p.p1.x, p.p1.y, p.p1.z)
	x2, y2, z2 = (p.p2.x, p.p2.y, p.p2.z)

	try:
		left = np.mat(
			[
				[xa-xb, x1-x0, x2-x0],
				[ya-yb, y1-y0, y2-y0],
				[za-zb, z1-z0, z2-z0]
			]
		)

		right = np.mat(
			[
				[xa-x0],
				[ya-y0],
				[za-z0]
			]
		)

		return tuple([x[0] for x in (left.getI()*right).tolist()])
	except:
		return None

def distance(start, end):
	x0, y0, z0 = start
	x1, y1, z1 = end
	return math.sqrt((x0-x1)**2+(y0-y1)**2+(z0-z1)**2)

def init():
	global cam, scene
	cam = Camera(0, 0, 0)
	scene = [Plane(Pt(0, 0, 2000), Pt(100, 100, 500), Pt(-100, 100, 100))]

def draw():
	screen.fill((0, 0, 0));

	scale = 10
	for y in range(0, height, 4):
		for x in range(0, width, 4):
			tx = cam.x+x/scale
			ty = cam.y+y/scale
			tz = cam.z+10

			ray = Line(Pt(cam.x, cam.y, cam.z), Pt(tx, ty, tz))
			intersection = intersect(scene[0], ray)

			if(intersection == None):
				color = 0
			else:
				if(distance(intersection, (tx, ty, tz))<distance(intersection, (cam.x-x/scale, cam.y-y/scale, cam.z-10))):
					dist = distance((cam.x, cam.y, cam.z), intersection)
					color = max(min(int(255-dist*20), 255), 0)
				else:
					color = 0

			screen.fill((color, color, color), ((x, y), (4, 4)))
			
		pygame.display.flip()


init()
draw()
while True:
	for event in pygame.event.get():
		if(event.type==pygame.KEYDOWN):
			if event.key == pygame.K_ESCAPE:
				exit()


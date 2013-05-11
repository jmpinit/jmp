import pygame, math, time
from three import *
from random import random

width = 1024
height = 600

timescale = 10

screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

class Planet(object):
	def __init__(self, mass, radius, atmosphere):
		self.x = self.y = 0

		self.mass = mass
		self.radius = radius
		self.atmosphere = atmosphere

class Satellite(object):
	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy

		self.mass = 1

		self.temp = 0
		self.dead = False

	def update(self, dt):
		if(not self.dead):
			r = math.sqrt((planet.x-self.x)**2 + (planet.y-self.y)**2)
			g_accel = (physics.G*planet.mass/r**2)

			angle_to = math.atan2(planet.y-self.y, planet.x-self.x)

			self.vx += g_accel*math.cos(angle_to)
			self.vy += g_accel*math.sin(angle_to)

			self.x += self.vx*dt
			self.y += self.vy*dt

			# burn in the atmosphere
			#altitude = r - planet.radius
			#if altitude < planet.atmosphere and altitude > 0:
				#self.temp = 100*(1-altitude/float(planet.atmosphere))*math.sqrt(self.vx**2+self.vy**2)

			if self.temp > 3000:
				self.dead = True

			# crash into surface
			if altitude < 0:
				self.dead = True

def launch(planet, location, speed, angle):
	r = planet.radius
	sat = Satellite(r*math.cos(location), r*math.sin(location), speed*math.cos(angle), speed*math.sin(angle))
	sats.append(sat)

class Camera(object):
	# width, height in 'real' coordinates (km)
	def __init__(self, center_x, center_y, width, height):
		self.x = center_x
		self.y = center_y
		self.width = width
		self.height = height
	
	def vis(self, ent):
		if(ent.x>self.x-self.width/2 and ent.x<self.x+self.width/2 and ent.y>self.y-self.height/2 and ent.y<self.y+self.height/2):
			return True
		else:
			return False

	def zoom(self, factor):
		self.width /= factor
		self.height /= factor

	def set_pos(self, x, y):
		self.x = x
		self.y = y

	def pos_x(self, real_x):
		if(real_x>self.x-self.width/2 and real_x<self.x+self.width/2):
			diff = real_x - self.x
			return width/2 + self.scale_x(diff)
		else:
			return -1

	def pos_y(self, real_y):
		if(real_y>self.y-self.width/2 and real_y<self.y+self.width/2):
			diff = real_y - self.y
			return height/2 + self.scale_y(diff)
		else:
			return -1

	# turn real world val into screen val
	def scale_x(self, real):
		return real/(self.width/width) # _ km per pixel

	def scale_y(self, real):
		return real/(self.height/height) # _ km per pixel

def init():
	global planet, sats, cam
	planet = Earth()
	sats = []
	cam = Camera(0, 0, planet.radius*4, planet.radius*4*(height/float(width)))

	# put something up there
	for i in range(0, 50):
		pos = 2*math.pi*random()
		a = pos+math.pi*random()-math.pi/2
		launch(planet, pos, 10+20*random(), a)

	global last_time
	last_time = time.time()

def draw():
	screen.fill((0, 0, 0));

	for v in self.vertices:
		# Rotate the point around X axis, then around Y axis, and finally around Z axis.
		r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
		# Transform the point from 3D to 2D
		p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
		x, y = int(p.x), int(p.y)
		# self.screen.fill((255,255,255),(x,y,2,2))
		if(not (v.x == 0 or v.y == 0 or v.z == 0)):
			pygame.draw.circle(self.screen, (255, 255, 255), (x, y), int(256/math.sqrt(v.x**2+v.y**2+(v.z-256)**2)))

	self.angleX += 1
	self.angleY += 1
	self.angleZ += 1

	# draw atmosphere
	layers = 10
	for h in range(layers, 0, -1):
		pygame.draw.circle(screen, (10, 10, int(255/h)), (int(cam.pos_x(planet.x)), int(cam.pos_y(planet.y))), int(cam.scale_x(planet.radius+planet.atmosphere/layers*h)))
	
	# draw atmosphere
	pygame.draw.circle(screen, (255, 255, 255), (int(cam.pos_x(planet.x)), int(cam.pos_y(planet.y))), int(cam.scale_x(planet.radius)))

	# draw satellites
	for sat in sats:
		if(cam.vis(sat)):
			pos = (int(cam.pos_x(sat.x)), int(cam.pos_y(sat.y)))
			size = int(cam.scale_x(100))
			thickness = min(int(sat.temp/1000*3+1), size)

			if(sat.dead):
				pygame.draw.circle(screen, (128, 128, 128), pos, size, thickness)
			else:
				pygame.draw.circle(screen, (255, 0, 0), pos, size, thickness)

	pygame.display.flip()

init()
while True:
	for sat in sats:
		sat.update(timescale*(time.time()-last_time))

	last_time = time.time()

	cam.set_pos(sats[-1].x, sats[-1].y)

	draw()

	for event in pygame.event.get():
		if(event.type==pygame.KEYDOWN):
			if event.key == pygame.K_LEFT:
				timescale *= 0.9
			if event.key == pygame.K_RIGHT:
				timescale *= 1.1
			if event.key == pygame.K_SPACE:
				cam.zoom(1.1)
			if event.key == pygame.K_BACKSPACE:
				cam.zoom(0.9)
			if event.key == pygame.K_ESCAPE:
				exit()


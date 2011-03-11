import sys
from threading import Thread

from particle import *
from random import random

class Simulation:
	def __init__(self, width, height):
		self.particles = []
		self.surface = pygame.display.set_mode((width, height))
		self.reconstituition = 0.01
		self.create_mesh(10, 10, (200, 200), 7)
		self.selected = None

	def run(self):
		clock = pygame.time.Clock()
		while 1:
			for part in self.particles:
				part.get_link_force()
			for part in self.particles:
				part.update()
			for part in self.particles:
				part.draw(self.surface)
			pygame.display.flip()
			self.surface.fill((0,0,0))
			clock.tick(40)

	def event(self):
		while 1:
			event = pygame.event.wait()
			if event.type == MOUSEMOTION:
				if self.selected == None: continue
				self.selected.pos[0] = event.pos[0]
				self.selected.pos[1] = event.pos[1]
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					if self.selected == None:
						self.selected = min(self.particles, key = lambda p: sqrt((\
						p.pos[0] - event.pos[0]) ** 2 + (p.pos[1] - event.pos[1]) ** 2))
						self.selected.static = True
					else:
						#self.selected.static = False
						self.selected = None
				elif event.button == 3:
						sec = min(self.particles, key = lambda p: sqrt((p.pos[0] - \
											event.pos[0]) ** 2 + (p.pos[1] - event.pos[1]) ** 2))
						sec.static = not sec.static
						self.selected = None

					

	def create_mesh(self, x, y, pos, d = 10):
		for xp in range(x):
			for yp in range(y):
					self.particles.append(Particle(xp * d + pos[0], yp * d + pos[1], 0, 0, static = 0, mass = 10))

		for xp in range(x):
			for yp in range(y):
				if(yp < y - 1):
					self.particles[xp * x + yp].links.append(Link(self.particles[xp * x + yp], self.particles[xp * x + yp + 1]))
				if(xp < x - 1):
					self.particles[xp * x + yp].links.append(Link(self.particles[xp * x + yp], self.particles[(xp + 1) * x + yp]))

teste = Simulation(1300, 800)
run = Thread(target = teste.run)
event = Thread(target = teste.event)
run.start()
event.start()

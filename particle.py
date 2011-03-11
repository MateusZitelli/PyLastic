from math import sqrt

import pygame
from pygame.locals import *

class Link:
	def __init__(self, part1, part2, restituition = 6, size = 7):
		self.size = size
		self.r = restituition
		self.link = (part1, part2)
		self.color = (255, 255,255)

	def solve(self):
		dx = float(self.link[0].pos[0] - self.link[1].pos[0])
		dy = float(self.link[0].pos[1] - self.link[1].pos[1])
		if dx == 0: dx = 10E-10
		if dy == 0: dy = 10E-10
		final = sqrt(dx * dx + dy * dy)
		#if final < self.size: return
		force = self.r * (final - self.size) / 2.0
		#if abs(force) > 200:
		#	if self in self.link[0].links:
		#		self.link[0].links.remove(self)
		#	elif self in self.link[0].links:
		#		self.link[0].links.remove(self)
		self.link[0].force[0] += - force * (dx / final)
		self.link[1].force[0] += force  * (dx / final)
		self.link[0].force[1] += - force  * (dy / final)
		self.link[1].force[1] += force  *  (dy / final)
		val = final/self.size * 16.0
		if val > 255: val = 255
		self.color = (val , 0 , 0)

	def draw(self, surface):
		pygame.draw.line(surface, self.color, (self.link[0].pos[0], self.link[0].pos[1]), (self.link[1].pos[0], self.link[1].pos[1]))

class Particle:
	def __init__(self, x, y, vx, vy, size = 3, color = (255, 20, 255), mass = 10, static = 0):
		self.pos = [x,y]
		self.speed = [vx, vy]
		self.size = size
		self.color = color
		self.mass = mass
		self.links = []
		self.force = [0,0]
		self.static = static

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.pos, self.size)
		for l in self.links:
			l.draw(surface)

	def update(self):
		#self.force[1] += 0.1
		if self.static:
			self.force = [0,0]
			return
		self.speed[0] += self.force[0] / self.mass - self.speed[0] / 50.0
		self.speed[1] += self.force[1] / self.mass - self.speed[1] / 50.0
		self.pos[0] += self.speed[0]
		self.pos[1] += self.speed[1]
		self.force = [0, 0]


	def get_link_force(self):
		for l in self.links:
			l.solve()


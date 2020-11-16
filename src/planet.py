##!/usr/bin/env python3

import random
import math

import pygame

import constants as c
from primitives import PhysicsObject, Pose

class Planet(PhysicsObject):
    def __init__(self, game, position, angle=None, radius=100, gravity_radius=None, mass=None):
        if angle is None:
            angle = random.random()*360
        super().__init__(game, position, angle)
        self.velocity.angle = 10
        self.radius = radius
        self.gravity_radius = gravity_radius if gravity_radius is not None else 2.5*radius
        self.mass = mass if mass is not None else radius*100

        self.surface = pygame.image.load(c.IMAGE_PATH + "/large_planet.png")
        self.surface = pygame.transform.scale(self.surface, (radius*2, radius*2))
        self.shadow = pygame.image.load(c.IMAGE_PATH + "/planet_shadow.png")
        self.shadow = pygame.transform.scale(self.shadow,
                                            (self.surface.get_width(),
                                            self.surface.get_height()))
        self.shadow.set_colorkey(c.WHITE)
        self.shadow.set_alpha(70)
        self.age = 0

    def is_moon(self):
        """ Planets aren't moons, silly. """
        return False

    def get_acceleration(self, ship):
        """ Return a Pose indicating the acceleration to apply to
            the Ship.
        """
        distance = self.pose.distance_to(ship.pose)
        if distance > self.gravity_radius:
            return Pose((0, 0), 0)
        if distance < self.radius + ship.radius:
            ship.destroy()
        gravity_magnitude = self.mass * c.GRAVITY_CONSTANT / distance**2
        gravity_vector = (self.pose - ship.pose)
        gravity_vector.set_angle(0)
        gravity_vector.scale_to(gravity_magnitude)
        return gravity_vector

    def draw(self, surf, offset=(0, 0)):
        my_surface = pygame.transform.rotate(self.surface, self.pose.angle)
        x, y = self.pose.get_position()
        x += offset[0]
        y += offset[1]
        surf.blit(my_surface, (x - my_surface.get_width()//2, y - my_surface.get_height()//2))
        surf.blit(self.shadow, (x - self.shadow.get_width()//2, y - self.shadow.get_height()//2))
        self.draw_gravity_region(surf, offset)
        # pygame.draw.circle(surf, (200, 200, 200), (x, y), self.radius)

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt

    def draw_gravity_region(self, surf, offset=(0, 0)):
        radius = self.gravity_radius
        pixels_per_degree = math.pi * 2 * radius / 360
        x, y = self.pose.get_position()
        x += offset[0]
        y += offset[0]
        w = self.gravity_radius * 2
        h = self.gravity_radius * 2
        pixels_each = 8
        dots = int((360 * pixels_per_degree / pixels_each)/10 * 10)
        angle_offset = self.age * 15 / radius
        for i in range(dots):
            angle_rad = 2 * math.pi * i/dots + (angle_offset)
            my_radius = radius + math.sin(i) * 3
            pygame.draw.circle(surf,
                            c.GRAY,
                            (x + my_radius * math.sin(angle_rad), y + my_radius * -math.cos(angle_rad)),
                            1)

        # x, y = self.pose.get_position()
        # x += offset[0]
        # y += offset[1]
        #pygame.draw.circle(surf, (100, 100, 100), (x, y), self.gravity_radius, 2)

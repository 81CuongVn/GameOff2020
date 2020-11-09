##!/usr/bin/env python3

import pygame
import constants as c
from primitives import PhysicsObject, Pose
from player import Player

class Ship(PhysicsObject):
    def __init__(self, game, program_string, player, position=(0, 0), angle=90):
        super().__init__(game, position, angle)
        self.program_string = program_string
        self.program = self.parse_program(program_string)
        self.player = player
        self.age = 0
        self.thrust = Pose((0,0), 0)
        self.commandIndex = 0
        self.delay = 0
        self.destroyed = False

    def destroy(self):
        self.destroyed = True

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt
        if self.delay > 0:
            self.delay = max(0, self.delay-dt)
        self.runCommands(dt)
        self.acceleration.clear()
        self.acceleration.add_pose(self.thrust, 1, frame=self.pose)
        for planet in self.game.current_scene.planets:
            self.acceleration.add_pose(planet.get_acceleration(self))

    def runCommands(self, dt):
        while self.delay <= 0 and self.commandIndex < len(self.program):
            command = self.program[self.commandIndex]
            if command[0] == 'd': # delay
                self.delay += command[1]/1000
            if command[0] == 't': # thrust
                self.thrust = Pose((command[1]*c.THRUST, 0), 0)
            if command[0] == 'r': # rotate
                self.velocity.set_angle(command[1])
            self.commandIndex += 1

    def draw(self, surface, offset=(0, 0)):
        ship_surf = pygame.Surface((60, 30)).convert()
        ship_surf.fill(c.BLACK)
        ship_surf.set_colorkey(c.BLACK)
        pygame.draw.rect(ship_surf, self.player.color, (15, 0, 30, 30))
        pygame.draw.circle(ship_surf, self.player.color, (45, 15), 15)
        ship_surf = pygame.transform.rotate(ship_surf, self.pose.angle)
        x = self.pose.x + offset[0] - ship_surf.get_width()//2
        y = self.pose.y + offset[1] - ship_surf.get_height()//2
        surface.blit(ship_surf, (x, y))

    @staticmethod
    def parse_program(program_string):
        program_string = program_string.lower().strip() + 'A'
        program = []
        arguments = []
        key = ''
        number = ''
        isNumber = False
        for char in program_string:
            if char == '.':
                print("Decimals not permitted")
                return []
            elif char.isnumeric() or char == '-':
                isNumber = True
                number += char
            elif char.isalnum():
                # terminate previous number
                if (len(number) == 1 or number[1:].isnumeric()) and \
                (number[0].isdigit() or number[0] == '-'):
                    arguments.append(int(number))
                    number = ''
                elif number != '':
                    print("Invalid number")
                    return []
                # terminate previous command
                if isNumber or char == 'A':
                    if key in c.COMMANDS.values():
                        command = key
                    elif key in c.COMMANDS:
                        command = c.COMMANDS[key]
                    else:
                        print("Invalid command")
                        return []
                    if len(arguments) != len(c.COMMANDS_MIN[command]):
                        print("Invalid number of arguments")
                        return []
                    for i, arg in enumerate(arguments):
                        if arg < c.COMMANDS_MIN[command][i]:
                            print("Argument was smaller than minimum value")
                            return []
                        if arg > c.COMMANDS_MAX[command][i]:
                            print("Argument was greater than maximum value")
                            return []
                    program.append((command, *arguments))
                    key = ''
                    arguments = []
                    isNumber = False
                key += char
            elif char in " ,;":
                isNumber = True
                if number[1:].isnumeric() and \
                (number[0].isdigit() or number[0] == '-'):
                    arguments.append(int(number))
                    number = ''
            else:
                print("Invalid character")
                return []
        return program

if __name__ == '__main__':
    Ship.parse_program("t100 r9 d1000 t1")
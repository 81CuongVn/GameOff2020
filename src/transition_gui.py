##!/usr/bin/env python3

import math
import random

import pygame

from primitives import GameObject, Pose
import constants as c

class AlertBox(GameObject):

    def __init__(self, game, position, header, message, side_surface=None):
        super().__init__(game)
        self.age = 0
        self.pose = Pose(position, 0)
        self.header = header
        self.message = message
        self.side_surface = side_surface
        self.generate_colors()
        self.load_surfs()
        self.max_width = self.top_surf.get_width() - c.ALERT_SIDE_PADDING * 2
        if self.side_surface is not None:
            self.max_width -= self.side_surface.get_width() + c.ALERT_SIDE_PADDING
        self.header_surf = self.get_header_surface()
        self.message_surface = self.get_message_surface()

    def generate_colors(self):
        self.header_color = (255, 200, 200)
        self.body_color = (190, 160, 160)

    def get_header_surface(self):
        render = self.game.alert_header_font.render(self.header, 1, self.header_color)
        background = pygame.transform.scale(self.middle_surf,
                                            (self.middle_surf.get_width(),
                                            render.get_height() + 8)).convert()
        x = background.get_width()//2 - render.get_width()//2
        if self.side_surface is not None:
            x += (self.side_surface.get_width() + c.ALERT_SIDE_PADDING)//2
        background.blit(render, (x, 0))
        return background

    def get_message_surface(self):
        message_surfaces = []
        message_lines = self.message.split("\n")
        for line in message_lines:
            message_words = line.split()
            this_line = []
            this_width = 0
            for word in message_words:
                surface = self.game.alert_body_font.render(word, 1, self.body_color)
                if this_width + surface.get_width() > self.max_width:
                    message_surfaces.append(this_line)
                    this_line = []
                    this_width = 0
                this_line.append(surface)
                this_width += surface.get_width() + c.ALERT_BODY_SPACE
            message_surfaces.append(this_line)

        total_height = c.ALERT_LINE_SPACING*(len(message_surfaces))
        if self.side_surface is not None and total_height < self.side_surface.get_height() - self.header_surf.get_height():
            total_height = self.side_surface.get_height() - self.header_surf.get_height()
        background = pygame.transform.scale(self.middle_surf,
                                            (self.middle_surf.get_width(),
                                            total_height)).convert()
        y = 0
        for line in message_surfaces:
            line_width = sum([item.get_width() + c.ALERT_BODY_SPACE for item in line]) - c.ALERT_BODY_SPACE
            x = background.get_width()//2 - line_width//2
            if self.side_surface is not None:
                x += self.side_surface.get_width()//2 + c.ALERT_SIDE_PADDING//2
            for word in line:
                background.blit(word, (x, y))
                x += word.get_width() + c.ALERT_BODY_SPACE
            y += c.ALERT_LINE_SPACING

        return background

    def load_surfs(self):
        self.top_surf = pygame.image.load(c.IMAGE_PATH + "/red_alert_box_top.png")
        self.middle_surf = pygame.image.load(c.IMAGE_PATH + "/red_alert_box_middle.png")
        self.bottom_surf = pygame.image.load(c.IMAGE_PATH + "/red_alert_box_bottom.png")

    def draw(self, surface, offset=(0, 0)):
        surfaces = [self.top_surf, self.header_surf, self.message_surface, self.bottom_surf]
        x = self.pose.x - self.top_surf.get_width()//2 + offset[0]
        y = self.pose.y - sum([item.get_height() for item in surfaces])//2 + offset[1] + 4 * math.sin(self.age * 2)
        y0 = y
        for piece in surfaces:
            surface.blit(piece, (x, y))
            y += piece.get_height()

        if self.side_surface is not None:
            surface.blit(self.side_surface,
                (x + c.ALERT_SIDE_PADDING,
                y0 + self.top_surf.get_height()
                + self.header_surf.get_height()//2
                + self.message_surface.get_height()//2
                - self.side_surface.get_height()//2))

    def update(self, dt, events):
        self.age += dt

class GreenAlertBox(AlertBox):
    def generate_colors(self):
        self.header_color = (200, 230, 205)
        self.body_color = (150, 180, 160)

    def load_surfs(self):
        self.top_surf = pygame.image.load(c.IMAGE_PATH + "/green_alert_box_top.png")
        self.middle_surf = pygame.image.load(c.IMAGE_PATH + "/green_alert_box_middle.png")
        self.bottom_surf = pygame.image.load(c.IMAGE_PATH + "/green_alert_box_bottom.png")

class PlayerMultiplierAlertBox(AlertBox):
    def __init__(self, game, position, header, message):
        self.background_color = (68, 35, 48)
        self.game = game
        self.generate_colors()
        side_surface = self.generate_multiplier_surface()
        super().__init__(game, position, header, message, side_surface=side_surface)
        self.age += 2

    def generate_multiplier_surface(self):
        text = f"x{self.game.player_multiplier()}"
        render = self.game.alert_large_font.render(text, 1, self.header_color)
        surface = pygame.Surface((render.get_width(), 70))
        surface.fill(self.background_color)
        surface.blit(render,
            (surface.get_width()//2 - render.get_width()//2,
            surface.get_height()//2 - render.get_height()//2))
        return surface

class Countdown(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.duration = 20

class TransitionGui(GameObject):

    def __init__(self, game):
        super().__init__(game)
        self.age = 0
        self.width = c.WINDOW_WIDTH - c.SCORE_TABLE_WIDTH
        self.height = c.WINDOW_HEIGHT
        self.pose = Pose((c.SCORE_TABLE_WIDTH + self.width//2, c.WINDOW_HEIGHT//2), 0)
        self.objects = []
        self.background = pygame.image.load(c.IMAGE_PATH + "/trans_gui_back.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.add_tip_box()
        self.add_player_mult_box()

    def add_tip_box(self):
        position = 0, c.WINDOW_HEIGHT*0.28
        header = "Helpful hint"
        body = random.choice(c.HINTS)
        #ss = pygame.image.load(c.IMAGE_PATH + "/bang.png")
        self.objects.append(GreenAlertBox(self.game, position, header, body))

    def add_player_mult_box(self):
        position = 0, -c.WINDOW_HEIGHT * 0.35
        header = "Player party multiplier"
        if self.game.player_multiplier() == 0:
            choices = c.MULT_0_MESSAGES
        else:
            choices = c.MULT_MESSAGES
        body = random.choice(choices).replace("{num}", str(self.game.number_of_players_last_round()))
        self.objects.append(PlayerMultiplierAlertBox(self.game, position, header, body))

    def update(self, dt, events):
        self.age += dt
        for item in self.objects:
            item.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        xoff = offset[0] + self.pose.x
        yoff = offset[1] + self.pose.y
        surface.blit(self.background, (xoff - self.width//2, yoff - self.height//2))
        for item in self.objects:
            item.draw(surface, (xoff, yoff))

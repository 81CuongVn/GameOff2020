##!/usr/bin/env python3

import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
FULLSCREEN = False

LEVEL_WIDTH = int(WINDOW_WIDTH * 0.8)
LEVEL_HEIGHT = int(WINDOW_HEIGHT * 1.0)

SIDE_PANEL_WIDTH = WINDOW_WIDTH - LEVEL_WIDTH
SIDE_PANEL_HEIGHT = WINDOW_HEIGHT
SIDE_PANEL_SIZE = SIDE_PANEL_WIDTH, SIDE_PANEL_HEIGHT

ACHIEVEMENT_WIDTH = 237
ACHIEVEMENT_POINTS_WIDTH = 70

ACHIEVEMENT_LABEL_WIDTH = SIDE_PANEL_WIDTH
ACHIEVEMENT_LABEL_HEIGHT = 40
ACHIEVEMENT_LABEL_SIZE = ACHIEVEMENT_LABEL_WIDTH, ACHIEVEMENT_LABEL_HEIGHT

TIMER_POSITION = SIDE_PANEL_WIDTH//2, 40

SHIP_SCALE = 0.6

MAX_FPS = 60
TICK_LENGTH = 1/100

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
CYAN = 0, 255, 255
MAGENTA = 255, 0, 255
GRAY = 128, 128, 128
DARK_GRAY = 50, 46, 57
DARKER_GRAY = 45, 42, 52
LIGHT_GRAY = 192, 192, 192

RIGHT = (1, 0)
UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
CENTER = (0, 0)

COMMANDS = {"thrust":'t', "delay":'d', "rotate":'r'}
COMMANDS_MIN = {'t':(0,), 'd':(0,), 'r':(-360,)}
COMMANDS_MAX = {'t':(100,), 'd':(60000,), 'r':(360,)}
THRUST = 2

LOG_PATH = "error_log.txt"
SCORE_SAVE_PATH = "../data"
IMAGE_PATH = "../images"
FONT_PATH = "../fonts"

GRAVITY_CONSTANT = 600

MIN_PLANET_RADIUS = 25
MAX_PLANET_RADIUS = 75
HOME_PLANET_RADIUS = 25
MIN_SPACING = 50

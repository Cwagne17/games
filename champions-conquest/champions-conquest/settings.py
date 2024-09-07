from os.path import join
from os import walk
from typing import List, Dict, Tuple, Optional
import pygame
from pygame.locals import *

ASSETS_PATH = "../assets"

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (1280, 720)
TILE_SIZE = 64

D_down = "down"
D_left = "left"
D_right = "right"
D_up = "up"

DIRECTIONS = [D_down, D_left, D_right, D_up]

# Character Classes

CT_champion = "champion"
CT_orc = "orc"

# Action Settings

A_attack = "attack"
A_death = "death"
A_hurt = "hurt"
A_idle = "idle"
A_run = "run"
A_walk_attack = "walk_attack"
A_walk = "walk"

CHARACTER_ACTION_FRAMES = {
    A_attack: {
        CT_champion: 8,
        CT_orc: 8
    },
    A_death: {
        CT_champion: 7,
        CT_orc: 8
    },
    A_hurt: {
        CT_champion: 5,
        CT_orc: 6
    },
    A_idle: {
        CT_champion: 4,
        CT_orc: 4
    },
    A_run: {
        CT_champion: 8,
        CT_orc: 8
    },
    A_walk_attack: {
        CT_champion: 6,
        CT_orc: 6
    },
    A_walk: {
        CT_champion: 6,
        CT_orc: 6
    }
}
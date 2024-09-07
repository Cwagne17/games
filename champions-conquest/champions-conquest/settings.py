from os.path import join
from os import walk
from typing import List, Dict, Tuple, Optional, TypeVar
import pygame
from pygame.locals import *

ASSETS_PATH = "../assets"

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (1280, 720)
TILE_SIZE = 64

# Character Directions

Direction = TypeVar("Direction")

D_down: Direction = "down"
D_left: Direction = "left"
D_right: Direction = "right"
D_up: Direction = "up"

DIRECTIONS: List[Direction] = [D_down, D_left, D_right, D_up]

# Character Classes

Class = TypeVar("Class")

C_champion: Class = "champion"
C_orc_brute: Class = "orc_brute"
C_orc_commander: Class = "orc_commander"
C_orc_grunt: Class = "orc_grunt"

# Action Settings

Action = TypeVar("Action")

A_attack: Action = "attack"
A_death: Action = "death"
A_hurt: Action = "hurt"
A_idle: Action = "idle"
A_run: Action = "run"
A_walk_attack: Action = "walk_attack"
A_walk: Action = "walk"

ACTIONS: List[Action] = [A_attack, A_death, A_hurt, A_idle, A_walk]

Frames = Dict[Action, Dict[Direction, List[pygame.Surface]]]

CHARACTER_ACTION_FRAMES: Dict[Action, Dict[Class, int]] = {
    A_attack: {
        C_champion: 8,
        C_orc_brute: 8,
        C_orc_commander: 8,
        C_orc_grunt: 8,
    },
    A_death: {
        C_champion: 7,
        C_orc_brute: 8,
        C_orc_commander: 8,
        C_orc_grunt: 8,
    },
    A_hurt: {
        C_champion: 5,
        C_orc_brute: 6,
        C_orc_commander: 6,
        C_orc_grunt: 6,
    },
    A_idle: {
        C_champion: 4,
        C_orc_brute: 4,
        C_orc_commander: 4,
        C_orc_grunt: 4,
    },
    A_run: {
        C_champion: 8,
        C_orc_brute: 8,
        C_orc_commander: 8,
        C_orc_grunt: 8,
    },
    A_walk_attack: {
        C_champion: 6,
        C_orc_brute: 6,
        C_orc_commander: 6,
        C_orc_grunt: 6,
    },
    A_walk: {
        C_champion: 6,
        C_orc_brute: 6,
        C_orc_commander: 6,
        C_orc_grunt: 6,
    }
}
import pygame
from shared.spritesheet import SpriteSheet

class Character():
    """This is the base class for all characters in the game."""
    # Positional variables
    _direction: str = "left"
    _x: int = 100
    _y: int = 100
    ## Animation variables
    _frame: int = 0
    _sword_walk_full_sprite = {"down": [], "left": [], "right": [], "up": []}
    
    # The speed of the character
    _velocity: int = 5 # Default speed
    
    # The health of the character
    _health: int = 100
    
    # The name of the character
    _name: str = "Base Character"
    
    def __init__(self, name, health, speed):
        self._name = name
        self._health = health
        self._speed = speed
        
        # Use the sprite sheet to load the character sprite
        male_image = SpriteSheet("assets/Characters/Male/PNG/Sword_Walk/Sword_Walk_full.png")
        for row, direction in enumerate(["down", "left", "right", "up"]):
            self._sword_walk_full_sprite[direction] = [ male_image.get_image(row, frame, 64, 64, 2.5) for frame in range(6)]
        
    # The following functions are positional functions
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def move_up(self):
        self._y -= self._speed
        self._direction = "up"
    
    def move_down(self):
        self._y += self._speed
        self._direction = "down"
    
    def move_left(self):
        self._x -= self._speed
        self._direction = "left"
    
    def move_right(self):
        self._x += self._speed
        self._direction = "right"
        
    # The following functions are action functions
    
    # The following function renders the character
    def draw(self, display: pygame.Surface, frame: int):
        display.blit(self._sword_walk_full_sprite[self._direction][frame], (self._x, self._y))
        
        
        
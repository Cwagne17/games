import pygame
from shared.spritesheet import SpriteSheet

class Character():
    """This is the base class for all characters in the game."""
    # Positional variables
    _direction: str = "left"
    _x: int = 100
    _y: int = 100
    _height: int = 64
    _width: int = 64
    
    # Animation variables
    _scale: float = 2.5
    _frame: int = 0
    _sword_walk_sprite = {"down": [], "left": [], "right": [], "up": []}
    _sword_walk_attack_sprite = {"down": [], "left": [], "right": [], "up": []}
    _sword_idle_sprite = {"down": [], "left": [], "right": [], "up": []}
    _attacking = False
    
    # Character attributes
    _name: str = "Base Character"
    _health: int = 100
    _velocity: int = 5 # Default speed
    
    
    def __init__(self, name, health, speed):
        self._name = name
        self._health = health
        self._speed = speed
        
        # Use the sprite sheet to load the character sprite
        male_walk = SpriteSheet("assets/Characters/Male/PNG/Sword_Walk/Sword_Walk_full.png")
        male_idle = SpriteSheet("assets/Characters/Male/PNG/Sword_Idle/Sword_Idle_full.png")
        male_walk_attack = SpriteSheet("assets/Characters/Male/PNG/Sword_Walk_Attack/Sword_Walk_Attack_full.png")
        for row, direction in enumerate(["down", "left", "right", "up"]):
            self._sword_walk_sprite[direction] = [ male_walk.get_image(row, frame, 64, 64, self._scale) for frame in range(6)]
            self._sword_walk_attack_sprite[direction] = [ male_walk_attack.get_image(row, frame, 64, 64, self._scale) for frame in range(6)]
            self._sword_idle_sprite[direction] = [male_idle.get_image(row, frame, 64, 64, self._scale) for frame in range(8)]
        
    # The following functions are positional functions
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def get_margin(self):
        # Each sprite is an 8x8 grid where there are 2 squares above and 
        # below the sprite and 3 on either side
        margin = 3 if self._direction in ["left", "right"] else 2
        
        # Since height and width are the same, we can use either
        _, image_height = self._sword_walk_sprite[self._direction][0].get_size()
     
        # Down and right can be calculated the same way
        if self._direction in ["down", "right"]:
            return image_height - (image_height//8 * margin)
        
        # Left, and up can be calculated the same way
        return image_height//8 * margin
        
    
    def move_up(self):
        self._y -= self._speed
        self._direction = "up"
        self._idle = False
    
    def move_down(self):
        self._y += self._speed
        self._direction = "down"
        self._idle = False

    def move_left(self):
        self._x -= self._speed
        self._direction = "left"
        self._idle = False
    
    def move_right(self):
        self._x += self._speed
        self._direction = "right"
        self._idle = False

    def set_idle(self):
        self._idle = True
        
    # The following functions are action functions
    def setAttacking(self, attacking: bool = False):
        self._attacking = attacking
    
    # The following function renders the character
    def draw(self, display: pygame.Surface, frame: int):
        if (self._attacking):
            display.blit(self._sword_walk_attack_sprite[self._direction][frame], (self._x, self._y))
        elif (self._idle):
            display.blit(self._sword_idle_sprite[self._direction][frame], (self._x, self._y))
        else:
            display.blit(self._sword_walk_sprite[self._direction][frame], (self._x, self._y))
        
        
        
import pygame
from pygame.locals import *
from shared.spritesheet import SpriteSheet
import os

class Character(pygame.sprite.Sprite):
    """This is the base class for all characters in the game."""
    # Positional variables
    __direction: pygame.Vector2 = pygame.Vector2(0, 0)
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
    
    
    def __init__(self, groups, name, health, speed):
        super().__init__(groups)
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
        
        self.image = self._sword_walk_sprite["down"][0]
        self.rect = self.image.get_rect(center = (100, 100))
        self.state, self.frame_index = "down", 0

    def load_images(self):
        """Loads the images for the character sprite in folders named left, right, up, and down
        
        This function expects that the file names are organized in alphabetical order
        """
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        
        for state in self.frames.keys():
            for folder_path, _, file_names in os.walk(os.path.join('assets', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = os.path.join(folder_path, file_name)
                        surface = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surface)
    
    def animate(self):
        # get state
        if self.__direction.x > 0:
            self.state = 'right' if self.__direction.x > 0 else 'left'
        if self.__direction.y > 0:
            self.state = 'down' if self.__direction.y > 0 else 'up'
        
        # animate
        self.frame_index = self.frame_index + 5 if self.__direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
    
    # def get_margin(self):
    #     # Each sprite is an 8x8 grid where there are 2 squares above and 
    #     # below the sprite and 3 on either side
    #     margin = 3 if self._direction in ["left", "right"] else 2
        
    #     # Since height and width are the same, we can use either
    #     _, image_height = self._sword_walk_sprite[self._direction][0].get_size()
     
    #     # Down and right can be calculated the same way
    #     if self._direction in ["down", "right"]:
    #         return image_height - (image_height//8 * margin)
        
    #     # Left, and up can be calculated the same way
    #     return image_height//8 * margin

    def set_idle(self):
        self._idle = True
        
    # The following functions are action functions
    def setAttacking(self, attacking: bool = False):
        self._attacking = attacking
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        # If no keys are pressed, set the character to idle
        if not keys[K_a] and not keys[K_s] and not keys[K_d] and not keys[K_w]:
            self.set_idle()
        
        self.__direction.x = int(keys[K_RIGHT]) - int(keys[K_LEFT])
        self.__direction.y = int(keys[K_DOWN]) - int(keys[K_UP])
        self.__direction = self.__direction.normalize() if self.__direction else self.__direction
        
        self.setAttacking(keys[K_SPACE])
        
        
    def update(self):
        self.rect.center += self.__direction * self._speed # * dt
    
    # The following function renders the character
    def draw(self, display: pygame.Surface, frame: int):
        if (self._attacking):
            display.blit(self._sword_walk_attack_sprite[self._direction][frame], (self._x, self._y))
        elif (self._idle):
            display.blit(self._sword_idle_sprite[self._direction][frame], (self._x, self._y))
        else:
            display.blit(self._sword_walk_sprite[self._direction][frame], (self._x, self._y))
        
        
        
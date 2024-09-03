import pygame
from pygame.locals import *
from shared.spritesheet import SpriteSheet
import os

D_down = "down"
D_left = "left"
D_right = "right"
D_up = "up"

directions = [D_down, D_left, D_right, D_up]

class Character(pygame.sprite.Sprite):
    """This is the base class for all characters in the game."""
    # Positional variables
    direction: pygame.Vector2 = pygame.Vector2(0, 0)
    
    # Animation variables

    ## The following actions define all potential character actions. These actions must match the
    ## name of the file in the assets/characters/champion directory
    actions = ["sword_walk_attack", "sword_walk"]    
    action = "sword_walk" # The current action the character is performing
    
    ## This is a dictionary that'll be constructed to hold all the character actions
    ## and their respective frames for each direction [action][direction][frame]
    frames = {}
    frame_index: int = 0 # The current frame index
    scale = 2.5 # The scale of the character

    # Character attributes
    name: str = "Champion"
    health: int = 100
    speed: int = 5
    
    def __init__(self, groups, name, health, speed):
        super().__init__(groups)
        # Set the character attributes
        self.name = name
        self.health = health
        self.speed = speed
        
        # Load images for animation
        self.load_images()
        
        # Set animation attributes
        self.action, self.state, self.frame_index = "sword_walk", D_down, 0
        
        # Set sprite attributes
        height, width = pygame.display.get_window_size()
        self.image = self.frames[self.action][self.state][self.frame_index]
        self.rect = self.image.get_rect(center = (height // 2, width // 2))
        
    def load_images(self):
        """Loads all the images for the character. This function is called once during initialization."""
        character_path = os.path.join("assets", "characters", "champion")
        
        for action in self.actions:
            action_surface: pygame.Surface = SpriteSheet(os.path.join(character_path, action + ".png"))
            self.frames[action] = {} # Initialize the action dictionary
            
            for row, direction in enumerate(directions):
                # TODO: We need to find a way to make the number of frames for dynamic for each action because it is not always 6
                self.frames[action][direction] = [action_surface.get_image(row, frame, 64, 64, self.scale) for frame in range(6)]
    
    def animate(self):
        # Get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        
        # Animate
        ## Update the frame index
        self.frame_index = self.frame_index + 5 if self.direction else 0
        
        ## Set the new frame as the image
        action_frames = self.frames[self.action][self.state]
        self.image = action_frames[int(self.frame_index) % len(action_frames)]
    
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
        
    # The following functions are action functions
    def setAttacking(self, attacking: bool = False):
        self.action = "sword_walk_attack" if attacking else "sword_walk"
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[K_RIGHT]) - int(keys[K_LEFT])
        self.direction.y = int(keys[K_DOWN]) - int(keys[K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        
        self.setAttacking(keys[K_SPACE])
        
    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed # * dt
        self.animate()

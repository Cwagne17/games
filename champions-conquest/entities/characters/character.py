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
    speed: int = 40
    
    def __init__(self, name, groups, collision_sprites):
        super().__init__(groups)
        # Set the character attributes
        self.name = name
        
        self.collision_sprites = collision_sprites
        
        # Load images for animation
        self.load_images()
        
        # Set animation attributes
        self.action, self.state, self.frame_index = "sword_walk", D_down, 0
        
        # Set sprite attributes
        height, width = pygame.display.get_window_size()
        self.image = self.frames[self.action][self.state][self.frame_index]
        self.rect = self.image.get_rect(center = (height // 2, width // 2))
        self.hitbox = self.rect.inflate(-48 * self.scale, -32 * self.scale)
        
    def load_images(self):
        """Loads all the images for the character. This function is called once during initialization."""
        character_path = os.path.join("assets", "characters", "champion")
        
        for action in self.actions:
            action_surface: pygame.Surface = SpriteSheet(os.path.join(character_path, action + ".png"))
            self.frames[action] = {} # Initialize the action dictionary
            
            for row, direction in enumerate(directions):
                # TODO: We need to find a way to make the number of frames for dynamic for each action because it is not always 6
                self.frames[action][direction] = [action_surface.get_image(row, frame, 64, 64, self.scale) for frame in range(6)]
    
    def animate(self, dt):
        # Get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        
        # Animate
        ## Update the frame index
        if self.action == "sword_walk_attack":
            self.frame_index += 1 * dt
        else:
            self.frame_index += 1 * dt if self.direction else 0
        
        ## Set the new frame as the image
        action_frames = self.frames[self.action][self.state]
        self.image = action_frames[int(self.frame_index) % len(action_frames)]
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[K_RIGHT]) - int(keys[K_LEFT])
        self.direction.y = int(keys[K_DOWN]) - int(keys[K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        
        self.action = "sword_walk_attack" if keys[K_SPACE] else "sword_walk"
    
    def move(self, dt):
        self.hitbox.x += int(self.direction.x * self.speed * dt)
        self.collision('horizontal')
        
        self.hitbox.y += int(self.direction.y * self.speed * dt)
        self.collision('vertical')
        
        # Sync the hitbox with the rect
        self.rect.center = self.hitbox.center
           
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom
                
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)

import pygame
from pygame.locals import *
from entities.maps.region import Region
from settings import *
from entities.characters.character import Character
from entities.maps.sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
import os
from entities.groups import AllSprites

FPS = 60

def collisions():
    """Detects collisions between the player and the map
    example:
    
    Only use collide_mask if it is needed, it is generally highly intensive on performance
    collied_sprites = pygame.sprite.spritecollide(player, enemy_sprites, True, pygame.sprite.collide_mask)
    if collied_sprites:
        player.health -= 10
    
    """
    pass

class App:
    def __init__(self):
        # Init the game the display
        pygame.init()
        self.size = self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup()
        
        # Add the region to the game
        # self.region = Region()
        
        # Add the character to the game
    
    def setup(self):
        worldMap = load_pygame(os.path.join("assets", "maps", "world.tmx"))
        for x, y, image in worldMap.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites,))
        
        for obj in worldMap.get_layer_by_name("Objects"):
            CollisionSprites((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
            
        for obj in worldMap.get_layer_by_name("Collisions"):
            CollisionSprites((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
            
        for obj in worldMap.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Character((obj.x, obj.y), self.all_sprites, self.collision_sprites)
        
    def run(self):
        while( self.running ):
            # Limit the frame rate
            dt = self.clock.tick() / 100
            
            # Parse pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Update the game state
            self.all_sprites.update(dt)
            
            # Render the game view
            # self.region.draw(self.display)
            self.display.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            
            # Update the display
            pygame.display.update()
        pygame.quit()

 
if __name__ == "__main__" :
    ccApp = App()
    ccApp.run()
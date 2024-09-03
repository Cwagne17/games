import pygame
from pygame.locals import *
from entities.maps.region import Region
from settings import *
from entities.characters.character import Character
from entities.maps.sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
import os
from entities.groups import AllSprites
from entities.characters.enemy import OrcBrute


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
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Champion's Conquest")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        # Enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 2000)
        self.spawn_positions = []
        
        # Setup
        self.setup()
        
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
            else:
                self.spawn_positions.append((obj.x, obj.y))
        
    def run(self):
        while( self.running ):
            dt = self.clock.tick() / 100
            
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    OrcBrute(choice(self.spawn_positions), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)
            
            # Update
            self.all_sprites.update(dt)
            
            # Draw
            self.display.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()
 
if __name__ == "__main__" :
    ccApp = App()
    ccApp.run()
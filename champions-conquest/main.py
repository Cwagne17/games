import pygame
from pygame.locals import *
from entities.maps.region import Region
from settings import *
from entities.characters.character import Character
from entities.sprites import *
from random import randint

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
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # Add the region to the game
        self.region = Region()
        
        # Add the character to the game
        self.character = Character("Player 1", self.all_sprites, self.collision_sprites)
        for i in range(6):
            x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            w, h = randint(50, 100), randint(50, 100)
            CollisionSprites((x, y), (w, h), (self.all_sprites, self.collision_sprites))
    
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
            self.region.draw(self.display)
            self.all_sprites.draw(self.display)
            
            # Update the display
            pygame.display.update()
        pygame.quit()

 
if __name__ == "__main__" :
    ccApp = App()
    ccApp.run()
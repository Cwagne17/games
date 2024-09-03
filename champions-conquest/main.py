import pygame
from pygame.locals import *
from entities.maps.region import Region
from entities.characters.character import Character

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
        self.size = self.width, self.height = 1280, 720
        self._display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._clock = pygame.time.Clock()
        self._running = True
        
        # Add the region to the game
        self.region = Region()
        
        # Add the character to the game
        self.all_sprites = pygame.sprite.Group()
        self.character = Character(self.all_sprites, "Player 1", 100, 10)

 
    def on_event(self, event):
        """"Handles native and custom pygame events that are triggered by the user"""
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        """"Hanldes the game play including key presses, mouse clicks, and game specifc logic like moving the player"""
        self.all_sprites.update()
    
    def on_render(self):
        """Renders the view of the game to the screen"""
        self.region.draw(self._display)
        
        # Select each index for 3 frames each
        # frame = (pygame.time.get_ticks() // 180) % 6
        # self.character.draw(self._display, frame)
        
        self.all_sprites.draw(self._display)

        pygame.display.update()
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        """Main game loop that runs the game"""
        while( self._running ):
            # Limit the frame rate
            self._clock.tick(FPS)
            
            # Parse pygame events
            for event in pygame.event.get():
                self.on_event(event)
            
            # Update the game state
            self.on_loop()
            
            # Render the game view
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    ccApp = App()
    ccApp.on_execute()
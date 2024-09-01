import pygame
from pygame.locals import *
from entities.maps.region import Region


FPS = 60

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 720
        self.clock = pygame.time.Clock()
        
        # Add the region to the game
        self.region = Region()
        
        # Init the game the display
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_event(self, event):
        """"Handles native and custom pygame events that are triggered by the user"""
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        """"Hanldes the game play including key presses, mouse clicks, and game specifc logic like moving the player"""
        pass
    
    def on_render(self):
        """Renders the view of the game to the screen"""
        self.region.draw(self._display_surf)
        pygame.display.update()
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        """Main game loop that runs the game"""
        while( self._running ):
            # Limit the frame rate
            self.clock.tick(FPS)
            
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
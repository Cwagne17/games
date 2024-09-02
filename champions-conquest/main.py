import pygame
from pygame.locals import *
from entities.maps.region import Region
from entities.characters.character import Character

FPS = 60

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
        self.character = Character("Player 1", 100, 5)

 
    def on_event(self, event):
        """"Handles native and custom pygame events that are triggered by the user"""
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        """"Hanldes the game play including key presses, mouse clicks, and game specifc logic like moving the player"""
        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            self.character.move_up()
        if keys[K_DOWN] or keys[K_s]:
            self.character.move_down()
        if keys[K_LEFT] or keys[K_a]:
            self.character.move_left()
        if keys[K_RIGHT] or keys[K_d]:
            self.character.move_right()
        if keys[K_SPACE]:
            print("Space bar pressed")
    
    def on_render(self):
        """Renders the view of the game to the screen"""
        self.region.draw(self._display)
        
        # Select each index for 3 frames each
        frame = (pygame.time.get_ticks() // 180) % 6
        self.character.draw(self._display, frame)

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
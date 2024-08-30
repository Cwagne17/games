import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

class GameState():
    # Game limits
    gameWidthLimit: int = 1280
    gameHeightLimit: int = 720
    
    # Player position
    x: int
    y: int
    
    # Bullet positions (list of tuples of x, y)
    bullets: list = []
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gameWidthLimit = x * 2        
        self.gameHeightLimit = y * 2

    def moveLeft(self):
        self.x -= 8
        
        # Check if the player is out of the screen
        if self.x < 0:
            self.x = 0
    
    def moveRight(self):
        self.x += 8
        if self.x > self.gameWidthLimit - 50:
            self.x = self.gameWidthLimit - 50
    
    def moveUp(self):
        self.y -= 8
        # Check if the player is out of the screen
        if self.y < 0:
            self.y = 0

    def moveDown(self):
        self.y += 8
        # Check if the player is out of the screen
        if self.y > self.gameHeightLimit - 50:
            self.y = self.gameHeightLimit - 50
    
    def shoot(self):
        self.bullets.append((self.x, self.y))
    
    def updateBullets(self):
        for i, bullet in enumerate(self.bullets):
            x, y = bullet
            self.bullets[i] = (x, y - 8)
            
            # Remove bullets that are out of the screen
            if y < 0:
                self.bullets.pop(i)

class UserInterface():
    def __init__(self):
        pygame.init()
        self.running = True
        
        # Set the screen size to 1280x720 pixels
        self.window = pygame.display.set_mode((1280,720))

        # Set the window title to "Asteroids"
        pygame.display.set_caption("Asteroids")
        
        # Load the background image and scale it to the screen size
        background = pygame.image.load("assets/space_background.png")
        self.background = pygame.transform.scale(background, (self.window.get_width(), self.window.get_height()))
        self.window.blit(self.background, (0, 0))
        
        # Load the play icon (rocket) and scale it to 50x50 pixels
        player = pygame.image.load("assets/rocket.svg")
        self.player = pygame.transform.scale(player, (50, 50))
        self.window.blit(self.player, (self.window.get_width() / 2, self.window.get_height() / 2))
        
        # Create a clock object to help control the frame rate
        self.clock = pygame.time.Clock()
        
        # Set the player's starting position to the center of the screen
        self.gameState = GameState(self.window.get_width() / 2, self.window.get_height() / 2)
        
        pygame.display.flip()  
        
        
    def processInput(self):
        for event in pygame.event.get():
            # Check if the user has quit the game
            if event.type == pygame.QUIT:
                self.running = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.gameState.moveRight()
            
        if keys[pygame.K_a]:
            self.gameState.moveLeft()
        
        if keys[pygame.K_s]:
            self.gameState.moveDown()
        
        if keys[pygame.K_w]:
            self.gameState.moveUp()
        
        if keys[pygame.K_SPACE]:
            self.gameState.shoot()
        
        # Update existing bullets positions
        self.gameState.updateBullets()
        

    def render(self):
        # Set the background image to the screen
        self.window.blit(self.background, (0, 0))
        
        # Set the player icon to the screen at the player's position
        self.window.blit(self.player, (self.gameState.x, self.gameState.y))
        
        # Draw bullets on the screen
        for bullet in self.gameState.bullets:
            pygame.draw.circle(self.window, (159,238,152), bullet, 2)
        
        pygame.display.flip()  
          

    def run(self):
        while self.running:
            self.processInput()
            self.render()
            self.clock.tick(60)

userInterface = UserInterface()
userInterface.run()

pygame.quit()
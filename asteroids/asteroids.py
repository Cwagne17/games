import os
import pygame
import random

class Asteroid():
    # Health is decreased when the player hits the asteroid
    # with a bullet. When health reaches 0, the asteroid is
    # destroyed.
    health: int
    
    # Asteroid position is randomly generated horizontally
    # and is set to be spawned above the screen
    x: int
    y: int
    
    # Size is randomly generated between 50 and 100 pixels
    size: int = random.randint(50, 100)
    
    # The png image of the asteroid is loaded and scaled to
    # the size of the asteroid
    asteroid: pygame.Surface
    
    def __init__(self, width):
        self.x = random.randint(0, int(width))
        self.y = -self.size
        
        self.health = self.size // 10
        
        asteroidsPath = "assets/asteroids/"
        asteroid = pygame.image.load(os.path.join(asteroidsPath, random.choice(os.listdir(asteroidsPath))))
        self.asteroid = pygame.transform.scale(asteroid, (self.size, self.size))
        
        print(f"Asteroid spawned at {self.x}, {self.y} with size {self.size}")

    def move(self):
        self.y += 1

    def draw(self, window):
        window.blit(self.asteroid, (self.x, self.y))
    
    def hit(self):
        self.health -= 1   

class GameState():
    # Game limits
    gameWidthLimit: int = 1280
    gameHeightLimit: int = 720
    
    # Player position
    x: int
    y: int
    movemenetSpeed: int = 6
    
    # Bullet positions (list of tuples of x, y)
    maxBullets: int = 30
    bullets: list = []
    
    # Asteroid Metadata
    asteroids: list[Asteroid] = []
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gameWidthLimit = x * 2        
        self.gameHeightLimit = y * 2

    def moveLeft(self):
        self.x -= self.movemenetSpeed
        
        # Check if the player is out of the screen
        if self.x < 0:
            self.x = 0
    
    def moveRight(self):
        self.x += self.movemenetSpeed
        if self.x > self.gameWidthLimit - 50:
            self.x = self.gameWidthLimit - 50
    
    def moveUp(self):
        self.y -= self.movemenetSpeed
        # Check if the player is out of the screen
        if self.y < 0:
            self.y = 0

    def moveDown(self):
        self.y += self.movemenetSpeed
        # Check if the player is out of the screen
        if self.y > self.gameHeightLimit - 50:
            self.y = self.gameHeightLimit - 50
    
    def shoot(self):
        # Limit the number of bullets on the screen
        if len(self.bullets) < self.maxBullets:
            self.bullets.append((self.x + 25, self.y))
    
    def updateBullets(self):
        for i, bullet in enumerate(self.bullets):
            x, y = bullet
            self.bullets[i] = (x, y - 8)
            
            # Remove bullets that are out of the screen
            if y < 0:
                self.bullets.pop(i)
    
    def spawnAsteroid(self):
        self.asteroids.append(Asteroid(self.gameWidthLimit))
        
    def moveAsteroids(self):
        for i, asteroid in enumerate(self.asteroids):
            asteroid.move()
            for asteroid in self.asteroids:
                if asteroid.y > self.gameHeightLimit + asteroid.size:
                    self.asteroids.pop(i)
                    
    def checkBulletHitsAsteroid(self):
        print("Checking bullet hits")
        for asteroid in self.asteroids: 
            asteroidCoordinates = (asteroid.x, asteroid.y, asteroid.size)
            print("Asteroids: ", asteroidCoordinates)
            print("Bullets: ", self.bullets)
                   
            xHitbox = range(asteroid.x, asteroid.x + asteroid.size)
            yHitbox = range(asteroid.y, asteroid.y - asteroid.size)
            
            # Check if the bullet is within the asteroid's hitbox
            for bullet in self.bullets:
                if bullet[0] in xHitbox and bullet[1] in yHitbox:
                    asteroid.hit()
                    self.bullets.remove(bullet)
                    
                    if asteroid.health <= 0:
                        self.asteroids.remove(asteroid)

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
        
        # Every 30 frames, create a new asteroid
        if pygame.time.get_ticks() % 1000 == 0:
            self.gameState.spawnAsteroid()
        
        # Move asteroids
        self.gameState.moveAsteroids()
        
        # Check if bullets hit asteroids
        self.gameState.checkBulletHitsAsteroid()

    def render(self):
        # Set the background image to the screen
        self.window.blit(self.background, (0, 0))
        
        # Set the player icon to the screen at the player's position
        self.window.blit(self.player, (self.gameState.x, self.gameState.y))
        
        # Draw bullets on the screen
        for bullet in self.gameState.bullets:
            pygame.draw.circle(self.window, (159,238,152), bullet, 1)
            
        # Draw asteroids on the screen
        for asteroid in self.gameState.asteroids:
            asteroid.draw(self.window)
        
        pygame.display.flip()  
          

    def run(self):
        while self.running:
            self.processInput()
            self.render()
            self.clock.tick(60)

userInterface = UserInterface()
userInterface.run()

pygame.quit()
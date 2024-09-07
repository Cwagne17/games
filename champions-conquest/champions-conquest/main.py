from settings import *
from characters import Character
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from enemy import OrcBrute

class Game:
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
        worldMap = load_pygame(join("assets", "maps", "world.tmx"))
        for x, y, image in worldMap.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))
        
        for obj in worldMap.get_layer_by_name("Objects"):
            CollisionSprites((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
            
        for obj in worldMap.get_layer_by_name("Collisions"):
            CollisionSprites((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        
        for obj in worldMap.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Character((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))
        
    def entity_collisions(self):
        """Detects collisions between the player and the enemies"""
        if self.enemy_sprites:
            collisions = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if collisions:
                for enemy_sprite in collisions:
                    # TODO: The player actions should be vars so the string can't be typoed
                    # we should define it in the player class
                    if self.player.action == "sword_walk_attack":
                        # TODO: We still need to make this do the death animation/hurt animation
                        enemy_sprite.destroy()
                    else:
                        # TODO: This should trigger a hurt animation
                        # there should also be a cooldown so we don't get immediately murked
                        self.player.health -= 10
                    
                    if self.player.health <= 0:
                        # TODO: This needs to implement the death animation
                        # then kill the game at the end of the death animation
                        # we could abstract the self.running to a variable in the
                        # settings.py so we can update it from anywhere
                        self.player.destroy()

    def run(self):
        while( self.running ):
            dt = self.clock.tick() / 100
            
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # if event.type == self.enemy_event:
                #     OrcBrute(choice(self.spawn_positions), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)
            
            # Update
            self.all_sprites.update(dt)
            self.entity_collisions()
            
            # Draw
            self.display.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            
            # TODO: Make this health bar look better
            pygame.draw.rect(self.display, 'black', (19, 10, 104, 20), 2)
            pygame.draw.rect(self.display, 'red', (21, 12, self.player.health, 16))
            
            pygame.display.update()

        pygame.quit()
 
if __name__ == "__main__" :
    game = Game()
    game.run()
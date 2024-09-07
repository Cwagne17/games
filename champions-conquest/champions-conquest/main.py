from settings import *
from sprites import *
from shared import load_sprite_frames
from characters import Champion, OrcBrute
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites


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
        # Load the character frames
        self.champion_frames = load_sprite_frames(C_champion)
        self.orc_brute_frames = load_sprite_frames(C_orc_brute)
        # self.orc_commander_frames = load_sprite_frames(C_orc_commander)
        # self.orc_grunt_frames = load_sprite_frames(C_orc_grunt)

        worldMap = load_pygame(join(ASSETS_PATH, "maps", "world.tmx"))
        for x, y, image in worldMap.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in worldMap.get_layer_by_name("Objects"):
            CollisionSprites(
                (obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites)
            )

        for obj in worldMap.get_layer_by_name("Collisions"):
            CollisionSprites(
                (obj.x, obj.y),
                pygame.Surface((obj.width, obj.height)),
                self.collision_sprites,
            )

        for obj in worldMap.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Champion(
                    (obj.x, obj.y),
                    self.champion_frames,
                    self.all_sprites,
                    self.collision_sprites,
                )
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def entity_collisions(self):
        """Detects collisions between the player and the enemies"""
        if self.enemy_sprites:
            enemy_collisions = pygame.sprite.spritecollide(
                self.player, self.enemy_sprites, False, pygame.sprite.collide_mask
            )

            if enemy_collisions:
                for enemy in enemy_collisions:
                    # self.player.attack(enemy)

                    enemy.attack(self.player)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 100

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    OrcBrute(
                        choice(self.spawn_positions),
                        self.orc_brute_frames,
                        (self.all_sprites, self.enemy_sprites),
                        self.collision_sprites,
                        self.player,
                    )

            # Update
            self.entity_collisions()
            self.all_sprites.update(dt)

            # Draw
            self.display.fill("black")
            self.all_sprites.draw(self.player.rect.center)

            # TODO: Make this health bar look better
            pygame.draw.rect(self.display, "black", (19, 10, 104, 20), 2)
            pygame.draw.rect(self.display, "red", (21, 12, self.player.health, 16))

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

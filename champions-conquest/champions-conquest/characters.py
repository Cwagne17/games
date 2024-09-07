from settings import *
from abc import ABC, abstractmethod


class Character(ABC, pygame.sprite.Sprite):
    hurt_cooldown = 0

    def __init__(
        self,
        position: Tuple[int, int],
        frames: Frames,
        groups: List[pygame.sprite.Group],
        collision_sprite: pygame.sprite.Group,
    ):
        super().__init__(groups)
        # Initialize the character attributes
        self.actions: List[Action] = ACTIONS
        # TODO: For some reason the hurt animation isn't working...
        self.action: Action = A_hurt

        self.direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.facing: Direction = D_down
        self.frame_index: int = 0

        self.frames: Frames = frames
        self.scale: float = SCALE

        self.image: pygame.Surface = self.frames[self.action][self.facing][
            self.frame_index
        ]
        self.rect: pygame.Rect = self.image.get_rect(center=position)
        self.hitbox: pygame.Rect = self.rect.inflate(-48 * self.scale, -48 * self.scale)

        self.collision_sprites: pygame.sprite.Group = collision_sprite

    @abstractmethod
    def get_direction(self) -> None:
        pass

    @abstractmethod
    def get_action(self) -> None:
        pass

    def animate(self, dt: float):
        # Gets the direction the character is facing
        if self.direction.x != 0:
            self.facing = D_right if self.direction.x > 0 else D_left
        if self.direction.y != 0:
            self.facing = D_down if self.direction.y > 0 else D_up

        # Update the frame index
        self.frame_index += dt if self.action not in [A_idle, A_hurt] else 0.5 * dt

        ## Set the new frame as the image
        action_frames = self.frames[self.action][self.facing]
        self.image = action_frames[int(self.frame_index) % len(action_frames)]

    def move(self, dt) -> None:
        # TODO: There is a bug when moving diagonally where the character basically doesn't move at all

        # TODO: once rect's are replaced with frects we can remove the int() cast
        # to allow for more precise movement
        self.hitbox.x += int(self.direction.x * self.speed * dt)
        self.collision("horizontal")

        # TODO: same as above (remove int() cast)
        self.hitbox.y += int(self.direction.y * self.speed * dt)
        self.collision("vertical")

        # Sync the hitbox with the rect
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                if direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def hurt(self, damage: float) -> None:
        # # Cooldown for the hurt or death animation
        if pygame.time.get_ticks() - self.hurt_cooldown > HURT_COOLDOWN:
            self.health -= damage
            self.action = A_hurt if self.health > 0 else A_death
            self.hurt_cooldown = pygame.time.get_ticks()

    def attack(self, character) -> None:
        # TODO: Idea, we could also add more complexity by incoorporating defense attributes of
        # the type of character etc...
        if self.action in [A_attack, A_walk_attack]:
            character.hurt(10)

    def update(self, dt):
        if (
            self.action == A_death
            and pygame.time.get_ticks() - self.hurt_cooldown > HURT_COOLDOWN
        ):
            self.kill()
        else:
            self.get_direction()
            self.get_action()
            self.move(dt)
            self.animate(dt)


class Champion(Character):
    def __init__(
        self,
        position: Tuple[int, int],
        frames: Frames,
        groups: List[pygame.sprite.Group],
        collision_sprites: pygame.sprite.Group,
    ):
        super().__init__(position, frames, groups, collision_sprites)

        # Set sprite attributes
        self.name: str = C_champion
        self.health: int = 100
        self.speed: int = 50

    def get_direction(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[K_d]) - int(keys[K_a])
        self.direction.y = int(keys[K_s]) - int(keys[K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )

    def get_action(self):
        mouse = pygame.mouse.get_pressed()

        if pygame.time.get_ticks() - self.hurt_cooldown > HURT_COOLDOWN:
            if mouse[0]:
                self.action = A_attack
            elif self.direction == pygame.Vector2(0, 0):
                self.action = A_idle
            else:
                self.action = A_walk


class Enemy(Character):
    def __init__(
        self,
        position: Tuple[int, int],
        frames: Frames,
        groups: List[pygame.sprite.Group],
        collision_sprites: pygame.sprite.Group,
        player: Champion,
    ):
        super().__init__(position, frames, groups, collision_sprites)

        # Set sprite attributes
        self.player: Champion = player

    def get_direction(self):
        # The enemy will always move towards the player
        self.direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(
            self.rect.center
        )
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )

    def get_action(self):
        # Calculate the distance between the player and the enemy
        distance = pygame.Vector2(self.player.rect.center) - pygame.Vector2(
            self.rect.center
        )
        self.action = A_attack if distance.magnitude() < 150 else A_walk


class OrcBrute(Enemy):
    def __init__(
        self,
        position: Tuple[int, int],
        frames: Frames,
        groups: List[pygame.sprite.Group],
        collision_sprites: pygame.sprite.Group,
        player: Champion,
    ):
        super().__init__(
            position,
            frames,
            groups,
            collision_sprites,
            player,
        )

        self.name: str = C_orc_brute
        self.health: int = 30
        self.speed: int = 30

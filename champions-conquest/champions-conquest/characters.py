from settings import *
from abc import ABC, abstractmethod
from shared import SpriteSheet


class Character(ABC, pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int], frames: Frames, groups: List[pygame.sprite.Group], collision_sprite: pygame.sprite.Group):
        super().__init__(groups)
        # Initialize the character attributes
        self.actions: List[Action] = ACTIONS
        self.action: Action = A_idle
        
        self.direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.facing: Direction = D_down
        self.frame_index: int = 0
        
        self.frames: Frames = frames
        
        self.image: pygame.Surface = self.frames[self.action][self.facing][self.frame_index]
        self.rect: pygame.Rect = self.image.get_rect(center = position)
        self.hitbox: pygame.Rect = self.rect.inflate(-48 * self.scale, -48 * self.scale)
        
        self.collision_sprites: pygame.sprite.Group = collision_sprite
        
    @abstractmethod
    def get_direction(self) -> None:
        pass

    # TODO: we might be able to implement this in a way that is more dynamic so that we don't have to
    # implement it in every subclass. If we can do this then we don't need to make it abstract
    @abstractmethod
    def animate(self, dt: float) -> None: pass
    
    def move(self, dt) -> None:
        # TODO: once rect's are replaced with frects we can remove the int() cast
        # to allow for more precise movement
        self.hitbox.x += int(self.direction.x * self.speed * dt)
        self.collision('horizontal')
        
        # TODO: same as above (remove int() cast)
        self.hitbox.y += int(self.direction.y * self.speed * dt)
        self.collision('vertical')
        
        # Sync the hitbox with the rect
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom

    # TODO: this needs to be updated to handle the different types of animation actions i.e hurt, dead, attack, etc..
    def update(self, dt):
        if self.death_time == 0:
            # self.input() # input is being replaced with get_direction since we are abstracting it out
            self.get_direction()
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
        
class Champion(Character):
    def __init__(self, position, groups, collision_sprites):
        frames = self.load_images()
        super().__init__(position, frames, groups, collision_sprites)
        
        # Set sprite attributes
        self.name: str = C_champion
        self.health: int = 100
        self.speed: int = 5
        
        self.death_time = 0
        self.death_duration = 400
        
    def animate(self, dt: float):
        # Get state
        if self.direction.x != 0:
            self.facing = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.facing = 'down' if self.direction.y > 0 else 'up'
        
        # Animate
        ## Update the frame index
        ### TODO: The animation is a bit too fast, we need to slow it down
        if self.action == A_walk_attack:
            self.frame_index += 1 * dt
        elif self.action == A_idle:
            self.frame_index += 1 * dt
        else:
            self.frame_index += 1 * dt if self.direction else 0
        
        ## Set the new frame as the image
        action_frames = self.frames[self.action][self.facing]
        self.image = action_frames[int(self.frame_index) % len(action_frames)]
        
    def get_direction(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[K_RIGHT]) - int(keys[K_LEFT])
        self.direction.y = int(keys[K_DOWN]) - int(keys[K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

        # Checks to see if any keys were pressed, if not, we are idle
        if not keys[K_RIGHT] and not keys[K_LEFT] and not keys[K_DOWN] and not keys[K_UP]:
            self.action = A_idle
        else:
            # Otherwise, check to see what the action was
            self.action = A_walk_attack if keys[K_SPACE] else A_walk
                    
    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        # Animation
        surf = pygame.mask.from_surface(self.frames[A_death][self.facing][0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf
        
    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time > self.death_duration:
            self.kill()
                
    def update(self, dt):
        if self.death_time == 0:
            self.input()
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()

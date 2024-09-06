from shared.spritesheet import SpriteSheet
from settings import *
from abc import ABC, abstractmethod

class Character(ABC, pygame.sprite.Sprite):
    """"""
    @property
    @abstractmethod
    def direction(self) -> pygame.Vector2: pass
    
    @property
    @abstractmethod
    def actions(self) -> list: pass
    
    @property
    @abstractmethod
    def action(self) -> str: pass
    
    def __init__(self, groups):
        super().__init__(groups)
        
        # We need to init things like hitboxes and rects here
        # anything that is shared between all characters (health
        # speed, etc..) should be initialized here as well
        
    @abstractmethod
    def get_direction(self) -> None:
        """This function is used to update the direction of the player or
        enemy based on the input from the user. This function is called prior
        to the move function.
        
        Having two separate functions for getting the direction and moving
        allows us to reuse the move function for both the player and the enemy
        while keeping the get_direction function separate for each.
        
        For example, the player's get_direction function would be based on the
        user's input while the enemy's get_direction function would be based on
        the game's logic.
        """
        pass

    # TODO: we might be able to implement this in a way that is more dynamic so that we don't have to
    # implement it in every subclass. If we can do this then we don't need to make it abstract
    @abstractmethod
    def animate(self, dt: float) -> None: pass
    
    def move(self, dt) -> None:
        self.hitbox.x += int(self.direction.x * self.speed * dt)
        self.collision('horizontal')
        
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
    
def Champion(Character):
    def __init__(self, groups):
        super().__init__(groups)
        
        self.actions = [ChampionActions.sword_walk_attack, ChampionActions.sword_walk, ChampionActions.sword_death, ChampionActions.sword_idle]
        self.action = ChampionActions.sword_idle
        
# TODO: This is temporary, we need to find a way to make the number of frames dynamic
# for each action because it is not always 6 (e.g. sword_idle is 12 for up, left, right but 4 for down)
class ChampionActions(enumerate):
    """This class is used to enumerate all the possible actions the champion can perform."""
    sword_walk_attack = {"name": "sword_walk_attack", "len": 6}
    sword_walk = {"name": "sword_walk", "len": 6}
    sword_death = {"name": "sword_death", "len": 6}
    sword_idle = {"name": "sword_idle", "len": 12}

class Character(pygame.sprite.Sprite):
    """This is the base class for all characters in the game."""
    # Positional variables
    direction: pygame.Vector2 = pygame.Vector2(0, 0)
    
    # Animation variables
    ## The following actions define all potential character actions. These actions must match the
    ## name of the file in the assets/characters/champion directory
    actions = [ChampionActions.sword_walk_attack, ChampionActions.sword_walk, ChampionActions.sword_death, ChampionActions.sword_idle]    
    action = ChampionActions.sword_idle # The current action the character is performing
    
    ## This is a dictionary that'll be constructed to hold all the character actions
    ## and their respective frames for each direction [action][direction][frame]
    frames = {}
    frame_index: int = 0 # The current frame index
    scale = 3 # The scale of the character

    # Character attributes
    name: str = "Champion"
    health: int = 100
    speed: int = 50
    
    def __init__(self, position, groups, collision_sprites):
        super().__init__(groups)
        self.collision_sprites = collision_sprites
        
        # Load images for animation
        self.load_images()
        
        # Set animation attributes
        self.action, self.state, self.frame_index = ChampionActions.sword_idle, D_down, 0
        
        # Set sprite attributes
        self.image = self.frames[self.action["name"]][self.state][self.frame_index]
        self.rect = self.image.get_rect(center = position)
        self.hitbox = self.rect.inflate(-48 * self.scale, -48 * self.scale)
        
        self.death_time = 0
        self.death_duration = 400
        
    def load_images(self):
        """Loads all the images for the character. This function is called once during initialization."""
        character_path = join("assets", "characters", "champion")
        
        for action in self.actions:
            action_surface: pygame.Surface = SpriteSheet(join(character_path, action["name"] + ".png"))
            self.frames[action["name"]] = {} # Initialize the action dictionary
            
            for row, direction in enumerate(DIRECTIONS):
                # TODO: We need to find a way to make the number of frames for dynamic for each action because it is not always 6
                self.frames[action['name']][direction] = [action_surface.get_image(row, frame, 64, 64, self.scale) for frame in range(action["len"])]
    
    def animate(self, dt):
        # Get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        
        # Animate
        ## Update the frame index
        ### TODO: The animation is a bit too fast, we need to slow it down
        if self.action["name"] == "sword_walk_attack":
            self.frame_index += 1 * dt
        elif self.action["name"] == "sword_idle":
            self.frame_index += 1 * dt
        else:
            self.frame_index += 1 * dt if self.direction else 0
        
        ## Set the new frame as the image
        action_frames = self.frames[self.action["name"]][self.state]
        self.image = action_frames[int(self.frame_index) % self.action['len']]
        
    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[K_RIGHT]) - int(keys[K_LEFT])
        self.direction.y = int(keys[K_DOWN]) - int(keys[K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

        # Checks to see if any keys were pressed, if not, we are idle
        if not keys[K_RIGHT] and not keys[K_LEFT] and not keys[K_DOWN] and not keys[K_UP]:
            self.action = ChampionActions.sword_idle
        else:
            # Otherwise, check to see what the action was
            self.action = ChampionActions.sword_walk_attack if keys[K_SPACE] else ChampionActions.sword_walk
    
    def move(self, dt):
        self.hitbox.x += int(self.direction.x * self.speed * dt)
        self.collision('horizontal')
        
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
                    
    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        # Animation
        surf = pygame.mask.from_surface(self.frames["sword_death"][self.state][0]).to_surface()
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

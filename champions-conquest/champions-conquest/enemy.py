from settings import *
from shared.spritesheet import SpriteSheet

class OrcBrute(pygame.sprite.Sprite):
    # Animation variables
    ## The following actions define all potential character actions. These actions must match the
    ## name of the file in the assets/characters/champion directory
    actions = ["walk_attack", "walk"]
    action = "walk" # The current action the character is performing
    
    ## This is a dictionary that'll be constructed to hold all the character actions
    ## and their respective frames for each direction [action][direction][frame]
    frames = {}
    frame_index: int = 0 # The current frame index
    scale = 3 # The scale of the character

    # Character attributes
    name: str = "Orc Brute"
    health: int = 100
    speed: int = 20
    
    def __init__(self, position, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        
        self.load_images()
        
        self.action, self.state, self.frame_index = "walk", D_down, 0
        self.animation_speed = 1
        
        self.image = self.frames[self.action][self.state][self.frame_index]
        self.rect = self.image.get_rect(center = position)
        self.hitbox = self.rect.inflate(-48 * self.scale, -48 * self.scale)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2(0, 0)
        
        self.death_time = 0
        self.death_duration = 400
    
    ## TODO: This needs to be abstracted out of the class so it doesn't have to load every time the
    ## class is instantiated (maybe singleton pattern?) Anyway, this function is causing a little bit
    ## of lag when there are many enemies on the screen
    def load_images(self):
        """Loads all the images for the character. This function is called once during initialization."""
        character_path = join("assets", "characters", "enemies", "orcs", "brute")
        
        for action in self.actions:
            action_surface: pygame.Surface = SpriteSheet(join(character_path, action + ".png"))
            self.frames[action] = {} # Initialize the action dictionary
            
            for row, direction in enumerate(DIRECTIONS):
                # TODO: We need to find a way to make the number of frames for dynamic for each action because it is not always 6
                self.frames[action][direction] = [action_surface.get_image(row, frame, 64, 64, self.scale) for frame in range(6)]
    
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        
        action_frames = self.frames[self.action][self.state]
        self.image = action_frames[int(self.frame_index) % len(action_frames)]
    
    def move(self, dt):
        # The enemy will always move towards the player
        self.direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)
        if self.direction:
            self.direction = self.direction.normalize()
        
        ## TODO: We should also make the path finding a little bit more advanced by
        ## having a range the enemy can view the player if they are certain distance away
        ## use vector magnitude to determine if the player is within range
        
        # update rect position + collision logic
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        
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
    
    def attack(self):
        self.player.health -= 10
        
    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        # Animation
        surf = pygame.mask.from_surface(self.frames["walk"][self.state][0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf
        
    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time > self.death_duration:
            self.kill()
    
    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
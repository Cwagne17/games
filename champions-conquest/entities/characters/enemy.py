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
    speed: int = 50
    
    def __init__(self, position, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        
        self.load_images()
        
        self.action, self.state, self.frame_index = "walk", D_down, 0
        
        self.image = self.frames[self.action][self.state][self.frame_index]
        self.rect = self.image.get_rect(center = position)
        self.hitbox = self.rect.inflate(-20 * self.scale, -20 * self.scale)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2(0, 0)
    
    def load_images(self):
        """Loads all the images for the character. This function is called once during initialization."""
        character_path = join("assets", "characters", "enemies", "orcs", "brute")
        
        for action in self.actions:
            action_surface: pygame.Surface = SpriteSheet(join(character_path, action + ".png"))
            self.frames[action] = {} # Initialize the action dictionary
            
            for row, direction in enumerate(DIRECTIONS):
                # TODO: We need to find a way to make the number of frames for dynamic for each action because it is not always 6
                self.frames[action][direction] = [action_surface.get_image(row, frame, 64, 64, self.scale) for frame in range(6)]
    
    def update(self, dt):
        pass
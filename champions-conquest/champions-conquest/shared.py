from settings import *

# This is just being kept here for now so we have a utility function that can be imported to load images
# it probably needs to be updated so it is more generic and not just assets/player/* but for now its ok
# This is when importing images that are numbered and each animation is separate file rather then a sprite sheet
# like we have seen in the past

def load_images(self):
        """Loads the images for the character sprite in folders named left, right, up, and down
        
        This function expects that the file names are organized in alphabetical order
        """
        self.frames = {D_left: [], D_right: [], D_up: [], D_down: []}
        
        for state in self.frames.keys():
            for folder_path, _, file_names in walk(join('assets', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surface = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surface)

def load_sprite_frames(character_class: Class, scale: Optional[float] = 3.0) -> Frames:
    """Loads the sprite frames for a character

    Args:
        character_class (Class): The character class to load the frames for
        scale (Optional[float], optional): The scale to resize the image. Defaults to 3.0.

    Returns:
        Frames: The frames for the character
    """
    frames: Frames = {}
    directory_path = join(ASSETS_PATH, "characters", character_class)
    for action in ACTIONS:
        frames[action] = {} # Initialize the action dictionary

        action_surface: SpriteSheet = SpriteSheet(join(directory_path, action + ".png"))
        for row, direction in enumerate(DIRECTIONS):
            frames[action][direction] = [action_surface.get_image(row, frame, TILE_SIZE, TILE_SIZE, scale) for frame in range(CHARACTER_ACTION_FRAMES[action][character_class])]
    

class SpriteSheet():
    def __init__(self, image):
        self.sheet = pygame.image.load(image).convert_alpha()

    def get_image(self, row: int, frame: int, width: int, height: int, scale: float):
        """Returns a scaled image from the sprite sheet

        Args:
            row (int): The row of the sprite sheet (uses height * row to get the starting y position)
            frame (int): The frame of the sprite sheet (uses width * frame to get the starting x position)
            width (int): The width of the sprite
            height (int): The height of the sprite
            scale (float): The scale to resize the image

        Returns:
            pygame.Surface: The scaled image from the sprite sheet
        """
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), (row * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0, 0, 0))
        return image
import pygame

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
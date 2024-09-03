import pygame

class CollisionSprites(pygame.sprite.Sprite):
    def __init__(self, position, size, groups):
        super().__init__(groups)
        
        self.image = pygame.Surface(size)
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = position)
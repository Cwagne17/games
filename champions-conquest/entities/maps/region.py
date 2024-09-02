import pygame
from .tile import *

tile_map = [
    # Top Water Edge
    [W_c] * 40,
    [W_c] * 40,
    
    # Grass Section with proper edges and corners
    [W_c, W_c, G_tlc] + [G_te] * 35 + [G_trc, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
    [W_c, W_c, G_blc] + [G_be] * 35 + [G_brc, W_c],
    
    # Bottom Water Edge
    [W_c] * 40,
    [W_c] * 40
]

class Region():
    tile_map = tile_map
    # tile_map = [
    #     [W_c, W_c, W_c, W_c, W_c],
    #     [G_tlc, G_te, G_te, G_te, G_trc],
    #     [G_le, G_c, G_c, G_c, G_re],
    #     [G_le, G_c, G_c, G_c, G_re],
    #     [G_le, G_c, G_c, G_c, G_re],
    #     [G_le, G_c, G_c, G_c, G_re],
    #     [G_blc, G_be, G_be, G_be, G_brc],
    #     [W_c, W_c, W_c, W_c, W_c],
    #     [W_c, W_c, W_c, W_c, W_c],
    #     [W_c, W_c, W_c, W_c, W_c],        
    # ]
    
    def __init__(self):
        pass
        
    def draw(self, window):
        for y, tiles in enumerate(self.tile_map):
            for x, tile in enumerate(tiles):
                tile_image = pygame.image.load(tile)
                
                # Each image is 32x32 pixels
                window.blit(tile_image, (x * 32, y * 32))
        
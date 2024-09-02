import pygame


ASSETS_PATH = "assets/Tiles/"
ASSETS_OBJECT_PATH = "assets/Objects/"
# Tile Constants
# The naming convention being used for the different tile types is as follows:
# [Tile Type]_[Tile Variant]
#
# For example, each tile has many types based on the edges, corners, and center of the tile.
#

# Grass tile types
G_c = ASSETS_PATH + "grass/grass_c.png"
G_tlc = ASSETS_PATH + "grass/grass_tlc.png"
G_le = ASSETS_PATH + "grass/grass_le.png"
G_blc = ASSETS_PATH + "grass/grass_blc.png"
G_be = ASSETS_PATH + "grass/grass_be.png"
G_brc = ASSETS_PATH + "grass/grass_brc.png"
G_re = ASSETS_PATH + "grass/grass_re.png"
G_trc = ASSETS_PATH + "grass/grass_trc.png"
G_te = ASSETS_PATH + "grass/grass_te.png"

W_lt_fl = ASSETS_PATH + "water/light_ocean_full.png"
W_dk_fl = ASSETS_PATH + "water/dark_ocean_full.png"
W_dk_lft_lt_rgt = ASSETS_PATH + "water/dark_left_light_right.png"
W_lt_lft_dk_rgt = ASSETS_PATH + "water/light_left_dark_right.png"
W_lt_tp_dk_bt = ASSETS_PATH + "water/light_tp_dark_bt.png"
W_dk_tp_lt_bt = ASSETS_PATH + "water/dark_tp_light_bt.png"
W_dk_lt_btl = ASSETS_PATH + "water/dark_light_btl.png"
W_dk_lt_btr = ASSETS_PATH + "water/dark_light_btr.png"
W_dk_lt_tpl = ASSETS_PATH + "water/dark_light_tpl.png"
W_dk_lt_tpr = ASSETS_PATH + "water/dark_light_tpr.png"
W_lt_dk_btl = ASSETS_PATH + "water/light_dark_btl.png"
W_lt_dk_btr = ASSETS_PATH + "water/light_dark_btr.png"
W_lt_dk_tpl = ASSETS_PATH + "water/light_dark_tpl.png"

# Objects

# Bushes
BUSH_1 = ASSETS_OBJECT_PATH + "Bushes/1.png"
BUSH_2 = ASSETS_OBJECT_PATH + "Bushes/2.png"
BUSH_3 = ASSETS_OBJECT_PATH + "Bushes/3.png"
BUSH_4 = ASSETS_OBJECT_PATH + "Bushes/4.png"
BUSH_5 = ASSETS_OBJECT_PATH + "Bushes/5.png"
BUSH_6 = ASSETS_OBJECT_PATH + "Bushes/6.png"

# Trees
TREE_1 = ASSETS_OBJECT_PATH + "Trees/1.png"
TREE_2 = ASSETS_OBJECT_PATH + "Trees/2.png"
TREE_3 = ASSETS_OBJECT_PATH + "Trees/3.png"
TREE_4 = ASSETS_OBJECT_PATH + "Trees/4.png"
TREE_5 = ASSETS_OBJECT_PATH + "Trees/5.png"
TREE_6 = ASSETS_OBJECT_PATH + "Trees/6.png"
TREE_7 = ASSETS_OBJECT_PATH + "Trees/7.png"
TREE_8 = ASSETS_OBJECT_PATH + "Trees/8.png"
TREE_9 = ASSETS_OBJECT_PATH + "Trees/9.png"

# Grass
GRASS_1 = ASSETS_OBJECT_PATH + "Grass/1.png"
GRASS_2 = ASSETS_OBJECT_PATH + "Grass/2.png"
GRASS_3 = ASSETS_OBJECT_PATH + "Grass/3.png"
GRASS_4 = ASSETS_OBJECT_PATH + "Grass/4.png"
GRASS_5 = ASSETS_OBJECT_PATH + "Grass/5.png"
GRASS_6 = ASSETS_OBJECT_PATH + "Grass/6.png"
GRASS_7 = ASSETS_OBJECT_PATH + "Grass/7.png"
GRASS_8 = ASSETS_OBJECT_PATH + "Grass/8.png"
GRASS_9 = ASSETS_OBJECT_PATH + "Grass/9.png"
GRASS_10 = ASSETS_OBJECT_PATH + "Grass/10.png"
import random

class Tile:
    def __init__(self, tile_type, x, y, noise):
        self.noise = noise
        self.tile_type = tile_type
        self.foliage = None
        if tile_type == G_c and noise < -0.01:
            # Randomly select a grass tile variant
            self.foliage = random.choice([GRASS_1, GRASS_2, GRASS_3, GRASS_4, GRASS_5, GRASS_6, GRASS_7, GRASS_8, GRASS_9, GRASS_10])
        self.x = x
        self.y = y
        self.image = pygame.image.load(tile_type)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x * 32, self.rect.y * 32))
        # Draw foliage
        if self.foliage and self.tile_type == G_c:
            foliage_image = pygame.image.load(self.foliage)
            screen.blit(foliage_image, (self.rect.x * 32, self.rect.y * 32))
    
    def update_tile(self, tile_type):
        self.tile_type = tile_type
        self.image = pygame.image.load(tile_type)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        return self
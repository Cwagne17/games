import logging
import numpy as np
import pygame
from .tile import *
import noise
from PIL import Image
# tile_map = [
#     # Top Water Edge
#     [W_c] * 40,
#     [W_c] * 40,
    
#     # Grass Section with proper edges and corners
#     [W_c, W_c, G_tlc] + [G_te] * 35 + [G_trc, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_le] + [G_c] * 35 + [G_re, W_c],
#     [W_c, W_c, G_blc] + [G_be] * 35 + [G_brc, W_c],
    
#     # Bottom Water Edge
#     [W_c] * 40,
#     [W_c] * 40
# ]

class Direction(enumerate):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    NORTH_EAST = 4
    NORTH_WEST = 5
    SOUTH_EAST = 6
    SOUTH_WEST = 7

def create_noise_map(shape=(40, 40), scale=100, octaves=6, persistence=0.5, lacunarity=2):
    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.pnoise2(i/scale,
                                        j/scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=1024,
                                        repeaty=1024,
                                        base=2)
    img = Image.fromarray((world * 255).astype('uint8'), 'L')
    img.save('world_gen.png')
    return world


def create_tile_map():
    print("Creating tile map")
    world  = create_noise_map()
    tile_map = []
    for i in range(world.shape[0]):
        row = []
        for j in range(world.shape[1]):
            if world[i][j] >= 0.05:
                row.append(Tile(W_dk_fl, j, i, world[i][j]))
            elif world[i][j] >= 0:
                row.append(Tile(W_lt_fl, j, i, world[i][j]))
            else:
                row.append(Tile(G_c, j, i, world[i][j]))
        tile_map.append(row)
    print("Tile map created")

    # Go through the tile map and set the edges of the water tiles to dirt whereever grass is adjacent
    beach_tiles = []
    for y in range(1, len(tile_map) - 1):
        for x in range(1, len(tile_map[y]) - 1):
            if tile_map[y][x].tile_type == W_lt_fl:
                if tile_map[y - 1][x].tile_type == G_c: # Top
                    beach_tiles.append((x, y - 1, Direction.NORTH))
                if tile_map[y + 1][x].tile_type == G_c: # Bottom
                    beach_tiles.append((x, y + 1, Direction.SOUTH))
                if tile_map[y][x - 1].tile_type == G_c: # Left
                    beach_tiles.append((x - 1, y, Direction.WEST))
                if tile_map[y][x + 1].tile_type == G_c: # Right
                    beach_tiles.append((x + 1, y, Direction.EAST))
                if tile_map[y - 1][x - 1].tile_type == G_c: # Top Left
                    beach_tiles.append((x - 1, y - 1, Direction.NORTH_WEST))
                if tile_map[y - 1][x + 1].tile_type == G_c: # Top Right
                    beach_tiles.append((x + 1, y - 1, Direction.NORTH_EAST))
                if tile_map[y + 1][x - 1].tile_type == G_c: # Bottom Left
                    beach_tiles.append((x - 1, y + 1, Direction.SOUTH_WEST))
                if tile_map[y + 1][x + 1].tile_type == G_c: # Bottom Right
                    beach_tiles.append((x + 1, y + 1, Direction.SOUTH_EAST))
    for x, y, dir in beach_tiles:
        if dir == Direction.NORTH:
            tile_map[y][x] = tile_map[y][x].update_tile(G_be)
        elif dir == Direction.SOUTH:
            tile_map[y][x] = tile_map[y][x].update_tile(G_te)
        elif dir == Direction.WEST:
            tile_map[y][x] = tile_map[y][x].update_tile(G_re) 
        elif dir == Direction.EAST:
            tile_map[y][x] = tile_map[y][x].update_tile(G_le) 
        # elif dir == Direction.NORTH_WEST:
        #     tile_map[y][x] = G_brc
        # elif dir == Direction.NORTH_EAST:
        #     tile_map[y][x] = G_blc
        # elif dir == Direction.SOUTH_WEST:
        #     tile_map[y][x] = G_trc
        # elif dir == Direction.SOUTH_EAST:
        #     tile_map[y][x] = G_tlc
    save_map_to_image(tile_map) 
    return tile_map

def save_map_to_image(tile_map):
    print("Saving map to image")
    # map_img = []
    # load the tile images
    # for y, tiles in enumerate(tile_map):
    #     row = []
    #     for x, tile in enumerate(tiles):
    #         row.append(tile.image)
    #     map_img.append(row)
    print("Tile images loaded")
    map_surface = pygame.Surface((len(tile_map[0]) * 32, len(tile_map) * 32))
    for y, tiles in enumerate(tile_map):
        for x, tile in enumerate(tiles):
            tile.draw(map_surface)
    print("Map surface created")
    pygame.image.save(map_surface, "map.png")
    # exit()

class Region(pygame.sprite.Sprite):
    tile_map =  create_tile_map()
    
    def __init__(self):
        pass
        
    def draw(self, window):
        for y, tiles in enumerate(self.tile_map):
            for x, tile in enumerate(tiles):
                tile.draw(window)
        
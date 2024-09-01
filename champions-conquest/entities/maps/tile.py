from enum import Enum

ASSETS_PATH = "assets/Tiles/"

class Tile(Enum):
    # Grass tile types
    GRASS = ASSETS_PATH + "grass/grass.png"
    
    WATER = ASSETS_PATH + "water/water.png"
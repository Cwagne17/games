import noise
import numpy as np
from PIL import Image

shape = (1024, 1024)
scale = 300
octaves = 6
persistence = 0.5
lacunarity = 2.0

"""
Generate a 2D array of Perlin noise
"""

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
                                    base=10)

blue = [65,105,225]
green = [34,139,34]
beach = [238,214,175]

def add_color(world):
    color_world = np.zeros(world.shape+(3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.05:
                color_world[i][j] = blue
            elif world[i][j] < 0:
                color_world[i][j] = beach
            else:
                color_world[i][j] = green

    return color_world

"""
Create an island in the middle of the world
"""
color_world = add_color(world)

a,b = shape[0]/2, shape[1]/2
n = 1024
r = 125
y,x = np.ogrid[-a:n-a, -b:n-b]
# creates a mask with True False values at indices
mask = x**2 + y**2 <= r**2

black = [0,0,0]
island_world = np.zeros_like(color_world)

for i in range(shape[0]):
    for j in range(shape[1]):
        if mask[i][j]:
            island_world[i][j] = color_world[i][j]
        else:
            island_world[i][j] = black

"""
Create a gradient that is 1 in the center and 0 at the edges
"""

import math
center_x, center_y = shape[1] // 2, shape[0] // 2
circle_grad = np.zeros_like(world)

for y in range(world.shape[0]):
    for x in range(world.shape[1]):
        distx = abs(x - center_x)
        disty = abs(y - center_y)
        dist = math.sqrt(distx**2 + disty**2)
        circle_grad[y][x] = dist

# Get it between -1 and 1
max_grad = np.max(circle_grad)
circle_grad = circle_grad / max_grad
circle_grad -= 0.5
circle_grad *= 2.0
circle_grad = -circle_grad

# shrink gradient
for y in range(world.shape[0]):
    for x in range(world.shape[1]):
        if circle_grad[y][x] > 0:
            circle_grad[y][x] *= 20

# get it to be between 0 and 1
max_grad = np.max(circle_grad)
circle_grad = circle_grad / max_grad

world_noise = np.zeros_like(world)

for i in range(shape[0]):
    for j in range(shape[1]):
        world_noise[i][j] = (world[i][j] * circle_grad[i][j])
        if world_noise[i][j] > 0:
            world_noise[i][j] *= 20

# get it to be between 0 and 1
max_grad = np.max(world_noise)
world_noise = world_noise / max_grad

lightblue = [0,191,255]
blue = [65,105,225]
green = [34,139,34]
darkgreen = [0,100,0]
sandy = [210,180,140]
beach = [238, 214, 175]
snow = [255, 250, 250]
mountain = [139, 137, 137]

threshold = 0

def add_color2(world):
    color_world = np.zeros(world.shape+(3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < threshold + 0.05:
                color_world[i][j] = blue
            elif world[i][j] < threshold + 0.055:
                color_world[i][j] = sandy
            elif world[i][j] < threshold + 0.1:
                color_world[i][j] = beach
            elif world[i][j] < threshold + 0.25:
                color_world[i][j] = green
            elif world[i][j] < threshold + 0.6:
                color_world[i][j] = darkgreen
            elif world[i][j] < threshold + 0.7:
                color_world[i][j] = mountain
            elif world[i][j] < threshold + 1.0:
                color_world[i][j] = snow

    return color_world

color_world = add_color2(world_noise)

img = Image.fromarray(color_world.astype('uint8'), 'RGB')
img.save('world_noise_color.png')

img = Image.fromarray((world_noise * 255).astype('uint8'), 'L')
img.save('world_noise.png')


img = Image.fromarray((world * 255).astype('uint8'), 'L')
img.save('world.png')

img = Image.fromarray(island_world.astype('uint8'), 'RGB')
img.save('world_island.png')

img = Image.fromarray((circle_grad * 255).astype('uint8'), 'L')
img.save('circle_grad.png')



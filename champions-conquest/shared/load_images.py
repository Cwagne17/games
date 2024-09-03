import os
import pygame

# This is just being kept here for now so we have a utility function that can be imported to load images
# it probably needs to be updated so it is more generic and not just assets/player/* but for now its ok
# This is when importing images that are numbered and each animation is separate file rather then a sprite sheet
# like we have seen in the past

def load_images(self):
        """Loads the images for the character sprite in folders named left, right, up, and down
        
        This function expects that the file names are organized in alphabetical order
        """
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        
        for state in self.frames.keys():
            for folder_path, _, file_names in os.walk(os.path.join('assets', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = os.path.join(folder_path, file_name)
                        surface = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surface)
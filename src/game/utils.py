from game import config
import pygame
import os

def load_image(name, size):
    path = name # if os.path.isabs(name) else os.path.join(config.ASSETS_PATH, name)
    if not os.path.exists(path):
        print(f"Image file '{path}' does not exist.")
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except pygame.error as e:
        print(f"Failed to load image '{path}': {e}")
        return None

def load_high_score(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return int(f.read())
    return 0

def save_high_score(file_path, score):
    with open(file_path, "w") as f:
        f.write(str(score))

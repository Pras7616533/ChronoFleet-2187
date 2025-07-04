import pygame
import os

def load_image(name, size):
    path = os.path.join("assets", name)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

def load_high_score(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return int(f.read())
    return 0

def save_high_score(file_path, score):
    with open(file_path, "w") as f:
        f.write(str(score))

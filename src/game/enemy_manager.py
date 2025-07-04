import pygame
import random

def spawn_enemies(enemy_basic_img, enemy_medium_img, enemy_strong_img, enemy_size):
    enemies = []
    rows = random.randint(3, 6)
    cols = random.randint(5, 9)
    for row in range(rows):
        for col in range(cols):
            x = 100 + col * 70
            y = 50 + row * 60
            rect = pygame.Rect(x, y, *enemy_size)
            if row == 0:
                image = enemy_strong_img
                points = 30
            elif row == 1:
                image = enemy_medium_img
                points = 20
            else:
                image = enemy_basic_img
                points = 10
            enemies.append({"rect": rect, "image": image, "points": points})
    return enemies

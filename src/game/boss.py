import pygame

class Boss:
    def __init__(self, x, y, image, health=50, speed=2):
        self.rect = pygame.Rect(x, y, 120, 80)
        self.image = pygame.transform.scale(image, (120, 80))
        self.health = health
        self.speed = speed
        self.direction = 1  # 1 = right, -1 = left

    def update(self, screen_width):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.direction *= -1

    def draw(self, win):
        win.blit(self.image, self.rect)
        pygame.draw.rect(win, (255, 0, 0), (self.rect.x, self.rect.y - 10, 120, 5))
        pygame.draw.rect(win, (0, 255, 0), (self.rect.x, self.rect.y - 10, 120 * (self.health / 50), 5))

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

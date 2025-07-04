import pygame

class InputBox:
    def __init__(self, x, y, w, h, font, placeholder='', is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = ''
        self.font = font
        self.txt_surface = font.render(placeholder, True, self.color)
        self.active = False
        self.placeholder = placeholder
        self.is_password = is_password

    def update_text(self):
        if not self.text and self.placeholder:
            self.display_text = self.placeholder
        else:
            if self.is_password:
                self.display_text = '*' * len(self.text) if self.text else self.placeholder
            elif self.text:
                self.display_text = self.text
        self.txt_surface = self.font.render(self.display_text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 20:
                    self.text += event.unicode
            self.update_text()
        return None
    
    def set_text(self, text):
        self.text = text
        self.update_text()
        
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

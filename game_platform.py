import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (69, 57, 55), self.rect, 2, border_radius=5)
        pygame.draw.line(screen, (182, 137, 94), (self.rect.left + 5, self.rect.top + 4),
                         (self.rect.right - 5, self.rect.top + 4), 3)

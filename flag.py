import pygame


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 45, 60)

    def draw(self, screen):
        pole_x = self.rect.left + 5
        pygame.draw.line(screen, (90, 68, 51), (pole_x, self.rect.bottom), (pole_x, self.rect.top), 5)
        wave = (pygame.time.get_ticks() // 80) % 5
        points = ((pole_x + 2, self.rect.top + 4), (pole_x + 34, self.rect.top + 8 + wave),
                  (pole_x + 28, self.rect.top + 23), (pole_x + 2, self.rect.top + 20))
        pygame.draw.polygon(screen, (248, 224, 112), points)
        pygame.draw.circle(screen, (255, 248, 205), (pole_x, self.rect.top), 4)

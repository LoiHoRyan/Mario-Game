import pygame


class Collectible(pygame.sprite.Sprite):
    COLORS = {"coin": (255, 202, 55), "star": (255, 240, 95), "heart": (244, 93, 125)}

    def __init__(self, x, y, value, kind="coin"):
        super().__init__()
        self.kind = kind
        self.value = value
        self.width = self.height = 22 if kind != "coin" else 18
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.base_y = y
        self.tick = 0
        self.color = self.COLORS.get(kind, self.COLORS["coin"])

    def draw(self, screen):
        self.tick += 1
        bob_y = round(3 * pygame.math.Vector2(0, 1).rotate(self.tick * 4).y)
        center = (self.rect.centerx, self.rect.centery + bob_y)
        if self.kind == "heart":
            x, y = center
            pygame.draw.circle(screen, self.color, (x - 4, y - 2), 6)
            pygame.draw.circle(screen, self.color, (x + 4, y - 2), 6)
            pygame.draw.polygon(screen, self.color, ((x - 10, y), (x + 10, y), (x, y + 11)))
        elif self.kind == "star":
            points = []
            for i in range(10):
                import math
                angle = -math.pi / 2 + i * math.pi / 5
                radius = 10 if i % 2 == 0 else 4
                points.append((center[0] + math.cos(angle) * radius,
                               center[1] + math.sin(angle) * radius))
            pygame.draw.polygon(screen, self.color, points)
        else:
            pygame.draw.ellipse(screen, self.color, (center[0] - 7, center[1] - 9, 14, 18))
            pygame.draw.line(screen, (255, 247, 190), (center[0], center[1] - 5), (center[0], center[1] + 5), 2)

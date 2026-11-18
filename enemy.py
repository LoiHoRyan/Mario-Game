import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, min_x, max_x, kind="walker", speed=1.6):
        super().__init__()
        self.width = 30 if kind == "hopper" else 32
        self.height = 28
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.min_x = min_x
        self.max_x = max(min_x + self.width, max_x)
        self.velocity_x = abs(speed)
        self.direction = 1
        self.velocity_y = 0.0
        self.gravity = 0.55
        self.kind = kind
        self.color = (103, 77, 146) if kind == "hopper" else (94, 66, 52)
        self.grounded = False
        self.tick = 0

    def update(self, platforms, screen_width):
        self.tick += 1
        # Patrol bounds are inclusive and account for the sprite width.
        self.rect.x += round(self.velocity_x * self.direction)
        if self.rect.left <= self.min_x:
            self.rect.left = self.min_x
            self.direction = 1
        elif self.rect.right >= self.max_x:
            self.rect.right = self.max_x
            self.direction = -1

        if self.kind == "hopper" and self.grounded and self.tick % 95 == 0:
            self.velocity_y = -8
            self.grounded = False
        self.velocity_y = min(self.velocity_y + self.gravity, 12)
        self.rect.y += round(self.velocity_y)
        self.grounded = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.grounded = True

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        eye_y = self.rect.y + 9
        pygame.draw.circle(screen, (255, 245, 220), (self.rect.centerx - 6, eye_y), 4)
        pygame.draw.circle(screen, (255, 245, 220), (self.rect.centerx + 6, eye_y), 4)
        pupil_shift = self.direction * 1
        pygame.draw.circle(screen, (35, 31, 40), (self.rect.centerx - 6 + pupil_shift, eye_y), 2)
        pygame.draw.circle(screen, (35, 31, 40), (self.rect.centerx + 6 + pupil_shift, eye_y), 2)
        pygame.draw.arc(screen, (48, 36, 43), (self.rect.x + 8, self.rect.y + 13, 16, 10), 3.3, 6.1, 2)

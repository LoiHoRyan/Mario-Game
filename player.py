import pygame


class Player(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 30, 44

    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.start_x, self.start_y = x, y
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = 5.2
        self.jump_power = 14.5
        self.gravity = 0.65
        self.max_fall_speed = 15
        self.facing = 1
        self.is_jumping = True
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.previous_bottom = self.rect.bottom
        self.score = 0
        self.coins = 0
        self.lives = 3
        self.invulnerability_timer = 0
        self.star_timer = 0
        self.dash_cooldown = 0
        self.dash_timer = 0
        self.animation_tick = 0

    @property
    def invulnerable(self):
        return self.invulnerability_timer > 0 or self.star_timer > 0

    def set_horizontal_input(self, direction):
        if direction:
            self.facing = 1 if direction > 0 else -1
        self.velocity_x = direction * self.speed

    def jump(self):
        self.jump_buffer = 8

    def dash(self):
        if self.dash_cooldown <= 0:
            self.dash_timer = 8
            self.dash_cooldown = 45
            self.velocity_x = self.facing * 12
            self.velocity_y = min(self.velocity_y, 1)

    def collect(self, item):
        self.score += item.value
        if item.kind == "coin":
            self.coins += 1
            if self.coins % 10 == 0:
                self.lives += 1
        elif item.kind == "star":
            self.star_timer = 60 * 6
        elif item.kind == "heart":
            self.lives = min(5, self.lives + 1)

    def update(self, platforms, screen_width, screen_height):
        self.previous_bottom = self.rect.bottom
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1
        if self.star_timer > 0:
            self.star_timer -= 1
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.dash_timer > 0:
            self.dash_timer -= 1

        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        if self.on_ground:
            self.coyote_timer = 7
        elif self.coyote_timer > 0:
            self.coyote_timer -= 1
        if self.jump_buffer > 0 and self.coyote_timer > 0:
            self.velocity_y = -self.jump_power
            self.on_ground = False
            self.is_jumping = True
            self.coyote_timer = 0
            self.jump_buffer = 0

        if self.dash_timer == 0:
            # Keep keyboard movement responsive, with a little inertia when released.
            if self.velocity_x and abs(self.velocity_x) <= self.speed:
                self.velocity_x *= 0.82
                if abs(self.velocity_x) < 0.25:
                    self.velocity_x = 0
        self.velocity_y = min(self.velocity_y + self.gravity, self.max_fall_speed)

        # Resolve horizontal and vertical collisions independently, preventing tunneling and wall sticking.
        self.rect.x += round(self.velocity_x)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right
                self.velocity_x = 0
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen_width, self.rect.right)

        self.rect.y += round(self.velocity_y)
        self.on_ground = False
        for platform in platforms:
            if not self.rect.colliderect(platform.rect):
                continue
            if self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
            elif self.velocity_y < 0:
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
        self.is_jumping = not self.on_ground
        self.animation_tick += 1

    def draw(self, screen):
        if self.invulnerability_timer and (self.invulnerability_timer // 5) % 2:
            return
        body = (255, 213, 92) if self.star_timer else (233, 89, 73)
        # Compact adventurer sprite: cap, tunic, boots, and eyes are drawn without external assets.
        pygame.draw.rect(screen, (73, 54, 100), (self.rect.x + 3, self.rect.y + 2, 24, 10), border_radius=5)
        pygame.draw.rect(screen, body, (self.rect.x + 2, self.rect.y + 10, 26, 23), border_radius=6)
        pygame.draw.rect(screen, (61, 71, 112), (self.rect.x + 4, self.rect.y + 30, 9, 12), border_radius=3)
        pygame.draw.rect(screen, (61, 71, 112), (self.rect.x + 17, self.rect.y + 30, 9, 12), border_radius=3)
        eye_x = self.rect.centerx + self.facing * 5
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, self.rect.y + 17), 4)
        pygame.draw.circle(screen, (35, 40, 54), (eye_x + self.facing, self.rect.y + 17), 2)
        if self.star_timer:
            pygame.draw.circle(screen, (255, 244, 115), self.rect.center, 27, 2)

    def set_start_position(self, x, y):
        self.start_x, self.start_y = x, y

    def reset_position(self):
        self.rect.topleft = (self.start_x, self.start_y)
        self.velocity_x = self.velocity_y = 0
        self.on_ground = False
        self.is_jumping = True
        self.coyote_timer = self.jump_buffer = 0
        self.dash_timer = 0

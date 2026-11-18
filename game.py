import pygame
from player import Player
from level import Level
from ui import UI


class Game:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mosslight: The Lost Garden")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.current_level = 1
        self.total_levels = 3
        self.level = Level(self.current_level, self.screen_width, self.screen_height)
        self.player = Player(70, 450)
        self.ui = UI()
        self.game_over = False
        self.game_won = False
        self.elapsed = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self.player.jump()
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.player.dash()
                elif event.key == pygame.K_r:
                    if self.game_over or self.game_won:
                        self.restart_game()
                    else:
                        self.reset_level()
                elif event.key == pygame.K_n and self.game_won:
                    self.restart_game()
        keys = pygame.key.get_pressed()
        self.player.set_horizontal_input(
            int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) -
            int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        )
        return True

    def update(self):
        if self.game_over or self.game_won:
            return
        self.elapsed += 1
        self.player.update(self.level.platforms, self.screen_width, self.screen_height)

        for collectible in self.level.collectibles[:]:
            if self.player.rect.colliderect(collectible.rect):
                self.player.collect(collectible)
                self.level.collectibles.remove(collectible)

        for enemy in self.level.enemies[:]:
            enemy.update(self.level.platforms, self.screen_width)
            if not self.player.rect.colliderect(enemy.rect) or self.player.invulnerable:
                continue
            # A stomp is detected from the previous frame's feet, not the enemy's x-coordinate.
            if self.player.velocity_y > 0 and self.player.previous_bottom <= enemy.rect.top + 12:
                self.level.enemies.remove(enemy)
                self.player.score += 100
                self.player.velocity_y = -10
                self.player.is_jumping = True
            else:
                self.lose_life()
                break

        if self.player.rect.top > self.screen_height:
            self.lose_life()

        if self.player.rect.colliderect(self.level.end_flag.rect):
            if self.current_level >= self.total_levels:
                self.game_won = True
            else:
                self.next_level()

    def lose_life(self):
        if self.player.invulnerable or self.game_over:
            return
        self.player.lives -= 1
        if self.player.lives <= 0:
            self.player.lives = 0
            self.game_over = True
        else:
            self.player.reset_position()
            self.player.invulnerability_timer = 100

    def render(self):
        self.draw_background()
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        self.ui.draw(self.screen, self.player.score, self.player.lives,
                     self.current_level, self.player.coins)
        if self.game_over:
            self.ui.draw_game_over(self.screen)
        elif self.game_won:
            self.ui.draw_game_won(self.screen, self.player.score)
        pygame.display.flip()

    def draw_background(self):
        self.screen.fill((129, 199, 224))
        # Layered hills and drifting clouds make each level feel less like a blank box.
        pygame.draw.circle(self.screen, (245, 220, 128), (1030, 100), 42)
        shift = (self.elapsed // 3) % 1500
        for x, y, radius in ((180, 95, 24), (560, 145, 18), (850, 75, 28)):
            cloud_x = (x - shift) % 1450 - 100
            pygame.draw.circle(self.screen, (235, 248, 239), (cloud_x, y), radius)
            pygame.draw.circle(self.screen, (235, 248, 239), (cloud_x + radius, y + 7), radius - 4)
        pygame.draw.ellipse(self.screen, (112, 190, 145), (-120, 375, 700, 250))
        pygame.draw.ellipse(self.screen, (91, 171, 130), (420, 400, 900, 240))

    def reset_level(self):
        self.player.reset_position()
        self.level = Level(self.current_level, self.screen_width, self.screen_height)

    def next_level(self):
        self.current_level += 1
        if self.current_level > self.total_levels:
            self.game_won = True
            return
        self.level = Level(self.current_level, self.screen_width, self.screen_height)
        self.player.set_start_position(70, 450)
        self.player.reset_position()

    def restart_game(self):
        self.current_level = 1
        self.game_over = False
        self.game_won = False
        self.player.score = 0
        self.player.coins = 0
        self.player.lives = 3
        self.player.set_start_position(70, 450)
        self.level = Level(self.current_level, self.screen_width, self.screen_height)
        self.player.reset_position()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

import pygame


class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 56)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def draw(self, screen, score, lives, level, coins=0):
        pygame.draw.rect(screen, (248, 246, 229), (12, 12, 330, 40), border_radius=12)
        text = self.font_small.render(f"SCORE {score:05d}   ♥ {lives}   ◆ {coins}   GROVE {level}/3", True, (49, 56, 70))
        screen.blit(text, (24, 22))
        controls = self.font_small.render("Move: A/D or ←/→   Jump: Space/W/↑   Dash: Shift   Restart: R", True, (38, 55, 62))
        screen.blit(controls, (355, 22))

    def _overlay(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((20, 28, 43, 190))
        screen.blit(overlay, (0, 0))

    def draw_game_over(self, screen):
        self._overlay(screen)
        title = self.font_large.render("THE GARDEN GOES QUIET", True, (255, 151, 132))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 35)))
        hint = self.font_medium.render("Press R to begin a fresh adventure", True, (255, 255, 255))
        screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 28)))

    def draw_game_won(self, screen, score):
        self._overlay(screen)
        title = self.font_large.render("THE GROVE IS RESTORED!", True, (255, 237, 135))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 65)))
        result = self.font_medium.render(f"Final score: {score}", True, (255, 255, 255))
        screen.blit(result, result.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))
        hint = self.font_small.render("Press R or N to play again", True, (220, 235, 232))
        screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 55)))

import pygame
from game_platform import Platform
from enemy import Enemy
from collectible import Collectible
from flag import Flag


class Level:
    def __init__(self, level_num, screen_width, screen_height):
        self.level_num = level_num
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.platforms = []
        self.enemies = []
        self.collectibles = []
        self.end_flag = None
        self.create_level()

    def add_platform(self, x, y, width, color=(133, 91, 62)):
        self.platforms.append(Platform(x, y, width, 18, color))

    def create_level(self):
        ground = Platform(0, 550, self.screen_width, 50, (71, 145, 83))
        self.platforms.append(ground)
        if self.level_num == 1:
            self.create_level_1()
        elif self.level_num == 2:
            self.create_level_2()
        else:
            self.create_level_3()
        self.end_flag = Flag(1125, 490)

    def create_level_1(self):
        # The stepping stones stay within a comfortable jump range and lead to the first secret.
        for x, y, width in ((190, 470, 145), (410, 410, 145), (640, 350, 145), (865, 410, 130)):
            self.add_platform(x, y, width)
        self.enemies.extend((Enemy(280, 522, 220, 390), Enemy(460, 382, 420, 535),
                             Enemy(700, 322, 650, 770, "hopper")))
        self.collectibles.extend((Collectible(235, 440, 10), Collectible(455, 380, 10),
                                  Collectible(685, 320, 10), Collectible(910, 380, 10),
                                  Collectible(1040, 510, 10), Collectible(590, 510, 25, "heart")))

    def create_level_2(self):
        self.add_platform(100, 475, 125)
        self.add_platform(285, 420, 115)
        self.add_platform(470, 365, 115)
        self.add_platform(665, 310, 115)
        self.add_platform(855, 365, 125)
        self.add_platform(1010, 455, 100)
        self.enemies.extend((Enemy(145, 447, 100, 225, speed=2),
                             Enemy(490, 337, 470, 585, "hopper", 1.8),
                             Enemy(880, 337, 855, 980, speed=2.2)))
        for x, y in ((145, 445), (330, 390), (515, 335), (710, 280), (900, 335), (1050, 425)):
            self.collectibles.append(Collectible(x, y, 15))
        self.collectibles.append(Collectible(570, 500, 35, "star"))

    def create_level_3(self):
        # A rising route, a safe lower route, and a final gap make dash useful but not mandatory.
        for x, y, width in ((115, 480, 105), (285, 425, 100), (445, 370, 100),
                            (605, 315, 100), (765, 370, 100), (925, 425, 105), (1060, 480, 85)):
            self.add_platform(x, y, width, (115, 79, 105))
        self.enemies.extend((Enemy(145, 452, 115, 220, "hopper", 2.0),
                             Enemy(470, 342, 445, 545, speed=2.4),
                             Enemy(790, 342, 765, 865, "hopper", 2.2),
                             Enemy(950, 397, 925, 1030, speed=2.5)))
        for x, y in ((145, 450), (315, 395), (475, 340), (635, 285), (795, 340), (955, 395)):
            self.collectibles.append(Collectible(x, y, 20))
        self.collectibles.extend((Collectible(550, 510, 50, "star"), Collectible(1080, 450, 25, "heart")))

    def draw(self, screen):
        for platform in self.platforms:
            platform.draw(screen)
        for collectible in self.collectibles:
            collectible.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        self.end_flag.draw(screen)

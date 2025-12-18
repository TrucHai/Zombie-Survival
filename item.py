import pygame
from settings import *

class HealthPack(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(
            "assets/health.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (28, 28))
        self.rect = self.image.get_rect(center=pos)

        self.heal_amount = 25   # 💊 HỒI BAO NHIÊU MÁU

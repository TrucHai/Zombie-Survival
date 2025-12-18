import pygame
import random
import math
from settings import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self, level, player):
        super().__init__()

        # Load ảnh gốc (chưa xoay)
        self.original_image = pygame.image.load(
            "assets/zombie.png"
        ).convert_alpha()
        self.original_image = pygame.transform.scale(
            self.original_image, (38, 38)
        )

        self.image = self.original_image
        self.rect = self.image.get_rect()

        # Spawn ngoài màn hình
        edge = random.choice(['top','bottom','left','right'])
        if edge == 'top':
            self.rect.center = (random.randint(0, WIDTH), -30)
        elif edge == 'bottom':
            self.rect.center = (random.randint(0, WIDTH), HEIGHT + 30)
        elif edge == 'left':
            self.rect.center = (-30, random.randint(0, HEIGHT))
        else:
            self.rect.center = (WIDTH + 30, random.randint(0, HEIGHT))

        self.pos = pygame.Vector2(self.rect.center)

        self.speed = ZOMBIE_SPEED_BASE + level * 0.05
        self.hp = 30 + level * 5
        self.player = player

    def update(self):
        # Vector hướng tới player
        direction = self.player.pos - self.pos

        if direction.length_squared() > 0:
            direction = direction.normalize()

            # Di chuyển
            self.pos += direction * self.speed

            # 🔄 TÍNH GÓC XOAY
            angle = math.degrees(math.atan2(-direction.y, direction.x))

            # Xoay ảnh
            self.image = pygame.transform.rotate(
                self.original_image, angle
            )

            # Giữ đúng tâm sau khi xoay
            self.rect = self.image.get_rect(center=self.pos)

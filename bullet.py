import pygame
import math
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()

        self.original_image = pygame.image.load(
            "assets/bullet.png"
        ).convert_alpha()
        self.original_image = pygame.transform.scale(
            self.original_image, (16, 16)
        )

        angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
        self.image = pygame.transform.rotate(self.original_image, angle) 
    
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.vel = direction * BULLET_SPEED

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if (self.pos.x < -20 or self.pos.x > WIDTH+20 or
            self.pos.y < -20 or self.pos.y > HEIGHT+20):
            self.kill()

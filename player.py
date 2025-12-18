import pygame
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(
            "assets/player.png"
        ).convert_alpha()
        self.original_image = pygame.transform.scale(
            self.original_image, (40, 40)
        )
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.pos = pygame.Vector2(self.rect.center)

        self.hp = MAX_HP
        self.xp = 0

        # 🔫 VŨ KHÍ
        self.weapon_level = 1
        self.base_damage = 20

        self.last_shot = 0
        self.shoot_delay = 180


    def update(self):
        keys = pygame.key.get_pressed()
        vel = pygame.Vector2(0, 0)
        if keys[pygame.K_w]: vel.y -= PLAYER_SPEED
        if keys[pygame.K_s]: vel.y += PLAYER_SPEED
        if keys[pygame.K_a]: vel.x -= PLAYER_SPEED
        if keys[pygame.K_d]: vel.x += PLAYER_SPEED
        if vel.length_squared() > 0:
            vel = vel.normalize() * PLAYER_SPEED
        self.pos += vel
        self.pos.x = max(18, min(WIDTH-18, self.pos.x))
        self.pos.y = max(18, min(HEIGHT-18, self.pos.y))
        self.rect.center = self.pos
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_pos) - self.pos

        if direction.length_squared() > 0:
            angle = math.degrees(math.atan2(-direction.y, direction.x))-90
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.pos)


    def shoot(self, target, bullets, all_sprites, Bullet):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            self.last_shot = now
            direction = pygame.Vector2(target) - self.pos
            if direction.length_squared() == 0:
                direction = pygame.Vector2(1,0)
            direction = direction.normalize()
            bullet = Bullet(self.pos, direction)
            bullets.add(bullet)
            all_sprites.add(bullet)


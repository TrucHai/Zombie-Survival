import pygame
import random
from settings import *
from player import Player
from zombie import Zombie
from bullet import Bullet
from item import HealthPack
from ui import draw_ui
from utils import load_highscore, save_highscore

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")
clock = pygame.time.Clock()

# ================== GAME STATE ==================
# START | PLAY | SHOP | GAMEOVER
game_state = "START"

# ================== HIGHSCORE ==================
highscore = load_highscore()

# ================== GROUPS ==================
all_sprites = pygame.sprite.Group()
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
items = pygame.sprite.Group()

# ================== PLAYER ==================
player = Player()
all_sprites.add(player)

# ================== GAME VAR ==================
score = 0
level = 1
spawn_timer = pygame.time.get_ticks()
current_weapon = "PISTOL"

# ================== FUNCTIONS ==================
def reset_game():
    global all_sprites, zombies, bullets, items
    global player, score, level, spawn_timer, current_weapon

    all_sprites.empty()
    zombies.empty()
    bullets.empty()
    items.empty()

    player.hp = MAX_HP
    player.xp = 0
    player.weapon_level = 1
    player.base_damage = 20
    player.shoot_delay = 180
    player.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    player.rect.center = player.pos

    all_sprites.add(player)

    score = 0
    level = 1
    spawn_timer = pygame.time.get_ticks()
    current_weapon = "PISTOL"

def get_spawn_settings(level):
    spawn_delay = max(900, SPAWN_DELAY - level * 30)
    zombie_count = min(1 + level // 3, 3)
    return spawn_delay, zombie_count

# ================== MAIN LOOP ==================
running = True
while running:
    clock.tick(FPS)

    # ================== EVENTS ==================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ----- START / RESTART -----
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "START":
                reset_game()
                game_state = "PLAY"
            elif game_state == "GAMEOVER":
                reset_game()
                game_state = "PLAY"

        # ----- SHOOT -----
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAY":
            if event.button == 1:
                player.shoot(
                    pygame.mouse.get_pos(),
                    bullets,
                    all_sprites,
                    Bullet
                )

        # ----- SHOP CONTROL -----
        if event.type == pygame.KEYDOWN:
            # Mở shop
            if event.key == pygame.K_b and game_state == "PLAY":
                game_state = "SHOP"

            # Thoát shop
            if event.key == pygame.K_ESCAPE and game_state == "SHOP":
                game_state = "PLAY"

            # Mua / nâng cấp vũ khí
            if game_state == "SHOP":
                # Nâng cấp súng hiện tại
                if event.key == pygame.K_1:
                    cost = 50 * player.weapon_level
                    if score >= cost:
                        score -= cost
                        player.weapon_level += 1
                        player.shoot_delay = max(80, player.shoot_delay - 15)
                # Mua Rifle
                if event.key == pygame.K_2 and current_weapon != "RIFLE":
                    if score >= 200:
                        score -= 200
                        current_weapon = "RIFLE"
                        player.base_damage = 30
                        player.weapon_level = 1
                        player.shoot_delay = 120
                # Mua Shotgun
                if event.key == pygame.K_3 and current_weapon != "SHOTGUN":
                    if score >= 350:
                        score -= 350
                        current_weapon = "SHOTGUN"
                        player.base_damage = 50
                        player.weapon_level = 1
                        player.shoot_delay = 220

    # ================== GAME LOGIC ==================
    if game_state == "PLAY":
        # ----- SPAWN ZOMBIE -----
        spawn_delay, zombie_count = get_spawn_settings(level)
        now = pygame.time.get_ticks()
        if now - spawn_timer > spawn_delay:
            spawn_timer = now
            for _ in range(zombie_count):
                z = Zombie(level, player)
                z.speed += level * 0.3  # Quái chạy nhanh theo level
                zombies.add(z)
                all_sprites.add(z)

        # ----- UPDATE SPRITES -----
        all_sprites.update()

        # ----- ITEM 10s -----
        for item in items:
            if now - item.spawn_time > 10000:
                item.kill()

        # ----- BULLET HIT -----
        hits = pygame.sprite.groupcollide(zombies, bullets, False, True)
        for z, bs in hits.items():
            damage = player.base_damage * player.weapon_level
            z.hp -= damage
            if z.hp <= 0:
                z.kill()
                score += 10
                player.xp += XP_PER_KILL

                if random.random() < 0.25:
                    item = HealthPack(z.pos)
                    item.spawn_time = pygame.time.get_ticks()
                    items.add(item)
                    all_sprites.add(item)

                if player.xp >= XP_TO_LEVEL:
                    player.xp = 0
                    level += 1

        # ----- PICK ITEM -----
        pickups = pygame.sprite.spritecollide(player, items, True)
        for item in pickups:
            player.hp = min(MAX_HP, player.hp + item.heal_amount)

        # ----- PLAYER HIT -----
        if pygame.sprite.spritecollide(player, zombies, True):
            player.hp -= 10
            if player.hp <= 0:
                game_state = "GAMEOVER"
                if score > highscore:
                    save_highscore(score)
                    highscore = score

    # ================== DRAW ==================
    screen.fill((20, 20, 20))

    if game_state == "START":
        font = pygame.font.Font(None, 64)
        small = pygame.font.Font(None, 36)
        screen.blit(font.render("ZOMBIE SURVIVAL", True, (0, 200, 0)),
                    (WIDTH//2 - 200, HEIGHT//2 - 100))
        screen.blit(small.render("Click chuot de bat dau", True, (255,255,255)),
                    (WIDTH//2 - 160, HEIGHT//2))

    elif game_state == "PLAY":
        all_sprites.draw(screen)
        draw_ui(screen, player, score, level, highscore)

    elif game_state == "SHOP":
        font = pygame.font.Font(None, 48)
        small = pygame.font.Font(None, 32)
        title = font.render("SHOP VU KHI", True, (255,255,0))
        screen.blit(title, (WIDTH//2 - 140, HEIGHT//2 - 120))

        buy1 = small.render(f"1: Nang cap vu khi (Gia: {50*player.weapon_level})", True, (255,255,255))
        buy2 = small.render("2: Mua Rifle (200)", True, (255,255,255))
        buy3 = small.render("3: Mua Shotgun (350)", True, (255,255,255))
        back = small.render("ESC: Quay lai game", True, (200,200,200))

        screen.blit(buy1, (WIDTH//2 - 260, HEIGHT//2 - 40))
        screen.blit(buy2, (WIDTH//2 - 260, HEIGHT//2))
        screen.blit(buy3, (WIDTH//2 - 260, HEIGHT//2 + 40))
        screen.blit(back, (WIDTH//2 - 160, HEIGHT//2 + 80))

    elif game_state == "GAMEOVER":
        all_sprites.draw(screen)
        draw_ui(screen, player, score, level, highscore)
        font = pygame.font.Font(None, 48)
        small = pygame.font.Font(None, 32)
        screen.blit(font.render("GAME OVER", True, (255,0,0)),
                    (WIDTH//2 - 120, HEIGHT//2 - 60))
        screen.blit(small.render("Click chuot de choi lai", True, (255,255,255)),
                    (WIDTH//2 - 150, HEIGHT//2))

    pygame.display.flip()

pygame.quit()

import pygame
import random
from settings import *
from player import Player
from zombie import Zombie
from bullet import Bullet
from item import HealthPack
from ui import draw_ui
from utils import load_highscore, save_highscore, load_gold, save_gold

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")
clock = pygame.time.Clock()

# ================== GAME STATE ==================
game_state = "START"

# ================== LOAD ==================
highscore = load_highscore()
gold = load_gold()

# ================== RESET GAME ==================
def reset_game():
    global all_sprites, zombies, bullets, items
    global player, score, level, spawn_timer

    all_sprites = pygame.sprite.Group()
    zombies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    items = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    score = 0
    level = 1
    spawn_timer = pygame.time.get_ticks()

# ================== SPAWN SETTINGS ==================
def get_spawn_settings(level):
    spawn_delay = max(300, SPAWN_DELAY - level * 80)
    zombie_count = min(1 + level // 2, 6)
    return spawn_delay, zombie_count

# ================== INIT ==================
reset_game()

running = True
while running:
    clock.tick(FPS)
    now = pygame.time.get_ticks()

    # ================== EVENTS ==================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # START / RESTART
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "START":
                game_state = "PLAY"
            elif game_state == "GAMEOVER":
                reset_game()
                game_state = "PLAY"

        # SHOOT
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAY":
            if event.button == 1:
                player.shoot(pygame.mouse.get_pos(), bullets, all_sprites, Bullet)

    # ================== INPUT LIÊN TỤC ==================
    keys = pygame.key.get_pressed()
    if game_state == "PLAY":
        if keys[pygame.K_b]:
            game_state = "SHOP"
    elif game_state == "SHOP":
        if keys[pygame.K_ESCAPE]:
            game_state = "PLAY"
        # Shop nâng cấp vũ khí bằng gold
        if keys[pygame.K_1]:
            cost = 50 * player.weapon_level
            if gold >= cost:
                gold -= cost
                save_gold(gold)
                player.weapon_level += 1
                player.shoot_delay = max(80, player.shoot_delay - 20)

    # ================== GAME LOGIC ==================
    if game_state == "PLAY":
        # SPAWN ZOMBIE
        spawn_delay, zombie_count = get_spawn_settings(level)
        if now - spawn_timer > spawn_delay:
            spawn_timer = now
            for _ in range(zombie_count):
                z = Zombie(level, player)
                zombies.add(z)
                all_sprites.add(z)

        # UPDATE SPRITES
        all_sprites.update()

        # ITEM 10s
        for item in items:
            if now - item.spawn_time > 10000:
                item.kill()

        # BULLET HIT
        hits = pygame.sprite.groupcollide(zombies, bullets, False, True)
        for z in hits:
            damage = player.base_damage * player.weapon_level
            z.hp -= damage

            if z.hp <= 0:
                z.kill()
                score += 10
                gold += random.randint(5,15)
                save_gold(gold)
                player.xp += XP_PER_KILL

                if random.random() < 0.25:
                    item = HealthPack(z.pos)
                    item.spawn_time = pygame.time.get_ticks()
                    items.add(item)
                    all_sprites.add(item)

                if player.xp >= XP_TO_LEVEL:
                    player.xp = 0
                    level += 1

        # PICK ITEM
        pickups = pygame.sprite.spritecollide(player, items, True)
        for item in pickups:
            player.hp = min(MAX_HP, player.hp + item.heal_amount)

        # PLAYER HIT
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
        screen.blit(font.render("ZOMBIE SURVIVAL", True, (0, 200, 0)), (WIDTH//2 - 200, HEIGHT//2 - 100))
        screen.blit(small.render("Click chuot de bat dau", True, (255, 255, 255)), (WIDTH//2 - 160, HEIGHT//2))

    elif game_state == "PLAY":
        all_sprites.draw(screen)
        draw_ui(screen, player, score, level, highscore, gold)

    elif game_state == "SHOP":
        font = pygame.font.Font(None, 48)
        small = pygame.font.Font(None, 32)
        title = font.render("SHOP VU KHI", True, (255, 255, 0))
        buy = small.render(f"Nhan 1: Nang cap vu khi (Gia: {50*player.weapon_level})", True, (255,255,255))
        back = small.render("ESC: Quay lai game", True, (200,200,200))
        gold_display = small.render(f"Gold: {gold}", True, (255, 215, 0))

        screen.blit(title, (WIDTH//2 - 140, HEIGHT//2 - 120))
        screen.blit(buy, (WIDTH//2 - 260, HEIGHT//2 - 40))
        screen.blit(back, (WIDTH//2 - 160, HEIGHT//2 + 20))
        screen.blit(gold_display, (WIDTH//2 + 100, HEIGHT//2 - 100))

    elif game_state == "GAMEOVER":
        all_sprites.draw(screen)
        draw_ui(screen, player, score, level, highscore, gold)
        font = pygame.font.Font(None, 48)
        small = pygame.font.Font(None, 32)
        screen.blit(font.render("GAME OVER", True, (255,0,0)), (WIDTH//2 - 120, HEIGHT//2 - 60))
        screen.blit(small.render("Click chuot de choi lai", True, (255,255,255)), (WIDTH//2 - 150, HEIGHT//2))

    pygame.display.flip()

pygame.quit()


import pygame
from settings import *

def draw_ui(screen, player, score, level, highscore):
    font = pygame.font.Font(None, 22)

    pygame.draw.rect(screen, (80,80,80), (20,20,200,18))
    pygame.draw.rect(screen, (220,60,60), (20,20,200*player.hp/MAX_HP,18))

    pygame.draw.rect(screen, (80,80,80), (20,44,200,14))
    pygame.draw.rect(screen, (80,180,255), (20,44,200*player.xp/XP_TO_LEVEL,14))

    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (20,70))
    screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (20,95))
    screen.blit(font.render(f"High Score: {highscore}", True, (255,255,255)), (WIDTH-220,20))

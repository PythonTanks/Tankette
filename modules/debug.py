import pygame

pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, screen, x = 10, y = 10):
    text = font.render(info, True, (255, 255, 255))
    screen.blit(text, (x, y))
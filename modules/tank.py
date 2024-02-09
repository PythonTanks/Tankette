import pygame
import time
from modules.movable import Movable
from modules.bullet import Bullet

class Tank(Movable):
    def __init__(self, game, image_path="assets/tank.png", initial_position=(0, 0), dimensions=(80, 100), velocity=10):
        # Appel du constructeur de la classe parente (Movable)
        super().__init__(game, image_path, initial_position, dimensions, velocity)
        # Référence à l'instance de la classe Game
        self.game = game
        # Groupe de projectiles tirés par le tank
        self.all_projectiles = pygame.sprite.Group()
        # Temps du dernier tir
        self.last_shot = 0
        
        self.rotation = "haut"

    def launch_projectile(self, angle, start):
        # Vérifie si le temps écoulé depuis le dernier tir est supérieur à 0.5 seconde
        now = time.time()
        if now - self.last_shot < 0.5:
            return
        # Met à jour le temps du dernier tir
        self.last_shot = now
        # Ajoute un nouveau projectile au groupe de projectiles
        self.all_projectiles.add(Bullet(self.game, angle=angle, start=start))

    def handle_input(self):
        # Récupère l'état des touches du clavier
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        moving = True

        # Si la touche 'd' est pressée, le tank se déplace vers la droite
        if self.game.diagonales:
            if keys[pygame.K_d] and keys[pygame.K_z]:
                self.image = pygame.transform.rotate(self.image, -45)
                dx += self.velocity
                dy -= self.velocity
                self.move(dx, dy, self.image_up_right)
                self.rotation = "haut droit"
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                self.image = pygame.transform.rotate(self.image, -135)
                dx += self.velocity
                dy += self.velocity
                self.move(dx, dy, self.image_down_right)
                self.rotation = "bas droit"
            elif keys[pygame.K_q] and keys[pygame.K_z]:
                self.image = pygame.transform.rotate(self.image, 45)
                dx -= self.velocity
                dy -= self.velocity
                self.move(dx, dy, self.image_up_left)
                self.rotation = "haut gauche"
            elif keys[pygame.K_q] and keys[pygame.K_s]:
                self.image = pygame.transform.rotate(self.image, 135)
                dx -= self.velocity
                dy += self.velocity
                self.move(dx, dy, self.image_down_left)
                self.rotation = "bas gauche"
            elif keys[pygame.K_d]:
                self.image = pygame.transform.rotate(self.image, -90)
                dx += self.velocity
                self.move(dx, dy, self.image_right)
                self.rotation = "droite"
            elif keys[pygame.K_q]:
                self.image = pygame.transform.rotate(self.image, 90)
                dx -= self.velocity
                self.move(dx, dy, self.image_left)
                self.rotation = "gauche"
            elif keys[pygame.K_z]:
                self.image = pygame.transform.rotate(self.image, 0)
                dy -= self.velocity
                self.move(dx, dy, self.image_up)
                self.rotation = "haut"
            elif keys[pygame.K_s]:
                self.image = pygame.transform.rotate(self.image, 180)
                dy += self.velocity
                self.move(dx, dy, self.image_down)
                self.rotation = "bas"
        else:
            if keys[pygame.K_d]:
                self.image = pygame.transform.rotate(self.image, -90)
                dx += self.velocity
                self.move(dx, dy, self.image_right)
                self.rotation = "droite"
            elif keys[pygame.K_q]:
                self.image = pygame.transform.rotate(self.image, 90)
                dx -= self.velocity
                self.move(dx, dy, self.image_left)
                self.rotation = "gauche"
            elif keys[pygame.K_z]:
                self.image = pygame.transform.rotate(self.image, 0)
                dy -= self.velocity
                self.move(dx, dy, self.image_up)
                self.rotation = "haut"
            elif keys[pygame.K_s]:
                self.image = pygame.transform.rotate(self.image, 180)
                dy += self.velocity
                self.move(dx, dy, self.image_down)
                self.rotation = "bas"

        # Si la touche 'espace' est pressée, le tank tire un projectile
        if keys[pygame.K_SPACE]:
            self.launch_projectile(self.game.toptank.get_angle(), self.game.toptank.get_position_bout_canon())
        
        if keys[pygame.K_KP0]:
            self.game.freeze = not self.game.freeze
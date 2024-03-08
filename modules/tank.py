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
        # Récupère l'état actuel des touches du clavier
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        # Si le jeu autorise les mouvements en diagonale
        if self.game.diagonales:
            
            # Si les touches 'd' et 'z' sont pressées simultanément
            if keys[pygame.K_d] and keys[pygame.K_z]:
                # Rotation de l'image du tank de -45 degrés
                self.image = pygame.transform.rotate(self.image, -45)
                # Déplacement du tank vers le haut et la droite
                dx += self.velocity
                dy -= self.velocity
                self.move(dx, dy, self.image_up_right)
                self.rotation = "haut_droit"
                
            # Si les touches 'd' et 's' sont pressées simultanément
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                # Rotation de l'image du tank de -135 degrés
                self.image = pygame.transform.rotate(self.image, -135)
                # Déplacement du tank vers le bas et la droite
                dx += self.velocity
                dy += self.velocity
                self.move(dx, dy, self.image_down_right)
                self.rotation = "bas_droit"
            
            # Si les touches 'q' et 'z' sont pressées simultanément
            elif keys[pygame.K_q] and keys[pygame.K_z]:
                # Rotation de l'image du tank de 45 degrés
                self.image = pygame.transform.rotate(self.image, 45)
                # Déplacement du tank vers le haut et la gauche
                dx -= self.velocity
                dy -= self.velocity
                self.move(dx, dy, self.image_up_left)
                self.rotation = "haut_gauche"
            
            # Si les touches 'q' et 's' sont pressées simultanément
            elif keys[pygame.K_q] and keys[pygame.K_s]:
                # Rotation de l'image du tank de 135 degrés
                self.image = pygame.transform.rotate(self.image, 135)
                # Déplacement du tank vers le bas et la gauche
                dx -= self.velocity
                dy += self.velocity
                self.move(dx, dy, self.image_down_left)
                self.rotation = "bas_gauche"
                
            # Si la touche 'd' est pressée
            elif keys[pygame.K_d]:
                # Rotation de l'image du tank de -90 degrés
                self.image = pygame.transform.rotate(self.image, -90)
                # Déplacement du tank vers la droite
                dx += self.velocity
                self.move(dx, dy, self.image_right)
                self.rotation = "droite"
            
            # Si la touche 'q' est pressée
            elif keys[pygame.K_q]:
                # Rotation de l'image du tank de 90 degrés
                self.image = pygame.transform.rotate(self.image, 90)
                # Déplacement du tank vers la gauche
                dx -= self.velocity
                self.move(dx, dy, self.image_left)
                self.rotation = "gauche"
                
            # Si la touche 'z' est pressée
            elif keys[pygame.K_z]:
                # Rotation de l'image du tank de 0 degrés
                self.image = pygame.transform.rotate(self.image, 0)
                # Déplacement du tank vers le haut
                dy -= self.velocity
                self.move(dx, dy, self.image_up)
                self.rotation = "haut"
                
            # Si la touche 's' est pressée
            elif keys[pygame.K_s]:
                # Rotation de l'image du tank de 180 degrés
                self.image = pygame.transform.rotate(self.image, 180)
                # Déplacement du tank vers le bas
                dy += self.velocity
                self.move(dx, dy, self.image_down)
                self.rotation = "bas"
        
        # Si le jeu n'autorise pas les mouvements en diagonale
        else:
            
            # Si la touche 'd' est pressée
            if keys[pygame.K_d]:
                # Rotation de l'image du tank de -90 degrés
                self.image = pygame.transform.rotate(self.image, -90)
                # Déplacement du tank vers la droite
                dx += self.velocity
                self.move(dx, dy, self.image_right)
                self.rotation = "droite"
            
            # Si la touche 'q' est pressée
            elif keys[pygame.K_q]:
                # Rotation de l'image du tank de 90 degrés
                self.image = pygame.transform.rotate(self.image, 90)
                # Déplacement du tank vers la gauche
                dx -= self.velocity
                self.move(dx, dy, self.image_left)
                self.rotation = "gauche"
                
            # Si la touche 'z' est pressée
            elif keys[pygame.K_z]:
                # Rotation de l'image du tank de 0 degrés
                self.image = pygame.transform.rotate(self.image, 0)
                # Déplacement du tank vers le haut
                dy -= self.velocity
                self.move(dx, dy, self.image_up)
                self.rotation = "haut"
                
            # Si la touche 's' est pressée
            elif keys[pygame.K_s]:
                # Rotation de l'image du tank de 180 degrés
                self.image = pygame.transform.rotate(self.image, 180)
                # Déplacement du tank vers le bas
                dy += self.velocity
                self.move(dx, dy, self.image_down)
                self.rotation = "bas"

        # Si la touche 'espace' est pressée
        if keys[pygame.K_SPACE]:
            # Appel de la méthode pour lancer un projectile
            self.launch_projectile(self.game.toptank.get_angle(), self.game.toptank.get_position_bout_canon())
        
        # Si la touche '0' du pavé numérique est pressée
        if keys[pygame.K_KP0]:
            # Inversion du mode de pause du jeu
            self.game.freeze = not self.game.freeze
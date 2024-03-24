import pygame  # Bibliothèque pour le développement de jeux vidéo
import time  # Fournit des fonctions pour manipuler le temps
from modules.movable import Movable  # Importe la classe Movable du module movable
from modules.bullet import Bullet  # Importe la classe Bullet du module bullet

# Classe représentant un tank
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
        # Rotation initiale du tank
        self.rotation = "haut"

    # Méthode pour lancer un projectile
    def launch_projectile(self, angle, start):
        # Vérifie si le temps écoulé depuis le dernier tir est supérieur à 0.5 seconde
        now = time.time()
        if now - self.last_shot < 0.5:
            return
        # Met à jour le temps du dernier tir
        self.last_shot = now
        # Ajoute un nouveau projectile au groupe de projectiles
        self.all_projectiles.add(Bullet(self.game, angle=angle, start=start))

    # Méthode pour gérer les entrées de l'utilisateur
    def handle_input(self):
        # Récupère l'état actuel des touches du clavier
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # Si le jeu autorise les mouvements en diagonale
        if self.game.diagonales:
            # Gestion des mouvements en diagonale
            if keys[pygame.K_d] and keys[pygame.K_z]:
                # Rotation et déplacement du tank vers le haut et la droite
                self.image = pygame.transform.rotate(self.image, -45)
                dx += self.velocity
                dy -= self.velocity
                self.move(dx, dy, self.image_up_right)
                self.rotation = "haut_droit"
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                # Rotation et déplacement du tank vers le bas et la droite
                self.image = pygame.transform.rotate(self.image, -135)
                dx += self.velocity
                dy += self.velocity
                self.move(dx, dy, self.image_down_right)
                self.rotation = "bas_droit"
            elif keys[pygame.K_q] and keys[pygame.K_z]:
                # Rotation et déplacement du tank vers le haut et la gauche
                self.image = pygame.transform.rotate(self.image, 45)
                dx -= self.velocity
                dy -= self.velocity
                self.move(dx, dy, self.image_up_left)
                self.rotation = "haut_gauche"
            elif keys[pygame.K_q] and keys[pygame.K_s]:
                # Rotation et déplacement du tank vers le bas et la gauche
                self.image = pygame.transform.rotate(self.image, 135)
                dx -= self.velocity
                dy += self.velocity
                self.move(dx, dy, self.image_down_left)
                self.rotation = "bas_gauche"
        else:
            # Gestion des mouvements sans diagonale
            if keys[pygame.K_d]:
                # Rotation et déplacement du tank vers la droite
                self.image = pygame.transform.rotate(self.image, -90)
                dx += self.velocity
                self.move(dx, dy, self.image_right)
                self.rotation = "droite"
            elif keys[pygame.K_q]:
                # Rotation et déplacement du tank vers la gauche
                self.image = pygame.transform.rotate(self.image, 90)
                dx -= self.velocity
                self.move(dx, dy, self.image_left)
                self.rotation = "gauche"
            elif keys[pygame.K_z]:
                # Rotation et déplacement du tank vers le haut
                self.image = pygame.transform.rotate(self.image, 0)
                dy -= self.velocity
                self.move(dx, dy, self.image_up)
                self.rotation = "haut"
            elif keys[pygame.K_s]:
                # Rotation et déplacement du tank vers le bas
                self.image = pygame.transform.rotate(self.image, 180)
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
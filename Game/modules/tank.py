import pygame  # Bibliothèque pour le développement de jeux vidéo
import time  # Fournit des fonctions pour manipuler le temps
from modules.movable import Movable  # Importe la classe Movable du module movable
from modules.bullet import Bullet  # Importe la classe Bullet du module bullet

# Classe représentant un tank
class Tank(Movable):
    def __init__(self, game, image_path="assets/tank.png", initial_position=(0, 0), dimensions=(80/1080, 106/1920), velocity=5, rotation="haut"):
        # Appel du constructeur de la classe parente (Movable)
        super().__init__(game, image_path, initial_position, dimensions, velocity)
        # Référence à l'instance de la classe Game
        self.game = game
        # Groupe de projectiles tirés par le tank
        self.all_projectiles = pygame.sprite.Group()
        # Temps du dernier tir
        self.last_shot = 0
        # Rotation initiale du tank
        self.rotation = rotation
        self.move(initial_position[0], initial_position[1], self.rotation)  # Déplacement initial du tank
        
        self.life = 100  # Points de vie du tank

        self.dimensions = dimensions

    # Méthode pour lancer un projectile
    def launch_projectile(self, angle, start):
        # Ajoute un nouveau projectile au groupe de projectiles
        self.all_projectiles.add(Bullet(self.game, angle=angle, start=start))
        
    def life_bar(self):
        # Dessine la barre de vie du tank
        myrect = pygame.Rect(0, 0, 110, 20)
        myrect.center = self.rect.center
        myrect.y = self.rect.y - 25
        pygame.draw.rect(self.game.screen, (0, 0, 0), myrect)
        if self.rotation == "haut" or self.rotation == "bas":
            if self.life <= 30:
                pygame.draw.rect(self.game.screen, (255, 0, 0), [myrect.left+5, myrect.top+5, self.life, 10])
            elif self.life <= 60:
                pygame.draw.rect(self.game.screen, (255, 255, 0), [myrect.left+5, myrect.top+5, self.life, 10])
            else:
                pygame.draw.rect(self.game.screen, (0, 255, 0), [myrect.left+5, myrect.top+5, self.life, 10])
        else:
            if self.life <= 30:
                pygame.draw.rect(self.game.screen, (255, 0, 0), [myrect.left+5, myrect.top+5, self.life, 10])
            elif self.life <= 60:
                pygame.draw.rect(self.game.screen, (255, 255, 0), [myrect.left+5, myrect.top+5, self.life, 10])
            else:
                pygame.draw.rect(self.game.screen, (0, 255, 0), [myrect.left+5, myrect.top+5, self.life, 10])

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
                self.move(dx, dy, "haut_droit")
                self.rotation = "haut_droit"
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                # Rotation et déplacement du tank vers le bas et la droite
                self.image = pygame.transform.rotate(self.image, -135)
                dx += self.velocity
                dy += self.velocity
                self.move(dx, dy, "bas_droit")
                self.rotation = "bas_droit"
            elif keys[pygame.K_q] and keys[pygame.K_z]:
                # Rotation et déplacement du tank vers le haut et la gauche
                self.image = pygame.transform.rotate(self.image, 45)
                dx -= self.velocity
                dy -= self.velocity
                self.move(dx, dy, "haut_gauche")
                self.rotation = "haut_gauche"
            elif keys[pygame.K_q] and keys[pygame.K_s]:
                # Rotation et déplacement du tank vers le bas et la gauche
                self.image = pygame.transform.rotate(self.image, 135)
                dx -= self.velocity
                dy += self.velocity
                self.move(dx, dy, "bas_gauche")
                self.rotation = "bas_gauche"
            # Gestion des mouvements sans diagonale
            elif keys[pygame.K_d]:
                # Rotation et déplacement du tank vers la droite
                self.image = pygame.transform.rotate(self.image, -90)
                dx += self.velocity
                self.move(dx, dy, "droite")
                self.rotation = "droite"
            elif keys[pygame.K_q]:
                # Rotation et déplacement du tank vers la gauche
                self.image = pygame.transform.rotate(self.image, 90)
                dx -= self.velocity
                self.move(dx, dy, "gauche")
                self.rotation = "gauche"
            elif keys[pygame.K_z]:
                # Rotation et déplacement du tank vers le haut
                self.image = pygame.transform.rotate(self.image, 0)
                dy -= self.velocity
                self.move(dx, dy, "haut")
                self.rotation = "haut"
            elif keys[pygame.K_s]:
                # Rotation et déplacement du tank vers le bas
                self.image = pygame.transform.rotate(self.image, 180)
                dy += self.velocity
                self.move(dx, dy, "bas")
                self.rotation = "bas"
                
        else:
            # Gestion des mouvements sans diagonale
            if keys[pygame.K_d]:
                # Rotation et déplacement du tank vers la droite
                self.image = pygame.transform.rotate(self.image, -90)
                dx += self.velocity
                self.move(dx, dy, "droite")
                self.rotation = "droite"
            elif keys[pygame.K_q]:
                # Rotation et déplacement du tank vers la gauche
                self.image = pygame.transform.rotate(self.image, 90)
                dx -= self.velocity
                self.move(dx, dy, "gauche")
                self.rotation = "gauche"
            elif keys[pygame.K_z]:
                # Rotation et déplacement du tank vers le haut
                self.image = pygame.transform.rotate(self.image, 0)
                dy -= self.velocity
                self.move(dx, dy, "haut")
                self.rotation = "haut"
            elif keys[pygame.K_s]:
                # Rotation et déplacement du tank vers le bas
                self.image = pygame.transform.rotate(self.image, 180)
                dy += self.velocity
                self.move(dx, dy, "bas")
                self.rotation = "bas"
                
        # Si la touche 'espace' est pressée
        if keys[pygame.K_SPACE]:
            # Vérifie si le temps écoulé depuis le dernier tir est supérieur à 0.5 seconde
            now = time.time()
            if now - self.last_shot > 0.5:
                # Appel de la méthode pour lancer un projectile
                self.launch_projectile(self.game.tanks[0][1].get_angle(), self.game.tanks[0][1].get_position_bout_canon())
                self.last_shot = now
        
        # Si la touche '0' du pavé numérique est pressée
        if keys[pygame.K_KP0]:
            # Inversion du mode de pause du jeu
            self.game.freeze = not self.game.freeze
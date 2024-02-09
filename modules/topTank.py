import pygame
import math

class TopTank(pygame.sprite.Sprite):
    def __init__(self, game, tank, image_path="assets/toptank.png"):
        super().__init__()  # Appel du constructeur de la classe parente (pygame.sprite.Sprite)
        self.game = game  # Référence à l'instance de la classe Game
        self.tank = tank  # Référence à l'instance de la classe Tank associée
        self.image = pygame.image.load(image_path)  # Chargement de l'image à partir du chemin spécifié
        self.image = pygame.transform.scale(self.image, (150, 150))  # Redimensionnement de l'image aux dimensions spécifiées
        dimensions = (150, 150)
        if game.debug:
            #ajout d'une bordure rouge autour de l'image
            self.image.fill((255, 0, 0), rect=[0, 0, dimensions[0], 5])
            self.image.fill((255, 0, 0), rect=[0, 0, 5, dimensions[1]])
            self.image.fill((255, 0, 0), rect=[0, dimensions[1]-5, dimensions[0], 5])
            self.image.fill((255, 0, 0), rect=[dimensions[0]-5, 0, 5, dimensions[1]])
        self.image = pygame.transform.rotate(self.image, -90)  # Rotation initiale de l'image
        self.rect = self.image.get_rect()  # Obtention du rectangle englobant l'image (utilisé pour le positionnement et la détection des collisions)
        self.image_original = self.image  # Sauvegarde de l'image originale pour les rotations futures
        self.angle = 0  # Angle initial de rotation

    def update(self):
        self.rotate()  # Appel de la méthode pour faire tourner le tank
        self.update_position()  # Appel de la méthode pour mettre à jour la position du tank

    def rotate(self):
        # Calcul de l'angle entre la position de la souris et la position du tank
        mouse_position = pygame.mouse.get_pos()
        player_position = self.tank.rect.center
        tank_center = (self.tank.rect.x + self.tank.rect.width / 2, self.tank.rect.y + self.tank.rect.height / 2)
        self.angle = math.atan2(mouse_position[1] - player_position[1], mouse_position[0] - player_position[0])
        self.angle = math.degrees(self.angle)
        # Rotation de l'image du tank en fonction de l'angle calculé
        self.image = pygame.transform.rotate(self.image_original, -self.angle)
        # Mise à jour du rectangle englobant pour correspondre à la nouvelle image
        self.direction = self.tank.rotation
        if self.direction == "haut" or self.direction == "bas":
            self.rect = self.image.get_rect(center=self.tank.rect.center)
        elif self.direction == "droite" or self.direction == "gauche":
            self.rect = self.image.get_rect(center=(tank_center[0] + 10, tank_center[1] - 10))
        else:
            self.rect = self.image.get_rect(center=(tank_center[0] + 22, tank_center[1] + 15))

    def update_position(self):
        # Mise à jour de la position du tank pour correspondre à celle du tank associé
        self.rect.center = self.tank.rect.center

    def get_angle(self):
        # Retourne l'angle actuel de rotation du tank
        return self.angle

    def get_position_bout_canon(self):
        # Calcule et retourne la position du bout du canon du tank
        center = self.rect.center
        distance = 70
        angle = math.radians(self.angle)
        return (center[0] + distance * math.cos(angle), center[1] + distance * math.sin(angle))
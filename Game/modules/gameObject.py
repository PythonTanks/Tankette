import pygame  # Importe le module pygame

# Classe représentant un objet de jeu, héritant de pygame.sprite.Sprite
class GameObject(pygame.sprite.Sprite):
    # Le constructeur de la classe GameObject
    def __init__(self, game, image_path, initial_position=(0, 0), dimensions=(100, 100), custom_rotate=0):
        super().__init__()  # Appel du constructeur de la classe parente (pygame.sprite.Sprite)
        self.game = game  # Référence à l'instance de la classe Game
            
        # Chargement de l'image à partir du chemin spécifié et redimensionnement aux dimensions spécifiées
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, dimensions)
        
        # Ajout d'une bordure rouge autour de l'image si le mode debug est activé
        if game.debug:
            self.image.fill((255, 0, 0), rect=[0, 0, dimensions[0], 5])
            self.image.fill((255, 0, 0), rect=[0, 0, 5, dimensions[1]])
            self.image.fill((255, 0, 0), rect=[0, dimensions[1]-5, dimensions[0], 5])
            self.image.fill((255, 0, 0), rect=[dimensions[0]-5, 0, 5, dimensions[1]])
            
        # Création de différentes versions de l'image, chacune tournée dans une direction différente
        self.image_right = pygame.transform.rotate(self.image, -90)
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.image_up = pygame.transform.rotate(self.image, 0)
        self.image_down = pygame.transform.rotate(self.image, 180)
        self.image_custom = pygame.transform.rotate(self.image, custom_rotate)
        self.image_up_left = pygame.transform.rotate(self.image, 45)
        self.image_up_right = pygame.transform.rotate(self.image, -45)
        self.image_down_left = pygame.transform.rotate(self.image, 135)
        self.image_down_right = pygame.transform.rotate(self.image, -135)
        
        # Obtention du rectangle englobant l'image (utilisé pour le positionnement et la détection des collisions)
        self.rect = self.image.get_rect()
        # Positionnement du rectangle à la position initiale spécifiée
        self.rect.topleft = initial_position
        
    # Méthode pour obtenir la position actuelle de l'objet
    def get_position(self):
        return [self.rect.x, self.rect.y]

    # Méthode pour définir la position de l'objet
    def set_position(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    # Méthode pour obtenir la hitbox (rectangle englobant) de l'objet
    def get_hitbox(self):
        return self.rect

    # Méthode pour obtenir l'image de l'objet (utilisée pour le dessin)
    def get_Sprite(self):
        return self.image
    
        # Méthode pour faire tourner l'image de l'objet
    def spriteRotate(self, rotate):
        if rotate == "droite":
            self.image = self.image_right
        elif rotate == "gauche":
            self.image = self.image_left
        elif rotate == "haut":
            self.image = self.image_up
        elif rotate == "bas":
            self.image = self.image_down
        elif rotate == "haut_droit":
            self.image = self.image_up_right
        elif rotate == "haut_gauche":
            self.image = self.image_up_left
        elif rotate == "bas_droit":
            self.image = self.image_down_right
        elif rotate == "bas_gauche":
            self.image = self.image_down_left
        else:
            self.image = self.image_custom
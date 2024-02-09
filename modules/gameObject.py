import pygame

class GameObject(pygame.sprite.Sprite):
    # Le constructeur de la classe GameObject
    def __init__(self, game, image_path, initial_position=(0, 0), dimensions=(100, 100), custom_rotate=0):
        super().__init__()  # Appel du constructeur de la classe parente (pygame.sprite.Sprite)
        self.game = game  # Référence à l'instance de la classe Game
            
        
        self.image = pygame.image.load(image_path)  # Chargement de l'image à partir du chemin spécifié
        self.image = pygame.transform.scale(self.image, dimensions)  # Redimensionnement de l'image aux dimensions spécifiées
        if game.debug:
            #ajout d'une bordure rouge autour de l'image
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
        self.rect = self.image.get_rect()  # Obtention du rectangle englobant l'image (utilisé pour le positionnement et la détection des collisions)
        self.rect.topleft = initial_position  # Positionnement du rectangle à la position initiale spécifiée

    # Méthode pour obtenir la position actuelle de l'objet
    def get_position(self):
        return self.rect.topleft

    # Méthode pour définir la position de l'objet
    def set_position(self, position):
        self.rect.topleft = position

    # Méthode pour obtenir la hitbox (rectangle englobant) de l'objet
    def get_hitbox(self):
        return self.rect

    # Méthode pour obtenir l'image de l'objet (utilisée pour le dessin)
    def get_Sprite(self):
        return self.image
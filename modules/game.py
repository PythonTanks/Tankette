import pygame
import math
import time

class Game:
    # Le constructeur de la classe Game
    def __init__(self, title="My Game", width=1920, height=1080, fps=60, background_path=None, icon_path=None):
        # Initialisation des attributs de la classe
        self.title = title  # Titre de la fenêtre du jeu
        self.width = width  # Largeur de la fenêtre du jeu
        self.height = height  # Hauteur de la fenêtre du jeu
        self.fps = fps  # Nombre de frames par seconde
        self.background_path = pygame.image.load(background_path)  # Chemin vers l'image de fond
        self.background = pygame.transform.scale(self.background_path, (self.width, self.height))  # Image de fond redimensionnée
        self.icon_path = icon_path  # Chemin vers l'icône du jeu
        
        self.pressed = {}  # Dictionnaire pour gérer les touches pressées

        # Création des objets Tank et TopTank
        self.tank = Tank(self, initial_position=(100, 100))
        self.toptank = TopTank(self.tank)

    # Méthode pour démarrer le jeu
    def start(self):        
        pygame.init()  # Initialisation de Pygame
        pygame.display.set_caption(self.title)  # Définition du titre de la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)  # Création de la fenêtre du jeu
        
        self.is_running = True  # Le jeu est en cours d'exécution
        
        # Boucle principale du jeu
        while self.is_running:

            # Dessin du fond
            self.screen.blit(self.background, (0,0))

            # Dessin des objets Tank et TopTank
            self.screen.blit(self.tank.image, self.tank.rect)
            self.screen.blit(self.toptank.image, self.toptank.rect)

            # Mise à jour et dessin des projectiles
            for bullet in self.tank.all_projectiles:
                bullet.update()
            self.tank.all_projectiles.draw(self.screen)

            # Gestion des entrées utilisateur
            self.tank.handle_input()
            self.toptank.rotate()
            pygame.display.flip()  # Mise à jour de l'affichage

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    pygame.quit()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # On enregistre que la touche est pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée

class GameObject(pygame.sprite.Sprite):
    # Le constructeur de la classe GameObject
    def __init__(self, image_path, initial_position=(0, 0), dimensions=(150, 150), custom_rotate=0):
        super().__init__()  # Appel du constructeur de la classe parente (pygame.sprite.Sprite)
        self.image = pygame.image.load(image_path)  # Chargement de l'image à partir du chemin spécifié
        self.image = pygame.transform.scale(self.image, dimensions)  # Redimensionnement de l'image aux dimensions spécifiées
        # Création de différentes versions de l'image, chacune tournée dans une direction différente
        self.image_right = pygame.transform.rotate(self.image, -90)
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.image_up = pygame.transform.rotate(self.image, 0)
        self.image_down = pygame.transform.rotate(self.image, 180)
        self.image_custom = pygame.transform.rotate(self.image, custom_rotate)
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
    
class Movable(GameObject):
    # Le constructeur de la classe Movable
    def __init__(self, image_path, initial_position=(0, 0), dimensions=(150, 150), velocity=5, custom_rotate=0):
        # Appel du constructeur de la classe parente (GameObject)
        super().__init__(image_path, initial_position, dimensions, custom_rotate)
        # Initialisation de la vitesse de l'objet
        self.velocity = velocity

    # Méthode pour déplacer l'objet
    def move(self, dx, dy, rotate):
        # Modification de la position de l'objet en fonction des déplacements dx et dy
        self.rect.x += dx
        self.rect.y += dy
        # Rotation de l'image de l'objet
        self.image = rotate

class Tank(Movable):
    def __init__(self, game, image_path="assets/tank.png", initial_position=(0, 0), dimensions=(150, 150), velocity=10):
        # Appel du constructeur de la classe parente (Movable)
        super().__init__(image_path, initial_position, dimensions, velocity)
        # Référence à l'instance de la classe Game
        self.game = game
        # Groupe de projectiles tirés par le tank
        self.all_projectiles = pygame.sprite.Group()
        # Temps du dernier tir
        self.last_shot = 0

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

        # Si la touche 'd' est pressée, le tank se déplace vers la droite
        if keys[pygame.K_d]:
            self.image = pygame.transform.rotate(self.image, -90)
            dx += self.velocity
            self.move(dx, dy, self.image_right)
        # Si la touche 'q' est pressée, le tank se déplace vers la gauche
        elif keys[pygame.K_q]:
            self.image = pygame.transform.rotate(self.image, 90)
            dx -= self.velocity
            self.move(dx, dy, self.image_left)
        # Si la touche 'z' est pressée, le tank se déplace vers le haut
        elif keys[pygame.K_z]:
            self.image = pygame.transform.rotate(self.image, 0)
            dy -= self.velocity
            self.move(dx, dy, self.image_up)
        # Si la touche 's' est pressée, le tank se déplace vers le bas
        elif keys[pygame.K_s]:
            self.image = pygame.transform.rotate(self.image, 180)
            dy += self.velocity
            self.move(dx, dy, self.image_down)

        # Si la touche 'espace' est pressée, le tank tire un projectile
        if keys[pygame.K_SPACE]:
            self.launch_projectile(self.game.toptank.get_angle(), self.game.toptank.get_position_bout_canon())

class TopTank(pygame.sprite.Sprite):
    def __init__(self, tank, image_path="assets/toptank.png"):
        super().__init__()  # Appel du constructeur de la classe parente (pygame.sprite.Sprite)
        self.tank = tank  # Référence à l'instance de la classe Tank associée
        self.image = pygame.image.load(image_path)  # Chargement de l'image à partir du chemin spécifié
        self.image = pygame.transform.scale(self.image, (150, 150))  # Redimensionnement de l'image aux dimensions spécifiées
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
        self.angle = math.atan2(mouse_position[1] - player_position[1], mouse_position[0] - player_position[0])
        self.angle = math.degrees(self.angle)
        # Rotation de l'image du tank en fonction de l'angle calculé
        self.image = pygame.transform.rotate(self.image_original, -self.angle)
        # Mise à jour du rectangle englobant pour correspondre à la nouvelle image
        self.rect = self.image.get_rect(center=self.tank.rect.center)

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
    
class Bullet(Movable):
    def __init__(self, game, velocity=20, angle=0, start=(0, 0)):
        # Appel du constructeur de la classe parente (Movable)
        super().__init__("assets/bullet.png", start, (50, 50), velocity, 270-angle)
        
        # Angle de déplacement de la balle
        self.angle = angle
        # Position de départ de la balle
        self.start = start
        # Rectangle englobant l'image de la balle
        self.rect = self.image.get_rect(center=start)
        # Vitesse de déplacement de la balle
        self.velocity = velocity
        # Référence à l'instance de la classe Game
        self.game = game
        
        # Calcul des composantes dx et dy du déplacement de la balle
        self.dx = math.cos(math.radians(self.angle)) * self.velocity
        self.dy = math.sin(math.radians(self.angle)) * self.velocity

    def update(self):
        # Déplacement de la balle
        self.move(self.dx, self.dy, self.image_custom)
        
        # Si la balle sort de l'écran, elle est supprimée
        if self.rect.x < 0 or self.rect.x > self.game.width or self.rect.y < 0 or self.rect.y > self.game.height:
            self.kill()
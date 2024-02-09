import pygame
from modules.tank import Tank
from modules.topTank import TopTank

class Game:
    # Le constructeur de la classe Game
    def __init__(self, title="My Game", width=1920, height=1080, fps=60, background_path=None, icon_path=None, debug=False, diagonales=False):
        # Initialisation des attributs de la classe
        self.title = title  # Titre de la fenêtre du jeu
        self.width = width  # Largeur de la fenêtre du jeu
        self.height = height  # Hauteur de la fenêtre du jeu
        self.fps = fps  # Nombre de frames par seconde
        self.background_path = pygame.image.load(background_path)  # Chemin vers l'image de fond
        self.background = pygame.transform.scale(self.background_path, (self.width, self.height))  # Image de fond redimensionnée
        self.icon_path = icon_path  # Chemin vers l'icône du jeu
        
        self.pressed = {}  # Dictionnaire pour gérer les touches pressées
        
        self.debug = debug  # Mode de débogage
        
        self.diagonales = diagonales  # Activation des déplacements en diagonale
        
        self.freeze = False  # Mode de pause du jeu

        # Création des objets Tank et TopTank
        self.tank = Tank(self, initial_position=(100, 100))
        self.toptank = TopTank(self, self.tank)

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
            
            if self.debug:
                self.debugScreen(pygame.mouse.get_pos())
                
            pygame.display.update()  # Mise à jour de l'affichage

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    pygame.quit()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # On enregistre que la touche est pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée
    
    def debugScreen(self, info, x = 10, y = 10):
        display_surface = pygame.display.get_surface()
        font = pygame.font.Font(None, 30)
        debug_surface = font.render(str(info), True, (255, 255, 255))
        debug_rect = debug_surface.get_rect(topleft=(x, y))
        display_surface.blit(debug_surface, debug_rect)
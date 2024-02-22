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
        
        self.tankEnemy = Tank(self, initial_position=(self.width - 100, self.height - 100))
        self.toptankEnemy = TopTank(self, self.tankEnemy)

    # Méthode pour démarrer le jeu
    def start(self):        
        pygame.init()  # Initialisation de Pygame
        pygame.display.set_caption(self.title)  # Définition du titre de la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)  # Création de la fenêtre du jeu

        self.smallfont = pygame.font.Font(None, 35) # Création d'une police de caractères
        self.largefont = pygame.font.Font(None, 75) # Création d'une police de caractères
        self.main_title = self.largefont.render('Tanks !' , True , (150,150,150)) # Création d'une surface de texte
        self.main_play = self.smallfont.render('Jouer' , True , (255,255,255)) # Création d'une surface de texte
        self.main_options = self.smallfont.render('Options' , True , (255,255,255)) # Création d'une surface de texte
        self.main_quit = self.smallfont.render('Quitter' , True , (255,255,255)) # Création d'une surface de texte
        self.main_back = self.smallfont.render('Retour' , True , (255,255,255)) # Création d'une surface de texte
        
        self.is_running = True  # Le jeu est en cours d'exécution
        self.in_main_menu = True  # Le jeu est dans le menu principal
        
        # Boucle principale du jeu
        while self.is_running:

            if self.in_main_menu:
                self.mainmenuScreen()
                self.in_main_menu = False

            # Dessin du fond
            self.screen.blit(self.background, (0,0))

            # Dessin des objets Tank et TopTank
            self.screen.blit(self.tank.image, self.tank.rect)
            self.screen.blit(self.toptank.image, self.toptank.rect)
            
            self.screen.blit(self.tankEnemy.image, self.tankEnemy.rect)
            self.screen.blit(self.toptankEnemy.image, self.toptankEnemy.rect)

            # Mise à jour et dessin des projectiles
            for bullet in self.tank.all_projectiles:
                bullet.update()
            self.tank.all_projectiles.draw(self.screen)

            # Gestion des entrées utilisateur
            self.tank.handle_input()
            self.toptank.rotate()
            
            self.tankEnemy.handle_input()
            self.toptankEnemy.rotate()
            
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

            if(self.pressed.get(pygame.K_ESCAPE)):
                self.in_main_menu = True

    
    # Méthode pour afficher des informations de débogage à l'écran
    def debugScreen(self, info, x = 10, y = 10):
        display_surface = pygame.display.get_surface()   # Récupération de la surface d'affichage
        font = pygame.font.Font(None, 30)   # Création d'une police de caractères 
        debug_surface = font.render(str(info), True, (255, 255, 255))   # Création d'une surface de texte
        debug_rect = debug_surface.get_rect(topleft=(x, y))   # Création d'un rectangle pour la surface de texte
        display_surface.blit(debug_surface, debug_rect)   # Affichage de la surface de texte

    def mainmenuScreen(self):
        is_open = True
        while is_open:
            self.screen.fill((0, 0, 0))

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50)) # Dessine le titre
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,290,150,40]) 
            self.screen.blit(self.main_play, (self.width/2 - self.main_play.get_width()/2, 300)) # Dessine le bouton "Jouer"
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,340,150,40])
            self.screen.blit(self.main_options, (self.width/2 - self.main_options.get_width()/2, 350)) # Dessine le bouton "Options"
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,390,150,40])
            self.screen.blit(self.main_quit, (self.width/2 - self.main_quit.get_width()/2, 400)) # Dessine le bouton "Quitter"

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    pygame.quit()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # On enregistre que la touche est pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 290 <= event.pos[1] <= 330:
                            is_open = False
                            self.is_running = True
                        elif self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 390 <= event.pos[1] <= 430:
                            self.is_running = False
                            is_open = False
                        elif self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 340 <= event.pos[1] <= 380:
                            self.is_running = True
                            self.optionsScreen()

    def optionsScreen(self):
        is_open = True
        while is_open:
            self.screen.fill((0, 0, 0))

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,490,150,40])
            self.screen.blit(self.main_back, (self.width/2 - self.main_back.get_width()/2, 500))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    pygame.quit()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # On enregistre que la touche est pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 490 <= event.pos[1] <= 530:
                            self.is_running = True
                            is_open = False

                if(self.pressed.get(pygame.K_ESCAPE)):
                    self.in_main_menu = True
                    is_open = False
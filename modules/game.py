import pygame
from modules.tank import Tank
from modules.topTank import TopTank
from modules.network import connect_to_server, send_message, get_last_message, close_connection

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
        self.tank = Tank(self)
        self.toptank = TopTank(self, self.tank)
        
        self.tankEnemy = Tank(self)
        self.toptankEnemy = TopTank(self, self.tankEnemy)

        # Connexion au serveur
        connect_to_server()

    # Méthode pour démarrer le jeu
    def start(self):        
        pygame.init()  # Initialisation de Pygame
        pygame.display.set_caption(self.title)  # Définition du titre de la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)  # Création de la fenêtre du jeu
        
        self.is_running = True  # Le jeu est en cours d'exécution
        
        self.screen.blit(self.background, (0,0))
        
        self.screen.blit(self.tank.image, self.tank.rect)
        self.screen.blit(self.toptank.image, self.toptank.rect)
        
        self.screen.blit(self.tankEnemy.image, self.tankEnemy.rect)
        self.screen.blit(self.toptankEnemy.image, self.toptankEnemy.rect)
        
        self.tank.set_position((100, 100))
        self.tank.spriteRotateDirection("droite")
        self.tank.rotation = "droite"
        self.toptank.rotate_with_angle(45.)
        
        self.tankEnemy.set_position((self.width - 200, self.height - 200))
        self.tankEnemy.spriteRotateDirection("gauche")
        self.tankEnemy.rotation = "gauche"
        self.toptankEnemy.rotate_with_angle(135.)
        
        
        
        # Boucle principale du jeu
        while self.is_running:
            
            # On vérifie que le jeu n'est pas fermé par un alt+f4
            if not pygame.display.get_init():
                close_connection()
                break

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
            
            if self.debug:
                self.debugScreen(pygame.mouse.get_pos())
                
            # Envoi des données au serveur
            send_message([self.tank.get_position(), self.tank.rotation, self.toptank.get_angle()])
            
            # On prend le dernier message reçu
            message = get_last_message()
            #exemple de message = "[[600, 370], 'haut', -6.188615963241602]" qui est un string et [600, 370] est une liste qui contient la position du tank
            if message:
                message = message.split(",")
                position = [int(message[0][2:]), int(message[1][1:-1])]
                rotation = message[2][2:-1]
                angle = float(message[3][1:-2])
                self.tankEnemy.set_position(position)
                self.tankEnemy.spriteRotateDirection(rotation)
                self.tankEnemy.rotation = rotation
                self.toptankEnemy.rotate_with_angle(angle)                
                
                if self.debug:
                    print(f"[CLIENT] Message reçu: {message}")
                    
            pygame.display.update()  # Mise à jour de l'affichage

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    close_connection()
                    pygame.quit()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # On enregistre que la touche est pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée
    
    # Méthode pour afficher des informations de débogage à l'écran
    def debugScreen(self, info, x = 10, y = 10):
        display_surface = pygame.display.get_surface()   # Récupération de la surface d'affichage
        font = pygame.font.Font(None, 30)   # Création d'une police de caractères 
        debug_surface = font.render(str(info), True, (255, 255, 255))   # Création d'une surface de texte
        debug_rect = debug_surface.get_rect(topleft=(x, y))   # Création d'un rectangle pour la surface de texte
        display_surface.blit(debug_surface, debug_rect)   # Affichage de la surface de texte
import pygame  # Importation de la bibliothèque Pygame pour la création de jeux
import socket  # Importation de la bibliothèque Socket pour les communications réseau
import threading  # Importation de la bibliothèque threading pour gérer les threads
import yaml # Importation de la bibliothèque yaml pour manipuler des fichiers de configuration
import time  # Importation de la bibliothèque time pour manipuler le temps
import requests  # Importation de la bibliothèque requests pour effectuer des requêtes HTTP
from modules.tank import Tank  # Importation de la classe Tank depuis le fichier modules/tank.py
from modules.topTank import TopTank  # Importation de la classe TopTank depuis le fichier modules/topTank.py
from modules.network import connect_to_server, send_message, get_last_message, close_connection  # Importation de certaines fonctions depuis le fichier modules/network.py
from modules.bullet import Bullet  # Importation de la classe Bullet depuis le fichier modules/bullet.py

configFile = open("../config.yaml", "r")
configContent = yaml.load(configFile, Loader=yaml.Loader) # Charge le contenu du fichier de configuration

IP_SERVER = configContent["API_ADDRESS"] # Adresse IP du serveur auquel se connecter

#IP_SERVER = "192.168.1.36"  # Adresse IP du serveur auquel se connecter

class Game:  # Définition de la classe Game

    def __init__(self, title="My Game", width=1920, height=1080, fps=60, background_path=None, icon_path=None, debug=False, diagonales=False):  # Définition du constructeur de la classe Game et de ses paramètres
        self.title = title  # Titre de la fenêtre du jeu
        self.width = width  # Largeur de la fenêtre du jeu
        self.height = height  # Hauteur de la fenêtre du jeu
        self.fps = fps  # Nombre de frames par seconde
        self.background_path = pygame.image.load(background_path)  # Chargement de l'image de fond
        self.background = pygame.transform.scale(self.background_path, (self.width, self.height))  # Redimensionnement de l'image de fond
        self.icon_path = icon_path  # Chemin vers l'icône du jeu
        self.ip = ""  # Adresse IP du serveur (initialisation à vide)
        
        self.pressed = {}  # Dictionnaire pour gérer les touches pressées
        
        self.debug = debug  # Mode de débogage
        
        self.diagonales = diagonales  # Activation des déplacements en diagonale
        
        self.freeze = False  # Mode de pause du jeu

        self.status = "menu"  # Statut du jeu (menu, play, options, ingame)
        
        self.num = 1  # Initialisation d'une variable numérique
        
        self.connected = False  # Initialisation de la variable indiquant l'état de connexion au serveur
        
        self.setFonts()  # Initialisation des polices de caractères
        
        self.is_running = True  # Le jeu est en cours d'exécution
        self.in_main_menu = True  # Le jeu est dans le menu principal
        
        self.in_game = False  # Le jeu n'est pas en cours
        
        self.tanks = []  # Initialisation de la liste des tanks
        
    def setPygame(self):
        pygame.init()  # Initialisation de Pygame
        pygame.display.set_caption(self.title)  # Définition du titre de la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)  # Création de la fenêtre du jeu
    
    def setFonts(self):
        self.smallfont = pygame.font.Font(None, 35)  
        self.largefont = pygame.font.Font(None, 75)
        self.main_title = self.largefont.render('Tanks !' , True , (150,150,150)) 
        self.main_play = self.smallfont.render('Jouer' , True , (255,255,255))
        self.main_options = self.smallfont.render('Options' , True , (255,255,255)) 
        self.main_quit = self.smallfont.render('Quitter' , True , (255,255,255)) 
        self.main_back = self.smallfont.render('Retour' , True , (255,255,255)) 
        self.ip_text = self.smallfont.render('Port du serveur' , True , (255,255,255))
        self.play_text = self.smallfont.render('Rejoindre' , True , (255,255,255))
        self.create_text = self.smallfont.render('Créer' , True , (255,255,255))

    def game(self):  # Méthode pour démarrer le jeu
        
        self.setPygame()  # Initialisation de Pygame
        
        self.screen.blit(self.background, (0,0))  # Affichage de l'image de fond
        
        # Boucle principale du jeu
        while self.is_running:
            
            # Vérification si la fenêtre est fermée
            if not pygame.display.get_init():
                close_connection()  # Fermeture de la connexion avec le serveur
                self.connected = False  # Mise à jour de l'état de connexion
                break
            
            if self.debug:
                self.debugScreen(pygame.mouse.get_pos())  # Affichage des informations de débogage
            
            if self.in_main_menu:
                self.mainmenuScreen()  # Affichage de l'écran du menu principal
                self.in_main_menu = False  # Changement du statut du menu
            
            if self.in_game and len(self.tanks) > 1:
            
                for tank in self.tanks:
                    for bullet in tank[0].all_projectiles:
                        bullet.update()
                    tank[0].all_projectiles.draw(self.screen)
            
                # Gestion des entrées utilisateur
                self.tanks[0][0].handle_input()  # Gestion des contrôles du Tank
                self.tanks[0][1].rotate()  # Rotation du TopTank
            
                # Préparation des données à envoyer au serveur
                data = [self.tanks[0][0].get_position(), self.tanks[0][0].rotation, self.tanks[0][1].get_angle(), [{"position": [projectile.rect.x, projectile.rect.y], "angle": projectile.angle} for projectile in self.tanks[0][0].all_projectiles]]
                
                # Envoi des données au serveur
                send_message(data)
            
                # Récupération du dernier message reçu
                message = get_last_message()
            
            # Gestion des messages reçus du serveur
            if message == "Disconnected":
                print("[CLIENT] Déconnexion du serveur.")
                close_connection()  # Fermeture de la connexion
                self.in_main_menu = True  # Retour au menu principal
                self.tanks = []  # Réinitialisation de la liste des tanks
                
            if message and (message != 1 or message != 2) and type(message) == list:
                # Mise à jour des informations des tanks ennemis
                self.tanks[1][0].set_position(message[0])
                self.tanks[1][0].spriteRotateDirection(message[1])
                self.tanks[1][0].rotation = message[1]
                self.tanks[1][1].rotate_with_angle(message[2])
                self.tanks[1][0].all_projectiles.empty()  # Effacement des projectiles existants
                for projectile in message[3]:  # Création des nouveaux projectiles
                    self.tanks[1][0].all_projectiles.add(Bullet(self, angle=projectile["angle"], start=projectile["position"]))
                
                if self.debug:
                    print(f"[CLIENT] Message reçu: {message}")  # Affichage du message reçu du serveur
                    
            pygame.display.update()  # Mise à jour de l'affichage
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    self.stopGame()  # Arrêt du jeu
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # Enregistrement de la touche pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # Enregistrement de la touche relâchée
            
            if(self.pressed.get(pygame.K_ESCAPE)):
                self.in_main_menu = True  # Retour au menu principal en cas d'appui sur la touche ESCAPE
    
        # Méthode pour afficher des informations de débogage à l'écran
    def debugScreen(self, info, x=10, y=10):
        display_surface = pygame.display.get_surface()   # Récupération de la surface d'affichage
        font = pygame.font.Font(None, 30)   # Création d'une police de caractères 
        debug_surface = font.render(str(info), True, (255, 255, 255))   # Création d'une surface de texte
        debug_rect = debug_surface.get_rect(topleft=(x, y))   # Création d'un rectangle pour la surface de texte
        display_surface.blit(debug_surface, debug_rect)   # Affichage de la surface de texte

    def mainmenuScreen(self):
        if self.connected:
            close_connection()  # Fermeture de la connexion si elle est établie
        is_open = True
        while is_open:
            self.screen.fill((0, 0, 0))  # Remplissage de l'écran en noir

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))  # Affichage du titre
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,290,150,40]) 
            self.screen.blit(self.main_play, (self.width/2 - self.main_play.get_width()/2, 300))  # Affichage du bouton "Jouer"
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,340,150,40])
            self.screen.blit(self.main_options, (self.width/2 - self.main_options.get_width()/2, 350))  # Affichage du bouton "Options"
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,390,150,40])
            self.screen.blit(self.main_quit, (self.width/2 - self.main_quit.get_width()/2, 400))  # Affichage du bouton "Quitter"

            pygame.display.update()  # Mise à jour de l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    return self.stopGame()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # Enregistrement de la touche pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # Enregistrement de la touche relâchée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Vérification des clics sur les boutons du menu principal
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 290 <= event.pos[1] <= 330:
                            self.status = "play"  # Changement de statut pour jouer
                            self.playScreen()  # Affichage de l'écran de jeu
                            if self.status == "ingame":
                                is_open = False
                        elif self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 390 <= event.pos[1] <= 430:
                            return self.stopGame()  # Arrêt de Pygame
                        elif self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 340 <= event.pos[1] <= 380:
                            self.status = "options"  # Changement de statut pour les options
                            self.is_running = True
                            self.optionsScreen()  # Affichage de l'écran des options

    def optionsScreen(self):
        is_open = True
        while is_open:
            self.screen.fill((0, 0, 0))  # Remplissage de l'écran en noir

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))  # Affichage du titre
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,490,150,40])
            self.screen.blit(self.main_back, (self.width/2 - self.main_back.get_width()/2, 500))  # Affichage du bouton "Retour"

            pygame.display.update()  # Mise à jour de l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    self.stopGame()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # Enregistrement de la touche pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # Enregistrement de la touche relâchée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 490 <= event.pos[1] <= 530:
                            self.is_running = True
                            is_open = False
                            self.status = "menu"

                if self.pressed.get(pygame.K_ESCAPE):
                    self.in_main_menu = True
                    is_open = False

    def playScreen(self):
        is_open = True
        write_mode = False  # Variable pour indiquer si le mode d'écriture est activé

        while is_open:

            self.screen.fill((0, 0, 0))  # Remplissage de l'écran en noir

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))  # Affichage du titre
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,540,150,40])
            self.screen.blit(self.main_back, (self.width/2 - self.main_back.get_width()/2, 550))  # Affichage du bouton "Retour"

            self.screen.blit(self.ip_text, (self.width/2 - self.ip_text.get_width()/2, 340))  # Affichage du texte ip

            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,440,150,40])
            self.screen.blit(self.play_text, (self.width/2 - self.play_text.get_width()/2, 450))  # Affichage du texte "Rejoindre"

            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,490,150,40])
            self.screen.blit(self.create_text, (self.width/2 - self.create_text.get_width()/2, 500))  # Affichage du texte "Créer"

            # Affichage du rectangle pour saisir l'adresse IP
            if write_mode:
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 300/2,370,300,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 300/2,370,300,40])

            ip_surface = self.smallfont.render(str(self.ip) , True , (255,255,255))  # Création d'une surface de texte
            self.screen.blit(ip_surface, (self.width/2 - ip_surface.get_width()/2, 380))  # Affichage du texte ip

            pygame.display.update()  # Mise à jour de l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    self.stopGame()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # On enregistre que la touche est pressée
                    if write_mode:
                        if event.key == pygame.K_BACKSPACE:
                            self.ip = str(self.ip)[:-1]  # Suppression du dernier caractère de l'adresse IP
                        else:
                            self.ip += event.unicode  # Ajout du caractère saisi à l'adresse IP
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Vérification des clics sur les différents boutons
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 540 <= event.pos[1] <= 580:
                            self.is_running = True
                            is_open = False
                            self.status = "menu"
                        if self.width/2 - 300/2 <= event.pos[0] <= self.width/2 - 300/2 + 300 and 370 <= event.pos[1] <= 410:
                            write_mode = True  # Activation du mode d'écriture
                        else:
                            write_mode = False  # Désactivation du mode d'écriture
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 - 150/2 + 300 and 440 <= event.pos[1] <= 480:
                            if self.ip != None:
                                try :
                                    self.ip = int(self.ip)
                                    if self.ip > 1000 and self.ip < 65535 and self.ip != 5555:
                                        response = connect_to_server(self.ip, IP_SERVER)
                                        if response:
                                            self.connected = True
                                            self.num = 2
                                            tank = self.tank
                                            self.tank = self.tankEnemy
                                            self.tankEnemy = tank
                                            toptank = self.toptank
                                            self.toptank = self.toptankEnemy
                                            self.toptankEnemy = toptank
                                            is_open = False
                                            self.is_running = True
                                            self.status = "ingame"
                                            self.tanks = [self.createMyTank(), self.createEnemyTank()]
                                except:
                                    continue
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 - 150/2 + 300 and 490 <= event.pos[1] <= 530:
                            self.ip = int(self.ip)
                            response = requests.post(f"http://{IP_SERVER}:5555/server/{self.ip}")
                            if response.status_code == 200:
                                time.sleep(0.25)
                                connect_to_server(self.ip, IP_SERVER)
                                self.connected = True
                                self.num = 1
                                is_open = False
                                self.is_running = True                                
                                self.status = "ingame"

                if self.pressed.get(pygame.K_ESCAPE):
                    self.in_main_menu = True
                    is_open = False
                    
    def stopGame(self):
        self.is_running = False  # Mise à jour de l'état de fonctionnement du jeu
        pygame.quit()  # Arrêt de Pygame
        close_connection()  # Fermeture de la connexion
        print("Game stopped")  # Message d'arrêt du jeu
        return None
    
    def createTanks(self):
        # Méthode pour créer les tanks au début du jeu
        self.tank.set_position((100, 100))  # Positionnement du tank du joueur
        self.tank.spriteRotateDirection("droite")  # Rotation du tank
        self.tank.rotation = "droite"  # Attribution de la direction
        self.toptank.rotate_with_angle(45.)  # Rotation du canon

        self.tankEnemy.set_position((self.width - 200, self.height - 200))  # Positionnement du tank ennemi
        self.tankEnemy.spriteRotateDirection("gauche")  # Rotation du tank ennemi
        self.tankEnemy.rotation = "gauche"  # Attribution de la direction
        self.toptankEnemy.rotate_with_angle(135.)  # Rotation du canon ennemi
    
    def createMyTank(self):
        tank = Tank(self)
        return (tank, TopTank(self, tank))
    
    def createEnemyTank(self):
        tank = Tank(self, image_path="assets/tank2.png")
        return (tank, TopTank(self, tank, image_path="assets/toptank2.png"))
    
    def setTank(self, tank, position=(100, 100), angle=45.):
        self.screen.blit(tank[0].image, tank[0].rect)
        self.screen.blit(tank[1].image, tank[1].rect)
        tank[0].set_position(position)  # Positionnement du tank du joueur
        tank[0].spriteRotateDirection("droite")  # Rotation du tank
        tank[0].rotation = "droite"  # Attribution de la direction
        tank[1].rotate_with_angle(angle)  # Rotation du canon
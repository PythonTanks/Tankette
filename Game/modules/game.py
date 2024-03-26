import pygame  # Importation de la bibliothèque Pygame pour la création de jeux
import socket  # Importation de la bibliothèque Socket pour les communications réseau
import threading  # Importation de la bibliothèque threading pour gérer les threads
import yaml # Importation de la bibliothèque yaml pour manipuler des fichiers de configuration
import time  # Importation de la bibliothèque time pour manipuler le temps
import requests  # Importation de la bibliothèque requests pour effectuer des requêtes HTTP
import datetime  # Importation de la bibliothèque datetime pour manipuler des objets datetime
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
        self.write_port_mode = ""  # Port du serveur (initialisation à vide)
        
        self.pressed = {}  # Dictionnaire pour gérer les touches pressées
        
        self.debug = debug  # Mode de débogage
        
        self.diagonales = diagonales  # Activation des déplacements en diagonale
        
        self.freeze = False  # Mode de pause du jeu

        self.status = "menu"  # Statut du jeu (menu, play, options, ingame)
        
        self.num = 1  # Initialisation d'une variable numérique
        
        self.connected = False  # Initialisation de la variable indiquant l'état de connexion au serveur
        self.client_socket = None  # Initialisation du socket client
        
        self.is_running = True  # Le jeu est en cours d'exécution
        self.in_main_menu = True  # Le jeu est dans le menu principal
        
        self.in_game = False  # Le jeu n'est pas en cours
        
        self.tanks = []  # Initialisation de la liste des tanks

        self.port = 5556 # Port par défaut
        self.ip = IP_SERVER # Adresse IP par défaut

        self.controls = {"up_key" : "z", "down_key": "s", "left_key" : "q", "right_key" : "d", "shoot_key" : "space"} # Initialisation du dictionnaire des contrôles
        
    def setPygame(self):
        pygame.init()  # Initialisation de Pygame
        pygame.display.set_caption(self.title)  # Définition du titre de la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)  # Création de la fenêtre du jeu
    
    def setFonts(self):
        # Initialisation des polices de caractères (textes généraux)
        self.smallfont = pygame.font.Font(None, 35)  
        self.largefont = pygame.font.Font(None, 75)
        self.mediumfont = pygame.font.Font(None, 50)
        self.main_title = self.largefont.render('Tanks !' , True , (150,150,150)) 
        self.main_play = self.smallfont.render('Jouer' , True , (255,255,255))
        self.main_options = self.smallfont.render('Options' , True , (255,255,255)) 
        self.main_quit = self.smallfont.render('Quitter' , True , (255,255,255)) 
        self.main_back = self.smallfont.render('Retour' , True , (255,255,255)) 

        # Initialisation des polices de caractères (textes menu jouer)
        self.port_text = self.smallfont.render('Port du serveur' , True , (255,255,255))
        self.ip_text = self.smallfont.render('Adresse IP du serveur' , True , (255,255,255))
        self.play_text = self.smallfont.render('Rejoindre' , True , (255,255,255))
        self.create_text = self.smallfont.render('Créer' , True , (255,255,255))

        # Initialisation des polices de caractères (textes options)
        self.up_key = self.smallfont.render('Haut' , True , (255,255,255))
        self.down_key = self.smallfont.render('Bas' , True , (255,255,255))
        self.left_key = self.smallfont.render('Gauche' , True , (255,255,255))
        self.right_key = self.smallfont.render('Droite' , True , (255,255,255))
        self.shoot_key = self.smallfont.render('Tirer' , True , (255,255,255))
        
        # Initialisation des polices de caractères (texte d'attente)
        self.wainting_text = self.mediumfont.render("En attente d'adversaire..." , True , (255,255,255))
        
        # Initialisation des polices de caractères (texte d'erreurs)
        self.error1_surface = self.smallfont.render("Serveur indisponible" , True , (255,64,64))  # Création d'une surface de texte
        self.error2_surface = self.smallfont.render("Error" , True , (255,64,64))  # Création d'une surface de texte
        self.error3_surface = self.smallfont.render("Port indisponible" , True , (255,64,64))  # Création d'une surface de texte

    def game(self):  # Méthode pour démarrer le jeu
        
        self.setPygame()  # Initialisation de Pygame

        self.setFonts()  # Initialisation des polices de caractères

        message = None  # Initialisation de la variable message (évite les erreurs de type NoneType)
        
        # Boucle principale du jeu
        while self.is_running:
            
            self.screen.blit(self.background, (0,0))  # Affichage de l'image de fond
            
            if self.in_game:
                message = get_last_message()
            
            if self.in_game and len(self.tanks) == 1:
                
                self.screen.blit(self.wainting_text, (self.width/2 - self.wainting_text.get_width()/2, 70))  # Affichage du titre
                
                self.screen.blit(self.tanks[0][0].image, self.tanks[0][0].rect)  # Affichage du Tank
                self.screen.blit(self.tanks[0][1].image, self.tanks[0][1].rect)  # Affichage du TopTank
                
                if message == "Connected":
                    self.tanks.append(self.createEnemyTank())
            
            if self.in_game and len(self.tanks) > 1:
                
                self.screen.blit(self.tanks[0][0].image, self.tanks[0][0].rect)
                self.screen.blit(self.tanks[0][1].image, self.tanks[0][1].rect)
                self.screen.blit(self.tanks[1][0].image, self.tanks[1][0].rect)
                self.screen.blit(self.tanks[1][1].image, self.tanks[1][1].rect)
                
                for tank in self.tanks:
                    for bullet in tank[0].all_projectiles:
                        bullet.update()
                    tank[0].all_projectiles.draw(self.screen)
            
            if self.in_main_menu:
                self.mainmenuScreen()  # Affichage de l'écran du menu principal
                self.in_main_menu = False  # Changement du statut du menu
            
            pygame.display.update()  # Mise à jour de l'affichage
            
            # Vérification si la fenêtre est fermée
            if not pygame.display.get_init():
                close_connection(self.client_socket)  # Fermeture de la connexion avec le serveur
                self.connected = False  # Mise à jour de l'état de connexion
                break
            
            if self.debug:
                self.debugScreen(pygame.mouse.get_pos())  # Affichage des informations de débogage
            
            if self.in_game and len(self.tanks) > 1:
                
                # Gestion des entrées utilisateur
                self.tanks[0][0].handle_input()  # Gestion des contrôles du Tank
                self.tanks[0][1].rotate()  # Rotation du TopTank
                
                # Gestion des messages reçus du serveur
                if message == "Disconnected":
                    print("[CLIENT] Déconnexion du serveur.")
                    close_connection(self.client_socket)  # Fermeture de la connexion
                    self.connected = False  # Mise à jour de l'état de connexion
                    self.in_main_menu = True  # Retour au menu principal
                    self.tanks = []  # Réinitialisation de la liste des tanks

                if message and (message != "Connected") and type(message) == list:
                    # Mise à jour des informations des tanks ennemis
                    self.tanks[1][0].set_position(message[0])
                    self.tanks[1][0].spriteRotate(message[1])
                    self.tanks[1][0].rotation = message[1]
                    self.tanks[1][1].rotate_with_angle(message[2])
                    self.tanks[1][0].all_projectiles.empty()  # Effacement des projectiles existants
                    for projectile in message[3]:  # Création des nouveaux projectiles
                        self.tanks[1][0].all_projectiles.add(Bullet(self, angle=projectile["angle"], start=projectile["position"]))

                    if self.debug:
                        print(f"[CLIENT] Message reçu: {message}")  # Affichage du message reçu du serveur
                        
                # Envoi des données au serveur
                if self.connected:
                    # Préparation des données à envoyer au serveur
                    data = [self.tanks[0][0].get_position(), self.tanks[0][0].rotation, self.tanks[0][1].get_angle(), [{"position": [projectile.rect.x, projectile.rect.y], "angle": projectile.angle} for projectile in self.tanks[0][0].all_projectiles]]
                    send_message(data, self.client_socket)

            
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
        self.tanks = []  # Réinitialisation de la liste des tanks
        self.in_game = False  # Le jeu n'est pas en cours
        if self.client_socket:
            close_connection(self.client_socket)  # Fermeture de la connexion avec le serveur
            self.connected = False  # Mise à jour de l'état de connexion
            self.client_socket = None  # Réinitialisation du socket client
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
        modify_up_key = False  # Variable pour indiquer si le mode de modification est activé
        modify_down_key = False
        modify_left_key = False
        modify_right_key = False
        modify_shoot_key = False

        while is_open:
            self.screen.fill((0, 0, 0))  # Remplissage de l'écran en noir

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))  # Affichage du titre

            self.screen.blit(self.up_key, (self.width/2 - self.up_key.get_width() - 200/2, 210))  # Affichage du texte "Haut"

            self.screen.blit(self.down_key, (self.width/2 - self.down_key.get_width() - 200/2, 260))  # Affichage du texte "Bas"

            self.screen.blit(self.left_key, (self.width/2 - self.left_key.get_width() - 200/2, 310))  # Affichage du texte "Gauche"

            self.screen.blit(self.right_key, (self.width/2 - self.right_key.get_width() - 200/2, 360))  # Affichage du texte "Droite"

            self.screen.blit(self.shoot_key, (self.width/2 - self.shoot_key.get_width() - 200/2, 410))  # Affichage du texte "Tirer"

            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,490,150,40])
            self.screen.blit(self.main_back, (self.width/2 - self.main_back.get_width()/2, 500)) # Affichage du bouton "Retour"

            if(modify_up_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,200,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,200,150,40])
            
            if(modify_down_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,250,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,250,150,40])

            if(modify_left_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,300,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,300,150,40])

            if(modify_right_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,350,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,350,150,40])

            if(modify_shoot_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,400,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,400,150,40])

            self.screen.blit(self.smallfont.render(self.controls["up_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 210))  # Affichage de la touche associée à "Haut"
            self.screen.blit(self.smallfont.render(self.controls["down_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 260))  # Affichage de la touche associée à "Bas"
            self.screen.blit(self.smallfont.render(self.controls["left_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 310))  # Affichage de la touche associée à "Gauche"
            self.screen.blit(self.smallfont.render(self.controls["right_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 360))  # Affichage de la touche associée à "Droite"
            self.screen.blit(self.smallfont.render(self.controls["shoot_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 410))  # Affichage de la touche associée à "Tirer"

            pygame.display.update()  # Mise à jour de l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    self.stopGame()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # Enregistrement de la touche pressée
                    if event.key == pygame.K_ESCAPE:  # Si la touche ESCAPE est pressée
                        self.status = "menu"  # Retour au menu principal
                        is_open = False
                        modify_up_key, modify_down_key, modify_left_key, modify_right_key, modify_shoot_key = False, False, False, False, False  # Réinitialisation des variables de modification
                        
                    if modify_up_key:
                        self.controls["up_key"] = pygame.key.name(event.key)
                        modify_up_key = False
                    elif modify_down_key:
                        self.controls["down_key"] = pygame.key.name(event.key)
                        modify_down_key = False
                    elif modify_left_key:
                        self.controls["left_key"] = pygame.key.name(event.key)
                        modify_left_key = False
                    elif modify_right_key:
                        self.controls["right_key"] = pygame.key.name(event.key)
                        modify_right_key = False
                    elif modify_shoot_key:
                        self.controls["shoot_key"] = pygame.key.name(event.key)
                        modify_shoot_key = False
        
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # Enregistrement de la touche relâchée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 490 <= event.pos[1] <= 530:
                            self.is_running = True
                            is_open = False
                            self.status = "menu"
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 200 <= event.pos[1] <= 240):
                            modify_up_key = True
                            modify_down_key, modify_left_key, modify_right_key, modify_shoot_key = False, False, False, False
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 250 <= event.pos[1] <= 290):
                            modify_down_key = True
                            modify_up_key, modify_left_key, modify_right_key, modify_shoot_key = False, False, False, False
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 300 <= event.pos[1] <= 340):
                            modify_left_key = True
                            modify_up_key, modify_down_key, modify_right_key, modify_shoot_key = False, False, False, False
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 350 <= event.pos[1] <= 390):
                            modify_right_key = True
                            modify_up_key, modify_down_key, modify_left_key, modify_shoot_key = False, False, False, False
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 400 <= event.pos[1] <= 440):
                            modify_shoot_key = True
                            modify_up_key, modify_down_key, modify_left_key, modify_right_key = False, False, False, False
                        else:
                            modify_up_key, modify_down_key, modify_left_key, modify_right_key, modify_shoot_key = False, False, False, False, False

                if self.pressed.get(pygame.K_ESCAPE):
                    self.in_main_menu = True
                    is_open = False

    def playScreen(self):
        is_open = True
        write_port_mode = False  # Variable pour indiquer si le mode d'écriture est activé
        write_ip_mode = False  # Variable pour indiquer si le mode d'écriture est activé
        
        error1 = False  # Variable pour indiquer si une erreur est survenue
        error2 = False  # Variable pour indiquer si une erreur est survenue
        error3 = False  # Variable pour indiquer si une erreur est survenue
        
        error1_time = None  # Initialisation du temps de l'erreur
        error2_time = None
        error3_time = None

        while is_open:

            self.screen.fill((0, 0, 0))  # Remplissage de l'écran en noir
            
            if error1 and error1_time and time.time() - error1_time < 3:  # Vérification du temps écoulé depuis l'erreur
                self.screen.blit(self.error1_surface, (self.width - self.error1_surface.get_width()-50, 35))
            
            if error2 and error2_time and time.time() - error2_time < 3:
                self.screen.blit(self.error2_surface, (self.width - self.error2_surface.get_width()-50, 35))
            
            if error3 and error3_time and time.time() - error3_time < 3:
                self.screen.blit(self.error3_surface, (self.width - self.error3_surface.get_width()-50, 35))

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))  # Affichage du titre
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,540,150,40])
            self.screen.blit(self.main_back, (self.width/2 - self.main_back.get_width()/2, 550))  # Affichage du bouton "Retour"

            self.screen.blit(self.port_text, (self.width/2 - self.port_text.get_width()/2, 340))  # Affichage du texte port

            self.screen.blit(self.ip_text, (self.width/2 - self.ip_text.get_width()/2, 260))  # Affichage du texte ip

            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,440,150,40])
            self.screen.blit(self.play_text, (self.width/2 - self.play_text.get_width()/2, 450))  # Affichage du texte "Rejoindre"

            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,490,150,40])
            self.screen.blit(self.create_text, (self.width/2 - self.create_text.get_width()/2, 500))  # Affichage du texte "Créer"

            # Affichage du rectangle pour saisir l'adresse IP / port
            if write_port_mode:
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 300/2,370,300,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 300/2,370,300,40])
            
            if write_ip_mode:
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 300/2,290,300,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 300/2,290,300,40])

            

            port_surface = self.smallfont.render(str(self.port) , True , (255,255,255))  # Création d'une surface de texte
            self.screen.blit(port_surface, (self.width/2 - port_surface.get_width()/2, 380))  # Affichage du texte port

            ip_surface = self.smallfont.render(str(self.ip) , True , (255,255,255))  # Création d'une surface de texte
            self.screen.blit(ip_surface, (self.width/2 - ip_surface.get_width()/2, 300))  # Affichage du texte ip

            pygame.display.update()  # Mise à jour de l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    self.stopGame()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # On enregistre que la touche est pressée
                    if write_port_mode:
                        if event.key == pygame.K_BACKSPACE:
                            self.port = str(self.port)[:-1]  # Suppression du dernier caractère du port
                        else:
                            self.port += event.unicode  # Ajout du caractère saisi au port
                    if write_ip_mode:
                        if event.key == pygame.K_BACKSPACE:
                            self.ip = str(self.ip)[:-1]
                        else:
                            self.ip += event.unicode
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Vérification des clics sur les différents boutons
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 540 <= event.pos[1] <= 580: #clic sur le bouton retour
                            self.is_running = True
                            is_open = False
                            self.status = "menu"
                        if self.width/2 - 300/2 <= event.pos[0] <= self.width/2 - 300/2 + 300 and 370 <= event.pos[1] <= 410: #clic sur le champ port
                            write_port_mode = True  # Activation du mode d'écriture
                        else: #clic autre part
                            write_port_mode = False  # Désactivation du mode d'écriture
                        if self.width/2 - 300/2 <= event.pos[0] <= self.width/2 - 300/2 + 300 and 290 <= event.pos[1] <= 330: #clic sur le champ ip
                            write_ip_mode = True  # Activation du mode d'écriture
                        else: #clic autre part
                            write_ip_mode = False
                            
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 440 <= event.pos[1] <= 480: #clic sur le bouton rejoindre
                            self.port = int(self.port)
                            response = requests.get(f"http://{self.ip}:5555/server/{self.port}")
                            if response.status_code == 200:
                                self.client_socket = connect_to_server(self.port, self.ip)
                                self.connected = True
                                self.num = 2
                                is_open = False
                                self.is_running = True
                                self.status = "ingame"
                                self.tanks = [self.createMyTank(position = (self.width - 200, self.height - 200), direction="gauche", angle=135.), self.createEnemyTank(position=(100, 100), direction="droite", angle=0)]
                                self.in_game = True
                                error1 = False
                                error2 = False
                                error3 = False
                                error1_time = None
                                error2_time = None
                                error3_time = None
                            elif response.status_code == 400:
                                error1 = True
                                error2 = False
                                error3 = False
                                error1_time = time.time()
                                error2_time = None
                                error3_time = None
                                print("[CLIENT] Server not found on port " + str(self.port) + " and IP " + self.ip)
                            else:
                                error1 = False
                                error2 = True
                                error3 = False
                                error1_time = None
                                error2_time = time.time()
                                error3_time = None
                                print("[CLIENT] Error while connecting to server on port " + str(self.port) + " and IP " + self.ip)
                                        
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 490 <= event.pos[1] <= 530: #clic sur le bouton créer
                            print("[CLIENT] Creating server on port " + str(self.ip) + ":" + str(self.port))
                            self.port = int(self.port)
                            response = requests.post(f"http://{self.ip}:5555/server/{self.port}")
                            if response.status_code == 200:
                                self.client_socket = connect_to_server(self.port, self.ip)
                                self.connected = True
                                self.num = 1
                                is_open = False
                                self.is_running = True                                
                                self.status = "ingame"
                                self.tanks = [self.createMyTank()]
                                self.in_game = True
                                error1 = False
                                error2 = False
                                error3 = False
                                error1_time = None
                                error2_time = None
                                error3_time = None
                            elif response.status_code == 400:
                                error1 = False
                                error2 = False
                                error3 = True
                                error1_time = None
                                error2_time = None
                                error3_time = time.time()
                                print("[CLIENT] Server already exists on port " + str(self.port))
                            else:
                                error1 = False
                                error2 = True
                                error3 = False
                                error1_time = None
                                error2_time = time.time()
                                error3_time = None
                                print("[CLIENT] Error while creating server on port " + str(self.port) + " and IP " + self.ip)

                if self.pressed.get(pygame.K_ESCAPE):
                    self.in_main_menu = True
                    is_open = False
                    
    def stopGame(self):
        self.is_running = False  # Mise à jour de l'état de fonctionnement du jeu
        pygame.quit()  # Arrêt de Pygame
        close_connection(self.client_socket)  # Fermeture de la connexion
        print("Game stopped")  # Message d'arrêt du jeu
        return None
    
    def createMyTank(self, position=(100, 100), direction="droite", angle=0):
        tank = Tank(self, initial_position=position, rotation=direction)
        return (tank, TopTank(self, tank, angle=angle))
    
    def createEnemyTank(self, position=(-1, -1), direction="droite", angle=135.):
        if position == (-1, -1):
            position = (self.width - 200, self.height - 200)
        tank = Tank(self, initial_position=position, rotation=direction, image_path="assets/tank2.png")
        return (tank, TopTank(self, tank, angle=angle, image_path="assets/toptank2.png"))
# Importation de la classe Game depuis le module game dans le package modules
from modules.game import Game

# Importation du module ctypes pour interagir avec les bibliothèques C
import ctypes
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

# Création d'un objet pour interagir avec la bibliothèque user32.dll de Windows
usr32 = ctypes.windll.user32

# Définition des constantes pour le jeu
SCREEN_WIDTH = usr32.GetSystemMetrics(0)  # Obtention de la largeur de l'écran en pixels
SCREEN_HEIGHT = usr32.GetSystemMetrics(1)  # Obtention de la hauteur de l'écran en pixels
FPS = 1000  # Nombre de frames par seconde
TITLE = "TANKETTE"  # Titre de la fenêtre du jeu
BACKGROUND_PATH = "assets/background.png"  # Chemin vers l'image de fond du jeu

# Initialisation du jeu avec les constantes définies précédemment
game = Game(title=TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, fps=FPS, background_path=BACKGROUND_PATH, debug=False, diagonales=False)

# Lancement du jeu
game.game()
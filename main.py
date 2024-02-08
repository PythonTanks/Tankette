from modules.game import Game

# Définition des constantes
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
TITLE = "TANKETTE"
BACKGROUND_PATH = "assets/background.png"

# Intialisation du jeu
game = Game(TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_PATH)

# Lancement du jeu
game.start()
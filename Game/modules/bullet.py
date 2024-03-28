import math
from modules.movable import Movable  # Importation de la classe parente Movable

class Bullet(Movable):
    def __init__(self, game, velocity=20, angle=0, start=(0, 0)):
        # Appel du constructeur de la classe parente (Movable)
        super().__init__(game, "assets/bullet.png", start, (10/1080, 30/1920), velocity, 270-angle)
        
        # Angle de déplacement de la balle
        self.angle = angle
        # Position de départ de la balle
        self.start = start
        self.start = (self.start[0] - 45, self.start[1] - 45)  # Ajustement de la position de départ
        # Rectangle englobant l'image de la balle
        self.rect = self.image.get_rect(center=start)
        # Vitesse de déplacement de la balle
        self.velocity = velocity
        # Référence à l'instance de la classe Game
        self.game = game

        self.rebond = 0
        
        # Calcul des composantes dx et dy du déplacement de la balle
        self.dx = math.cos(math.radians(self.angle)) * self.velocity  # Calcul de la composante horizontale
        self.dy = math.sin(math.radians(self.angle)) * self.velocity  # Calcul de la composante verticale
        
        # Rotation de l'image de la balle en fonction de l'angle de déplacement
        self.spriteRotate(self.image_custom)  # Rotation de l'image de la balle

    def update(self):
        # Si le jeu n'est pas en pause
        if not self.game.freeze:
            # Déplacement de la balle
            self.move(self.dx, self.dy, self.image_custom)  # Déplacement de la balle
            
        # Si la balle sort de l'écran, elle est supprimée
        myWall = self.collision()
        if myWall != -1:
            if self.rebond == 2:
                self.kill()  # Suppression de la balle si elle sort de l'écran
            else:
                self.rebond += 1
                
                
            
        # Si la balle touche un tank, elle est supprimée
        for tank in self.game.tanks:
            if self.rect.colliderect(tank[0].rect):
                self.kill()  # Suppression de la balle si elle touche un tank
                tank[0].life -= 10  # Réduction des points de vie du tank touché
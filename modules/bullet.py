import math
from modules.movable import Movable

class Bullet(Movable):
    def __init__(self, game, velocity=20, angle=0, start=(0, 0)):
        # Appel du constructeur de la classe parente (Movable)
        super().__init__(game, "assets/bullet.png", start, (10, 30), velocity, 270-angle)
        
        # Angle de déplacement de la balle
        self.angle = angle
        # Position de départ de la balle
        self.start = start
        self.start = (self.start[0] - 45, self.start[1] - 45)
        # Rectangle englobant l'image de la balle
        self.rect = self.image.get_rect(center=start)
        # Vitesse de déplacement de la balle
        self.velocity = velocity
        # Référence à l'instance de la classe Game
        self.game = game
        
        # Calcul des composantes dx et dy du déplacement de la balle
        self.dx = math.cos(math.radians(self.angle)) * self.velocity
        self.dy = math.sin(math.radians(self.angle)) * self.velocity
        
        self.spriteRotate(self.image_custom)

    def update(self):
        if not self.game.freeze:
            # Déplacement de la balle
            self.move(self.dx, self.dy, self.image_custom)
            
        # Si la balle sort de l'écran, elle est supprimée
        if self.rect.x < -30 or self.rect.x > self.game.width or self.rect.y < -30 or self.rect.y > self.game.height:
            self.kill()
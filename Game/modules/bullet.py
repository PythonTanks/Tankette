import math
from modules.movable import Movable  # Importation de la classe parente Movable

class Bullet(Movable):
    def __init__(self, game, velocity=20, angle=0, start=(0, 0)):
        self.angle = angle
        # Appel du constructeur de la classe parente (Movable)
        super().__init__(game, "assets/bullet.png", start, (10/1080, 30/1920), velocity, 270 - self.angle)
        
        # Angle de déplacement de la balle
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
        
        self.cos_angle = math.cos(math.radians(angle))
        self.sin_angle = math.sin(math.radians(angle))
        # Calcul des composantes dx et dy du déplacement de la balle
        self.dx = math.cos(math.radians(angle)) * self.velocity  # Calcul de la composante horizontale
        self.dy = math.sin(math.radians(angle)) * self.velocity  # Calcul de la composante verticale
        
        # Rotation de l'image de la balle en fonction de l'angle de déplacement
        self.spriteRotate(self.image_custom)  # Rotation de l'image de la balle

    def update(self):
        # Si le jeu n'est pas en pause
        if not self.game.freeze:
            # Déplacement de la balle
            self.move(self.dx, self.dy, self.image_custom)  # Déplacement de la balle
            
        # Si la balle sort de l'écran, elle est supprimée
        myWall = self.collision()
        if self in self.game.tanks[0][0].all_projectiles:
            if myWall[0] == True and (myWall[1] != -1):
                if self.rebond == 2:
                    self.kill()  # Suppression de la balle si elle atteint 3 rebonds
                else:
                    self.rebond += 1
                    if myWall[1] == "limite":
                        # On cherche a quel bord de l'écran la balle a touché
                        # Si elle touche le haut ou le bas, on inverse la composante verticale du déplacement
                        if self.rect.y < 0 or self.rect.y > self.game.height - self.rect.height:
                            self.dy = -self.dy
                            self.sin_angle = -self.sin_angle
                            self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                            self.newAngle(self.angle)
                            self.spriteRotate(self.angle)                            
                        # Si elle touche la gauche ou la droite, on inverse la composante horizontale du déplacement
                        if self.rect.x < 0 or self.rect.x > self.game.width - self.rect.width:
                            self.dx = -self.dx
                            self.cos_angle = -self.cos_angle
                            self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                            self.newAngle(self.angle)
                            self.spriteRotate(self.angle)
                    if myWall[1] == "tank":
                                self.kill()  # Suppression de la balle si elle touche un tank
                                myWall[2].life -= 10  # Réduction des points de vie du tank touché
                    if myWall[1] == "wall":
                        # On cherche a quel partie du mur la balle a touché
                        rect_wall = myWall[2].rect
                        # Si elle touche le haut du mur et que la balle va vers le bas, on inverse la composante verticale du déplacement
                        # On vérfie d'abord toutes les conditions que la balle confirmer pour etre qu'elle touche la partie haute du mur
                        if self.rect.bottom < rect_wall.bottom - rect_wall.height/2 and self.dy > 0:
                            self.dy = -self.dy
                            self.sin_angle = -self.sin_angle
                            self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                            self.newAngle(self.angle)
                            self.spriteRotate(self.angle)
                        # Si elle touche le bas du mur et que la balle va vers le haut, on inverse la composante verticale du déplacement
                        # On vérfie d'abord toutes les conditions que la balle confirmer pour etre qu'elle touche la partie basse du mur
                        elif self.rect.top > rect_wall.top + rect_wall.height/2 and self.dy < 0:
                            self.dy = -self.dy
                            self.sin_angle = -self.sin_angle
                            self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                            self.newAngle(self.angle)
                            self.spriteRotate(self.angle)
                        # Si elle touche la gauche du mur et que la balle va vers la droite, on inverse la composante horizontale du déplacement
                        # On vérfie d'abord toutes les conditions que la balle confirmer pour etre qu'elle touche la partie gauche du mur
                        elif self.rect.right < rect_wall.right - rect_wall.width/2 and self.dx > 0:
                            self.dx = -self.dx
                            self.cos_angle = -self.cos_angle
                            self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                            self.newAngle(self.angle)
                            self.spriteRotate(self.angle)
                        # Si elle touche la droite du mur et que la balle va vers la gauche, on inverse la composante horizontale du déplacement
                        # On vérfie d'abord toutes les conditions que la balle confirmer pour etre qu'elle touche la partie droite du mur
                        elif self.rect.left > rect_wall.left + rect_wall.width/2 and self.dx < 0:
                            self.dx = -self.dx
                            self.cos_angle = -self.cos_angle
                            self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                            self.newAngle(self.angle)
                            self.spriteRotate(self.angle)
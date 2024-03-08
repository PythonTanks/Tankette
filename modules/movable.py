from modules.gameObject import GameObject

class Movable(GameObject):
    # Le constructeur de la classe Movable
    def __init__(self, game, image_path, initial_position=(0, 0), dimensions=(150, 150), velocity=5, custom_rotate=0):
        # Appel du constructeur de la classe parente (GameObject)
        super().__init__(game, image_path, initial_position, dimensions, custom_rotate)
        # Initialisation de la vitesse de l'objet
        self.velocity = velocity
        self.image_pathmovable = image_path
    
    # Méthode pour faire tourner l'image de l'objet
    def spriteRotate(self, rotate):
        # Rotation de l'image de l'objet en fonction de la direction spécifiée
        self.image = rotate
        
    def collision(self, dx, dy):
        # Si l'objet est en collision avec un mur
        if self.rect.x + dx < 0 or self.rect.x + dx > self.game.width - self.rect.width or self.rect.y + dy < 0 or self.rect.y + dy > self.game.height - self.rect.height:
            return True
        return False

    # Méthode pour déplacer l'objet
    def move(self, dx, dy, rotate):
        # Modification de la position de l'objet en fonction des déplacements dx et dy
        if not self.collision(dx, dy) or ("bullet" in self.image_pathmovable):
            self.rect.x += dx
            self.rect.y += dy
        self.spriteRotate(rotate)
        
    def spriteRotateDirection(self, direction):
        if direction == "haut":
            self.spriteRotate(self.image_up)
        elif direction == "bas":
            self.spriteRotate(self.image_down)
        elif direction == "droite":
            self.spriteRotate(self.image_right)
        elif direction == "gauche":
            self.spriteRotate(self.image_left)
        elif direction == "haut_droit":
            self.spriteRotate(self.image_up_right)
        elif direction == "haut_gauche":
            self.spriteRotate(self.image_up_left)
        elif direction == "bas_droit":
            self.spriteRotate(self.image_down_right)
        elif direction == "bas_gauche":
            self.spriteRotate(self.image_down_left)
        else:
            self.spriteRotate(self.image_custom)
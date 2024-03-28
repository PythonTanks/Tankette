from modules.gameObject import GameObject  # Importe la classe GameObject du module gameObject

# Classe représentant un objet mobile, héritant de GameObject
class Movable(GameObject):
    # Le constructeur de la classe Movable
    def __init__(self, game, image_path, initial_position=(0, 0), dimensions=(150, 150), velocity=5, custom_rotate=0):
        # Appel du constructeur de la classe parente (GameObject)
        super().__init__(game, image_path, initial_position, dimensions, custom_rotate)
        # Initialisation de la vitesse de l'objet
        self.velocity = velocity
        # Chemin de l'image de l'objet mobile
        self.image_pathmovable = image_path
        
    # Méthode pour gérer les collisions avec les bords de l'écran
    def collision(self):
        # Vérifie si l'objet est en collision avec un mur
        if self.rect.x < 0 or self.rect.x > self.game.width - self.rect.width or self.rect.y < 0 or self.rect.y > self.game.height - self.rect.height:
            return (True, "limite", None)
        if len(self.game.tanks) > 0:
            if len(self.game.tanks) > 1:
                if self.rect.colliderect(self.game.tanks[1][0].rect):
                    return (True, "tank", self.game.tanks[1][0])
            if "bullet" in self.image_pathmovable:
                if self.rect.colliderect(self.game.tanks[0][0].rect):
                    return (True, "tank", self.game.tanks[0][0])
        wall = self.rect.collidelist(self.game.walls)
        if wall != -1:
            return (True, "wall", self.game.walls[wall])
        return (False, None, None)

    # Méthode pour déplacer l'objet
    def move(self, dx, dy, rotate):
        # Modification de la position de l'objet en fonction des déplacements dx et dy, tout en gérant les collisions
        self.rect.x += dx
        self.rect.y += dy
        if self.collision()[0] and not ("bullet" in self.image_pathmovable):  # Vérifie s'il y a une collision avec un mur ou si l'objet est un projectile
            self.rect.x -= dx
            self.rect.y -= dy
        if not "bullet" in self.image_pathmovable:
            self.spriteRotate(rotate)  # Appel de la méthode pour orienter l'image de l'objet en fonction de sa direction
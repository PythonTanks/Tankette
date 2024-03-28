try:
    from modules.gameObject import GameObject  # Importe la classe GameObject du module gameObject
except ModuleNotFoundError:
    from gameObject import GameObject

def gen(name : str):
    myMap = open(f"../maps/{name}.txt", "a")
    for lines in range(22):
        myMap.write("-"*38+"\n")
    myMap.close()
    return None

def getWalls(game, nameFile : str, image):
    myMap = open(f"maps/{nameFile}.txt", "r")
    myWalls = []
    for i, lines in enumerate(myMap.readlines()):
        for j, value in enumerate(lines):
            if value=="|":
                wall = GameObject(game, image_path=image, initial_position=(j*50/1080*game.height, i*50/1920*game.width), dimensions=(50/game.height, 50/game.width), custom_rotate=0, need_rotate=False)
                myWalls.append(wall)
    return myWalls

if __name__ == "__main__":
    gen("map1")
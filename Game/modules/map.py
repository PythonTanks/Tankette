import pygame
from modules.gameObject import GameObject  # Importe la classe GameObject du module gameObject

def gen(name : str):
    myMap = open(f"../maps/{name}.txt", "a")
    for lines in range(10):
        myMap.write("-"*19+"\n")
    myMap.close()
    return None

def getWalls(game, nameFile : str, image):
    print(1)
    myMap = open(f"maps/{nameFile}.txt", "r")
    myWalls = []
    print(2)
    for i, lines in enumerate(myMap.readlines()):
        print(i)
        for j, value in enumerate(lines):
            print(j)
            if value=="|":
                wall = GameObject(game, image_path=image, initial_position=(j*100/1080*game.height, i*100/1920*game.width), dimensions=(100/1080, 100/1920), custom_rotate=0, need_rotate=False)
                myWalls.append(wall)
    print("finish")
    return myWalls

if __name__ == "__main__":
    gen("map1")
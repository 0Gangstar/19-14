import pygame  # загружаю нужные библиотеки
import sys
import os


def load_image(name, colorkey=None):  # класс для загрузки изображения
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image2 = pygame.image.load(fullname)
    return image2


g = load_image("grass_night.png")
empty = load_image("empty.png")
num = load_image("empty2.png")
j = load_image("junk_can.png")
tree = load_image("tree.png")
leather_stuff = load_image('leatherstuff.png')
s = load_image('stone.png')
g2 = load_image("grass_night2.png")
sign = load_image('Signs.png')
pol = [empty, g, g2]
barriers = [leather_stuff, tree, j, num, s, sign]

sprites_for_hero_animation = [load_image("main1_left.png"), load_image("main1_right.png"),
                              load_image("main4_walk.png"), load_image("main4.png"),
                              load_image("main4_walk2.png"), load_image("main4.png"),
                              load_image("main5_walk.png"), load_image("main5.png"),
                              load_image("main5_walk2.png"), load_image("main5.png"),
                              load_image("main3_right.png"), load_image("main3_left.png")]

world = [[[j, g2], [s, g2], g, g2, [s, g], g2, g, g2, g2, [sign, g], [j, g2], g, [s, g2], g2, [s, g], g, g, g2, g2, g, [s, g], g2, g, [sign, g2], g, g2, g, g2, g, g, g, g2, [j, g], g, [j, g2], g, g, [j, g], g, [s, g], g2, g, [s, g], g, [j, g2], g, g, g2],
         [g2, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g], g, g, g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [[s, g], g2, g2, [s, g], g, g2, g, g2, g2, [sign, g], g2, g2, g, [sign, g], g, g2, g2, g, g2, g2, [s, g], g, g2, g, g, g2, g, g2, g2, g2, g2, g, [s, g], g2, [s, g], g, g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, g, g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g2, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [[s, g], g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, g, g, g, g, g2, g, g ,g, g2, g, g, g, g],
         [g, g2, g, g2, g2, g2, g, g, g, g, g2, g2, g, g2, g2, g2, g2, g2, g, g2, g2, g2, g, g2, g, g2, g2, g, g2, g2, g2, g, g2, g2, g2, g2, g, g2, g2, g, g, g2, g, g2, g, g, g, g, g2, g2, g, g, g, g, g, g2, g, g2, g, g ,g, g, g, g, g, g],
         [g, g2, g, g2, g2, g2, g, g, g, g, g2, g2, g, g2, g2, g2, g2, g2, g, g2, g2, g2, g, g2, g, g2, g2, g, g2, g2, g2, g, g2, g2, g2, g2, g, g2, g2, g, g, g2, g, g2, g, g, g, g, g2, g2, g, g, g, g, g, g2, g, g2, g, g ,g, g, g, g, g, g],
         [[s, g], g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [s, g], g2, [s, g2], g, g, [j, g], [sign, g], [j, g2], g, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, g, g, [s, g2], g, g, [j, g], g, g2, g2, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [[sign, g], g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, g, g, [s, g2], g, g, [j, g], g, g2, g, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, g2, g, [s, g], g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [[j, g], g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, g2, g, [j, g], g, sign, g2, g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g2, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [s, g], g, g2, g, [sign, g], g2, g, g2, g, [s, g], g, [j, g2], [s, g], g, g, [s, g] ,g, g, g, g2, g, g],
         [g2, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g2, [j, g], g, [j, g2], g, g, g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g, g2, g2, g, g2, g2, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, [s, g], g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [[s, g], g, g2, g2, g, [s, g], g, [sign, g], g, g2, g2, [s, g], g, [sign, g], g2, g2, g, g2, g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g2, [s, g2], g, g, [j, g], g, g2, g2, g, g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [g2, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, g2, g, g, g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g2, g2, g, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g2, [j, g], g2, [j, g], g2, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [g2, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g2, [s, g2], g, g, [j, g], g, [j, g2], g, g, g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [g2, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g], g, g, g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [[s, g], g2, g2, [s, g], g, g2, g, g2, g2, [sign, g], g2, g2, g, [sign, g], g, g2, g2, g, g2, g2, [s, g], g, g2, g, g, g2, g, g2, g2, g2, g2, g, [s, g], g2, [s, g], g, g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, g, g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g2, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [[s, g], g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, g, g, g, g, g2, g, g ,g, g2, g, g, g, g],
         [g, g2, g, g2, g2, g2, g, g, g, g, g2, g2, g, g2, g2, g2, g2, g2, g, g2, g2, g2, g, g2, g, g2, g2, g, g2, g2, g2, g, g2, g2, g2, g2, g, g2, g2, g, g, g2, g, g2, g, g, g, g, g2, g2, g, g, g, g, g, g2, g, g2, g, g ,g, g, g, g, g, g],
         [g, g2, g, g2, g2, g2, g, g, g, g, g2, g2, g, g2, g2, g2, g2, g2, g, g2, g2, g2, g, g2, g, g2, g2, g, g2, g2, g2, g, g2, g2, g2, g2, g, g2, g2, g, g, g2, g, g2, g, g, g, g, g2, g2, g, g, g, g, g, g2, g, g2, g, g ,g, g, g, g, g, g],
         [[s, g], g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [s, g], g2, [s, g2], g, g, [j, g], [sign, g], [j, g2], g, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, g, g, [s, g2], g, g, [j, g], g, g2, g2, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [[sign, g], g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, g, g, [s, g2], g, g, [j, g], g, g2, g, g, g, [j, g], g, [sign, g], g, g ,g, [j, g], g, [j, g2], g, g],
         [g, g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, g2, g, [s, g], g, [j, g], g, [sign, g2], g, g ,g, [j, g], g, [j, g2], g, g],
         [[j, g], g, g2, g2, g, g2, g, [s, g], g, g, g2, g2, g, [sign, g], g2, g2, g, [s, g], g, g, g2, g2, g, g2, g, g, g2, [sign, g], g2, [tree, g], g2, [tree, g], g2, [tree, g], g2, g2, g2, [s, g], g2, g, g, [j, g2], g, g2, [j, g], g, [s, g2], g, g, [j, g], g, [j, g2], g, g2, g, [j, g], g, sign, g2, g, g ,g, [j, g], g, [j, g2], g, g]]

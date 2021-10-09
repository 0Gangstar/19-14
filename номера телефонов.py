import pygame  # загружаю нужные библиотеки
import sys
import os
from math import floor, ceil


def load_image(name, colorkey=None):  # класс для загрузки изображения
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image2 = pygame.image.load(fullname)
    return image2

def render(screen_start_x, screen_start_y, screen_end_x, screen_end_y):
    screen_line = -1
    screen_sprites = []
    x1 = floor(screen_start_x / 64)
    y1 = floor(screen_start_y / 64)
    x2 = screen_start_x % 64
    y2 = screen_start_y % 64
    for line in range(0, ceil(screen_end_y / 64)):
        if line >= y1:
            screen_line += 1
            screen_sprites.append([])
        for num in range(0, ceil(screen_end_x / 64)):
            obj = world[line][num]
            if line >= y1 and num >= x1:
                if type(obj) == list:
                    Sprite(obj[0], num * 64 - x1 * 64 - x2, line * 64 - y1 * 64 - y2, barrier_sprites)
                    screen_sprites[screen_line].append(Sprite(obj[1], num * 64 - x1 * 64 - x2, line * 64 - y1 * 64 - y2, all_sprites))
                elif obj in pol:
                    screen_sprites[screen_line].append(Sprite(obj, num * 64 - x1 * 64 - x2, line * 64 - y1 * 64 - y2, all_sprites))
            elif type(obj) == list:
                size = obj[0].get_rect().size
                if num * 64 + size[0] >= screen_start_x and line * 64 + size[1] >= screen_start_y:
                    Sprite(obj[0], num * 64 - x1 * 64 - x2, line * 64 - y1 * 64 - y2, barrier_sprites)
    return screen_sprites


class Sprite(pygame.sprite.Sprite):  # класс для создания спрайтов на экране
    def __init__(self, image, x, y, *group):  # с помощью супера все созданные спрайты скидываю в группу спрайтов
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.sprite_size = self.image.get_size()

    def update(self, x, y):  # обновляет спрайт при необходимости
        self.rect.x += x
        self.rect.y += y


    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_sprite_size(self):
        return self.sprite_size

class Hero(Sprite):
    def __init__(self, image, x, y, *group):
        super().__init__(image, x, y, *group)
        self.x = x
        self.y = y

    def set_image(self, image):
        self.image = image

class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.rect.y + spr.sprite_size[1]

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

class Camera:
    def __init__(self, x, y, x2, y2):
        self.screen_start_x = x
        self.screen_start_y = y
        self.screen_end_x = x2
        self.screen_end_y = y2

    def move_left(self, screen_sprites):
        self.screen_start_x -= velocity
        self.screen_end_x -= velocity
        all_sprites.update(velocity, 0)
        barrier_sprites.update(velocity, 0)
        print(len(barrier_sprites))
        if screen_sprites[0][-1].get_x() + self.screen_start_x > self.screen_end_x:
            for i in range(len(screen_sprites)):
                screen_sprites[i][-1].kill()
                screen_sprites[i].pop(-1)
        # Добавить удаление препятствий
        if screen_sprites[0][0].get_x() + self.screen_start_x > self.screen_start_x:
            cell_sx, cell_sy = floor(self.screen_start_x / 64), floor(self.screen_start_y / 64)
            for line in range(0, ceil(self.screen_end_y / 64)):
                for num in range(0, ceil(self.screen_start_x / 64)):
                    sprite = world[line][num]
                    if type(sprite) == list:
                        size = sprite[0].get_rect()
                        if num * 64 + size[2] >= self.screen_start_x and line * 64 + size[3] >= self.screen_start_y:
                            if num * 64 + size[2] - velocity <= self.screen_start_x:
                                Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, barrier_sprites)
            for i in range(len(screen_sprites)):
                if type(world[cell_sy + i][cell_sx]) is not list:
                    screen_sprites[i].insert(0, Sprite(world[cell_sy + i][cell_sx], screen_sprites[i][0].get_x() - 64, screen_sprites[i][0].get_y(), all_sprites))
                else:
                    screen_sprites[i].insert(0, Sprite(world[cell_sy + i][cell_sx][1], screen_sprites[i][0].get_x() - 64, screen_sprites[i][0].get_y(), all_sprites))

    def move_right(self, screen_sprites):
        self.screen_start_x += velocity
        self.screen_end_x += velocity
        all_sprites.update(-velocity, 0)
        barrier_sprites.update(-velocity, 0)
        if screen_sprites[0][0].get_x() + self.screen_start_x + screen_sprites[0][0].get_sprite_size()[0] < self.screen_start_x:
            for i in range(len(screen_sprites)):
                screen_sprites[i][0].kill()
                screen_sprites[i].pop(0)
        # Добавить удаление препятствий
        if screen_sprites[0][-1].get_x() + self.screen_start_x + screen_sprites[0][-1].get_sprite_size()[0] < self.screen_end_x:
            cell_sx, cell_sy = floor(self.screen_start_x / 64), floor(self.screen_start_y / 64)
            cell_ex, cell_ey = floor(self.screen_end_x / 64), floor(self.screen_end_y / 64)
            print(cell_ex)
            # for line in range(0, ceil(self.screen_end_y / 64)):
            #     for num in range(0, ceil(self.screen_start_x / 64)):
            #         sprite = world[line][num]
            #         if type(sprite) == list:
            #             size = sprite[0].get_rect()
            #             if num * 64 + size[2] >= self.screen_start_x and line * 64 + size[3] >= self.screen_start_y:
            #                 if num * 64 + size[2] - velocity <= self.screen_start_x: #
            #                     Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, barrier_sprites)
            #  добавить добавление припятствий
            for i in range(len(screen_sprites)):
                # print(len(screen_sprites[0]))
                if type(world[cell_sy + i][cell_ex]) is not list:
                    screen_sprites[i].append(Sprite(world[cell_sy + i][cell_ex], screen_sprites[i][-1].get_x() + 64, screen_sprites[i][0].get_y(), all_sprites))
                else:
                    screen_sprites[i].append(Sprite(world[cell_sy + i][cell_ex][1], screen_sprites[i][-1].get_x() + 64, screen_sprites[i][0].get_y(), all_sprites))


if __name__ == '__main__':
    pygame.init()
    all_sprites = YAwareGroup()
    barrier_sprites = YAwareGroup()
    size = 984, 576
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    fps = 60
    velocity = int(320 / fps)
    screen_start_x = 600
    screen_start_y = 0
    screen_end_x = screen_start_x + size[0]
    screen_end_y = screen_start_y + size[1]
    camera = Camera(screen_start_x, screen_start_y, screen_end_x, screen_end_y)
    grass_night = load_image("grass_night.png")
    empty = load_image("empty.png")
    junk_can = load_image("junk_can.png")
    tree = load_image("tree.png")
    leather_stuff = load_image('leatherstuff.png')
    pol = [empty, grass_night]
    barriers = [leather_stuff, tree, junk_can]
    far_nums = []
    world = [[empty, [leather_stuff, grass_night], grass_night, grass_night, [leather_stuff,
              grass_night], empty, grass_night, empty, empty, [junk_can, grass_night], [junk_can, grass_night],
              grass_night, [junk_can, grass_night], empty, [junk_can, empty], [junk_can, empty], grass_night, grass_night, empty,
              empty, grass_night, empty, grass_night, empty, [junk_can, grass_night], grass_night, grass_night, grass_night,
              grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, [junk_can,
              empty], grass_night, grass_night, [junk_can, grass_night], grass_night, [junk_can,
              empty], grass_night, grass_night, [junk_can, grass_night], grass_night, [junk_can,
              empty], grass_night, grass_night, empty],
             [grass_night, grass_night, empty, empty, empty, grass_night, empty, [leather_stuff, grass_night], empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, empty, empty, [junk_can, grass_night],
              grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, [junk_can, grass_night],
              grass_night, [junk_can, grass_night], grass_night, grass_night, [junk_can, grass_night], grass_night, [junk_can,
              empty], grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, [junk_can,
              empty], grass_night, grass_night ,grass_night, [junk_can, grass_night], grass_night, [junk_can,
              empty], grass_night, grass_night],
            [grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, [leather_stuff, grass_night], empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night,
             grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night],
             grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, [junk_can, empty], grass_night, grass_night],
             [grass_night, grass_night, grass_night, [junk_can, empty], empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night,
              grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night,
              empty, grass_night, grass_night, grass_night, grass_night, empty, grass_night],
             [grass_night, grass_night, [junk_can, empty], [junk_can, grass_night], [junk_can, grass_night], empty,
              grass_night, empty, grass_night, empty, [junk_can, grass_night], grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, [junk_can, grass_night], empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night,
              grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night,
              grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, junk_can, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night,
              grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night,
              grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, grass_night, grass_night, grass_night, empty, [junk_can,
              grass_night], empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night,
              grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night,
              grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, junk_can, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night],
             [grass_night, grass_night, grass_night, empty, [junk_can, empty], grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, empty, [junk_can, empty],
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty, grass_night, empty,
              grass_night, empty, grass_night, empty, grass_night, empty, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, grass_night, [junk_can, grass_night], grass_night, grass_night, grass_night, grass_night, grass_night]]
    screen_sprites = render(screen_start_x, screen_start_y, screen_end_x, screen_end_y)
    print(len(screen_sprites[0]))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(all_sprites)
                running = False
        pygame.event.pump()  # нужно, чтобы при зажатой мыши действие происходило несколько раз
        if pygame.key.get_pressed()[pygame.K_a]:
            camera.move_left(screen_sprites)
        elif pygame.key.get_pressed()[pygame.K_d]:
            camera.move_right(screen_sprites)
        clock.tick(fps)
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        barrier_sprites.draw(screen)
        pygame.display.flip()



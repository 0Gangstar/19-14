import pygame  # загружаю нужные библиотеки
from math import floor, ceil
import sys
import os
from Location1 import StartLocation
from Variables import *
# Сдеалть хитбоксы и сделать,  чтобы при движение наверх, при столкновении, герой начинал  двигаться в строны, если не в самом низу барьера


def load_image(name, colorkey=None):  # класс для загрузки изображения
    fullname = os.path.join('pythongame/data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image2 = pygame.image.load(fullname)
    return image2


def render(start_x, start_y, end_x, end_y):
    screen_line = -1
    screen_sprites = []
    screen_sprites2 = []
    x1 = floor(start_x / 64)
    y1 = floor(start_y / 64)
    x2 = start_x % 64
    y2 = start_y % 64
    for line in range(0, ceil(end_y / 64)):
        if line >= y1:
            screen_line += 1
            screen_sprites.append([])
        for num in range(0, ceil(end_x / 64)):
            obj = location.location[line][num]
            if line >= y1 and num >= x1:
                if type(obj) == list:
                    screen_sprites2.append(Sprite(obj[0], num * 64 - x1 * 64 - x2, line * 64 - y1 * 64 - y2, location.width_of_base[obj[0]], barrier_sprites))
                    screen_sprites[screen_line].append(Sprite(obj[1], num * 64 - x1 * 64 - x2, line * 64 - y1 * 64 - y2, 0, all_sprites))
                elif obj in location.pol:
                    screen_sprites[screen_line].append(Sprite(obj, num * 64 - x1 * 64 - x2, line * 64 - y1 * 64 - y2, 0, all_sprites))
            elif type(obj) == list:
                size = obj[0].get_rect().size
                if num * 64 + size[0] >= start_x and line * 64 + size[1] >= start_y:
                    screen_sprites2.append(Sprite(obj[0], num * 64 - x1 * 64 - x2, line * 64 - y1 * 64 - y2, location.width_of_base[obj[0]], barrier_sprites))
    return screen_sprites, screen_sprites2


class Sprite(pygame.sprite.Sprite):  # класс для создания спрайтов на экране
    def __init__(self, image, x, y, base, *group):  # с помощью супера все созданные спрайты скидываю в группу спрайтов
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.sprite_size = self.image.get_size()
        self.width_of_base = base

    def update(self, x, y):  # обновляет спрайт при необходимости
        self.rect.x += x
        self.rect.y += y

    def get_image(self):
        return self.image

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_sprite_size(self):
        return self.sprite_size


class Hero(Sprite):
    def __init__(self, image, x, y, base, *group):
        super().__init__(image, x, y, base, *group)
        self.x = x
        self.y = y
        self.sprite_now = 0
        self.hor_animation_speed = 2 / 32
        self.ver_animation_speed = 3 / 32
        self.able_to_move = True
        self.hitbox_pos = (self.x + 3 * 4, self.y + 27 * 4)
        self.width_of_base = base

    def set_image(self, image, now):
        self.image = image
        self.sprite_now = now

    def move_right(self):
        for sprite in pygame.sprite.spritecollide(hitbox, screen_sprites2, False):
            if pygame.sprite.collide_mask(hitbox, sprite):
                sprite_pos = sprite.get_y() + sprite.get_sprite_size()[1]
                if sprite_pos - sprite.width_of_base < hitbox.get_y() + hitbox.get_sprite_size()[1] < sprite_pos + hitbox.get_sprite_size()[1]:
                    self.set_image(hero_right, 3)
                    while pygame.sprite.collide_mask(hitbox, sprite):
                        camera.move_left(screen_sprites, 1)
                    self.able_to_move = False
                    break
        if self.able_to_move is False:
            self.able_to_move = True
        else:
            self.sprite_now += self.hor_animation_speed
            if self.sprite_now < 2:
                self.sprite_now = 2
            elif self.sprite_now >= 6:
                self.sprite_now = 2
            self.set_image(sprites_for_hero_animation[int(self.sprite_now)], self.sprite_now)

    def move_left(self):
        for sprite in pygame.sprite.spritecollide(hitbox, screen_sprites2, False):
            if pygame.sprite.collide_mask(hitbox, sprite):
                sprite_pos = sprite.get_y() + sprite.get_sprite_size()[1]
                if sprite_pos - sprite.width_of_base < hitbox.get_y() + hitbox.get_sprite_size()[1] < sprite_pos + hitbox.get_sprite_size()[1]:
                    self.set_image(hero_left, 7)
                    while pygame.sprite.collide_mask(hitbox, sprite):
                        camera.move_right(screen_sprites, 1)
                    self.able_to_move = False
                    break
        if self.able_to_move is False:
            self.able_to_move = True
        else:
            self.sprite_now += self.hor_animation_speed
            if self.sprite_now < 6:
                self.sprite_now = 6
            elif self.sprite_now >= 10:
                self.sprite_now = 6
            self.set_image(sprites_for_hero_animation[int(self.sprite_now)], self.sprite_now)

    def move_up(self):
        for sprite in pygame.sprite.spritecollide(hitbox, screen_sprites2, False):
            # print(hitbox.get_y(), sprite.get_y() + sprite.get_sprite_size()[1] - sprite.width_of_base, sprite.get_y() + sprite.get_sprite_size()[1])
            if pygame.sprite.collide_mask(hitbox, sprite):
                sprite_pos = sprite.get_y() + sprite.get_sprite_size()[1]
                if sprite_pos - sprite.width_of_base <= hitbox.get_y() <= sprite_pos:
                    self.set_image(hero_up2, 10)
                    while (sprite.get_y() + sprite.get_sprite_size()[1] - sprite.width_of_base <= hitbox.get_y() <= sprite.get_y() + sprite.get_sprite_size()[1]) and pygame.sprite.collide_mask(hitbox, sprite):
                        camera.move_down(screen_sprites, 1)
                    self.able_to_move = False
                    break
        if self.able_to_move is False:
            self.able_to_move = True
        else:
            if self.able_to_move is False:
                self.able_to_move = True
            else:
                self.sprite_now += self.ver_animation_speed
                if self.sprite_now < 10:
                    self.sprite_now = 10
                elif self.sprite_now >= 14:
                    self.sprite_now = 10
                self.set_image(sprites_for_hero_animation[int(self.sprite_now)], self.sprite_now)

    def move_down(self):
        for sprite in pygame.sprite.spritecollide(hitbox, screen_sprites2, False):
            if pygame.sprite.collide_mask(hitbox, sprite):
                sprite_pos = sprite.get_y() + sprite.get_sprite_size()[1]
                if sprite_pos - sprite.width_of_base <= hitbox.get_y() + hitbox.get_sprite_size()[1] <= sprite_pos:
                    self.set_image(hero_down, 0)
                    while (sprite.get_y() + sprite.get_sprite_size()[1] - sprite.width_of_base <
                           hitbox.get_y() + hitbox.get_sprite_size()[1] <
                           sprite.get_y() + sprite.get_sprite_size()[1]) and pygame.sprite.collide_mask(hitbox, sprite) :
                        camera.move_up(screen_sprites, 1)
                    self.able_to_move = False
                    break
        if self.able_to_move is False:
            self.able_to_move = True
        else:
            self.sprite_now += self.ver_animation_speed
            if self.sprite_now < 0:
                self.sprite_now = 0
            elif self.sprite_now >= 2:
                self.sprite_now = 0
            self.set_image(sprites_for_hero_animation[int(self.sprite_now)], self.sprite_now)


class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.rect.y + spr.sprite_size[1] - spr.width_of_base

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

    def move_left(self, sprites, v):
        self.screen_start_x -= v
        self.screen_end_x -= v
        all_sprites.update(v, 0)
        for sprite in screen_sprites2:
            sprite.update(v, 0)
        for i in screen_sprites2:
            if i.get_x() + self.screen_start_x > self.screen_end_x:
                i.kill()
                screen_sprites2.remove(i)
        if sprites[0][-1].get_x() + self.screen_start_x > self.screen_end_x:
            for i in range(len(sprites)):
                sprites[i][-1].kill()
                sprites[i].pop(-1)
        if sprites[0][0].get_x() + self.screen_start_x > self.screen_start_x:
            cell_sy = int(self.screen_start_y // 64)
            cell_sx = int(self.screen_start_x // 64)
            for line in range(0, ceil(self.screen_end_y / 64)):
                for num in range(0, ceil(self.screen_start_x / 64)):
                    sprite = location.location[line][num]
                    if type(sprite) == list:
                        size = sprite[0].get_rect()
                        if num * 64 + size[2] >= self.screen_start_x and line * 64 + size[3] >= self.screen_start_y:
                            if num * 64 + size[2] - velocity <= self.screen_start_x:
                                screen_sprites2.append(Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, location.width_of_base[sprite[0]], barrier_sprites))
            for i in range(len(sprites)):
                if type(location.location[cell_sy + i][cell_sx]) is not list:
                    sprites[i].insert(0, Sprite(location.location[cell_sy + i][cell_sx], sprites[i][0].get_x() - 64, sprites[i][0].get_y(), 0, all_sprites))
                else:
                    sprites[i].insert(0, Sprite(location.location[cell_sy + i][cell_sx][1], sprites[i][0].get_x() - 64, sprites[i][0].get_y(), 0, all_sprites))

    def move_right(self, sprites, v):
        self.screen_start_x += v
        self.screen_end_x += v
        all_sprites.update(-v, 0)
        for sprite in screen_sprites2:
            sprite.update(-v, 0)
        for i in screen_sprites2:
            if i.get_x() + self.screen_start_x + i.get_sprite_size()[0] < self.screen_start_x:
                i.kill()
                screen_sprites2.remove(i)
        if sprites[0][0].get_x() + self.screen_start_x + sprites[0][0].get_sprite_size()[0] < self.screen_start_x:
            for i in range(len(sprites)):
                sprites[i][0].kill()
                sprites[i].pop(0)
        if sprites[0][-1].get_x() + self.screen_start_x + sprites[0][-1].get_sprite_size()[0] < self.screen_end_x:
            cell_sy = int(self.screen_start_y // 64)
            cell_ex = int(self.screen_end_x // 64)
            num = floor(self.screen_end_x // 64)
            for line in range(0, ceil(self.screen_end_y / 64)):
                sprite = location.location[line][num]
                if type(sprite) == list:
                    if sprite[0].get_rect()[3] + line * 64 >= self.screen_start_y:
                        screen_sprites2.append(Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, location.width_of_base[sprite[0]], barrier_sprites))
            for i in range(len(sprites)):
                if type(location.location[cell_sy + i][cell_ex]) is not list:
                    sprites[i].append(Sprite(location.location[cell_sy + i][cell_ex], sprites[i][-1].get_x() + 64, sprites[i][0].get_y(), 0, all_sprites))
                else:
                    sprites[i].append(Sprite(location.location[cell_sy + i][cell_ex][1], sprites[i][-1].get_x() + 64, sprites[i][0].get_y(), 0, all_sprites))

    def move_up(self, sprites, v):
        self.screen_start_y -= v
        self.screen_end_y -= v
        all_sprites.update(0, v)
        for sprite in screen_sprites2:
            sprite.update(0, v)
        for i in screen_sprites2:
            if i.get_y() + self.screen_start_y > self.screen_end_y:
                i.kill()
                screen_sprites2.remove(i)
        if sprites[-1][0].get_y() + self.screen_start_y > self.screen_end_y:
            for i in range(len(sprites[-1])):
                sprites[-1][i].kill()
            sprites.pop(-1)
        if sprites[0][0].get_y() + self.screen_start_y > self.screen_start_y:
            cell_sy = int(self.screen_start_y // 64)
            cell_sx = int(self.screen_start_x // 64)
            for line in range(0, ceil(self.screen_start_y / 64)):
                for num in range(0, ceil(self.screen_end_x / 64)):
                    sprite = location.location[line][num]
                    if type(sprite) == list:
                        rect = sprite[0].get_rect()
                        if rect[3] + line * 64 >= self.screen_start_y:
                            if rect[3] + line * 64 - velocity <= self.screen_start_y:
                                screen_sprites2.append(Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, location.width_of_base[sprite[0]], barrier_sprites))
            sprites.insert(0, [])
            for x in range(len(sprites[1])):
                sprite = location.location[cell_sy][cell_sx + x]
                if type(sprite) == list:
                    sprites[0].append(Sprite(sprite[1], sprites[1][x].get_x(), sprites[1][0].get_y() - 64, 0, all_sprites))
                else:
                    sprites[0].append(Sprite(sprite, sprites[1][x].get_x(), sprites[1][0].get_y() - 64, 0, all_sprites))

    def move_down(self, sprites, v):
        self.screen_start_y += v
        self.screen_end_y += v
        all_sprites.update(0, -v)
        for sprite in screen_sprites2:
            sprite.update(0, -v)
        for i in screen_sprites2:
            if i.get_y() + self.screen_start_y + i.get_sprite_size()[1] < self.screen_start_y:
                i.kill()
                screen_sprites2.remove(i)
        if sprites[0][0].get_y() + self.screen_start_y + sprites[0][0].get_sprite_size()[1] < self.screen_start_y:
            for i in range(len(sprites[0])):
                sprites[0][i].kill()
            sprites.pop(0)
        if sprites[-1][0].get_y() + self.screen_start_y + sprites[0][0].get_sprite_size()[1] < self.screen_end_y:
            cell_sx = int(self.screen_start_x // 64)
            cell_ey = int(self.screen_end_y // 64)
            line = int(self.screen_end_y // 64)
            for num in range(0, ceil(self.screen_end_x / 64)):
                sprite = location.location[line][num]
                if type(sprite) is list:
                    if sprite[0].get_rect()[2] + num * 64 >= self.screen_start_x:
                        screen_sprites2.append(Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, location.width_of_base[sprite[0]], barrier_sprites))
            sprites.append([])
            for x in range(len(sprites[-2])):
                sprite = location.location[cell_ey][cell_sx + x]
                if type(sprite) == list:
                    sprites[-1].append(Sprite(sprite[1], sprites[-2][x].get_x(), sprites[-2][x].get_y() + sprites[-2][x].get_sprite_size()[1], 0, all_sprites))
                else:
                    sprites[-1].append(Sprite(sprite, sprites[-2][x].get_x(), sprites[-2][x].get_y() + sprites[-2][x].get_sprite_size()[1], 0, all_sprites))


if __name__ == '__main__':
    pygame.init()
    screen_size = pygame.display.Info()
    # k = screen_size.current_h / 1080
    # size = size[0] * k
    all_sprites = YAwareGroup()
    barrier_sprites = YAwareGroup()
    characters = YAwareGroup()
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    hero_down = pygame.image.load('data/main1.png').convert_alpha()
    hero_down2 = pygame.image.load('data/main1_left.png').convert_alpha()
    hero_down3 = pygame.image.load('data/main1_right.png').convert_alpha()
    hero_up = pygame.image.load('data/main3.png').convert_alpha()
    hero_up2 = pygame.image.load('data/main3_1.png').convert_alpha()
    hero_up3 = pygame.image.load('data/main3_2.png').convert_alpha()
    hero_up4 = pygame.image.load('data/main3_3.png').convert_alpha()
    hero_up5 = pygame.image.load('data/main3_4.png').convert_alpha()
    hero_right = pygame.image.load('data/main4.png').convert_alpha()
    hero_right2 = pygame.image.load('data/main4_walk.png').convert_alpha()
    hero_right3 = pygame.image.load('data/main4_walk2.png').convert_alpha()
    hero_left = pygame.image.load('data/main5.png').convert_alpha()
    hero_left2 = pygame.image.load('data/main5_walk.png').convert_alpha()
    hero_left3 = pygame.image.load('data/main5_walk2.png').convert_alpha()
    hero_hitbox = pygame.image.load('data/a.png').convert_alpha()
    sprites_for_hero_animation = [hero_down2, hero_down3,
                                  hero_right2, hero_right, hero_right3, hero_right,
                                  hero_left2, hero_left, hero_left3, hero_left,
                                  hero_up2, hero_up3, hero_up4, hero_up5]
    camera = Camera(screen_start_x, screen_start_y, screen_end_x, screen_end_y)
    Hero = Hero(hero_down, int(size[0] / 2 - sprites_for_hero_animation[0].get_size()[0] / 2), int(size[1] / 2 - sprites_for_hero_animation[0].get_size()[1] / 2), hero_hitbox.get_size()[1], barrier_sprites)
    hitbox = Sprite(hero_hitbox, Hero.hitbox_pos[0], Hero.hitbox_pos[1], hero_hitbox.get_size()[1])
    location = StartLocation()
    screen_sprites, screen_sprites2 = render(screen_start_x, screen_start_y, screen_end_x, screen_end_y)
    time = 0
    sec = 0
    while running:
        # print(time % 1000)
        # if time // 1000 == sec:
        #     sec += 1
        #     print(sec)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # при нажатии номер спрайта обнуляется, чтобы
                if event.key == pygame.K_s:
                    sprite_now = 0.4
                elif event.key == pygame.K_d:
                    sprite_now = 2.4
                elif event.key == pygame.K_a:
                    sprite_now = 6.4
                elif event.key == pygame.K_w:
                    sprite_now = 10.4
            elif event.type == pygame.KEYUP:  # при отпускании, спрайт возвращается в своё
                if event.key == pygame.K_d:
                    Hero.set_image(hero_right, 2)
                elif event.key == pygame.K_a:
                    Hero.set_image(hero_right, 6)
                if event.key == pygame.K_s:
                    Hero.set_image(hero_down, 0)
                elif event.key == pygame.K_w:
                    Hero.set_image(hero_up, 10)
        pygame.event.pump()  # нужно, чтобы при зажатой мыши действие происходило несколько раз
        if pygame.key.get_pressed()[pygame.K_a]:
            camera.move_left(screen_sprites, velocity)
            Hero.move_left()
        elif pygame.key.get_pressed()[pygame.K_d]:
            camera.move_right(screen_sprites, velocity)
            Hero.move_right()
        elif pygame.key.get_pressed()[pygame.K_w]:
            camera.move_up(screen_sprites, velocity)
            Hero.move_up()
        elif pygame.key.get_pressed()[pygame.K_s]:
            camera.move_down(screen_sprites, velocity)
            Hero.move_down()
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        barrier_sprites.draw(screen)
        pygame.display.flip()
        pygame.display.set_caption("fps: " + str(clock.get_fps()))
        pygame.display.update()
        clock.tick(fps)
        # for sprite in pygame.sprite.spritecollide(hitbox, screen_sprites2, False):
        #     print(sprite.get_y() + sprite.get_sprite_size()[1] - sprite.width_of_base, hitbox.get_y(), sprite.get_y() + sprite.get_sprite_size()[1])
        # print('barrier screen:', len(screen_sprites2), 'floor screen:', len(screen_sprites), 'all floor', len(all_sprites), 'all barriers', len(barrier_sprites))


# if pygame.sprite.spritecollideany(Hero, screen_sprites2):
#                 sprite_in_touch = pygame.sprite.spritecollide(Hero, screen_sprites2, False)
#                 for i in range(len(sprite_in_touch)):
#                     sprite = sprite_in_touch[i]
#                     sprite_pos = sprite.get_y() + sprite.get_sprite_size()[1]
#                     hero_pos = Hero.get_y() + Hero.get_sprite_size()[1]
#                     # print(sprite_pos, hero_pos)
#                     # print(sprite.get_image(), Hero.get_image())
#                     if sprite_pos - width_of_base[sprite.get_image()] > hero_pos < sprite_pos:
#                         able_to_move = False
#                         break
#             if able_to_move is True:
#                 camera.move_left(screen_sprites)
#                 Hero.move_left()
#             able_to_move = True


# for sprite in pygame.sprite.spritecollide(self, screen_sprites2, False):
#             if pygame.sprite.collide_mask(self, sprite):
#                 sprite_pos = sprite.get_y() + sprite.get_sprite_size()[1]
#                 hero_pos = Hero.get_y() + Hero.get_sprite_size()[1]
#                 # print(sprite_pos, hero_pos)
#                 # print(sprite.get_image(), Hero.get_image())
#                 if sprite_pos - width_of_base[sprite.get_image()] < hero_pos > sprite.get_y() and hero_pos <= sprite_pos:
#                     self.able_to_move = False
#                     camera.move_left(screen_sprites, velocity)
#                     break



# if pygame.sprite.spritecollideany(self, screen_sprites2):
#             sprite_in_touch = pygame.sprite.spritecollide(self, screen_sprites2, False)
#             for i in range(len(sprite_in_touch)):
#                 sprite = sprite_in_touch[i]
#                 sprite_pos = sprite.get_y() + sprite.get_sprite_size()[1]
#                 hero_pos = Hero.get_y() + Hero.get_sprite_size()[1]
#                 # print(sprite_pos, hero_pos)
#                 # print(sprite.get_image(), Hero.get_image())
#                 if sprite_pos - width_of_base[sprite.get_image()] < hero_pos > sprite.get_y() and hero_pos <= sprite_pos:
#                     self.able_to_move = False
#                     camera.move_left(screen_sprites, self.get_x() + self.get_sprite_size()[0] - sprite.get_x())
#                     break

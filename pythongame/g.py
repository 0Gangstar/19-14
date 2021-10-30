import pygame  # загружаю нужные библиотеки
from math import floor, ceil
from World import world, pol, barriers, sprites_for_hero_animation


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
        self.sprite_now = 0
        self.hor_animation_speed = 4 / 32
        self.ver_animation_speed = 2 / 32

    def set_image(self, image, now):
        self.image = image
        self.sprite_now = now

    def move_right(self):
        self.sprite_now += self.hor_animation_speed
        if self.sprite_now < 2:
            self.sprite_now = 2
        elif self.sprite_now >= 6:
            self.sprite_now = 2
        self.set_image(sprites_for_hero_animation[int(self.sprite_now)], self.sprite_now)

    def move_left(self):
        self.sprite_now += self.hor_animation_speed
        if self.sprite_now < 6:
            self.sprite_now = 6
        elif self.sprite_now >= 10:
            self.sprite_now = 6
        self.set_image(sprites_for_hero_animation[int(self.sprite_now)], self.sprite_now)

    def move_up(self):
        self.sprite_now += self.ver_animation_speed
        if self.sprite_now < 10:
            self.sprite_now = 10
        elif self.sprite_now >= 12:
            self.sprite_now = 10
        self.set_image(sprites_for_hero_animation[int(self.sprite_now)], self.sprite_now)

    def move_down(self):
        self.sprite_now += self.ver_animation_speed
        if self.sprite_now < 0:
            self.sprite_now = 0
        elif self.sprite_now >= 2:
            self.sprite_now = 0
        self.set_image(sprites_for_hero_animation[int(self.sprite_now)], self.sprite_now)

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
        for i in barrier_sprites:
            if i.get_x() + self.screen_start_x > self.screen_end_x:
                i.kill()
                # print(len(barrier_sprites))
        if screen_sprites[0][-1].get_x() + self.screen_start_x > self.screen_end_x:
            for i in range(len(screen_sprites)):
                screen_sprites[i][-1].kill()
                screen_sprites[i].pop(-1)
        if screen_sprites[0][0].get_x() + self.screen_start_x > self.screen_start_x:
            cell_sy = self.screen_start_y // 64
            cell_ex = self.screen_end_x // 64
            cell_sx = self.screen_start_x // 64
            # print(self.screen_start_x)
            for line in range(0, ceil(self.screen_end_y / 64)):
                for num in range(0, ceil(self.screen_start_x / 64)):
                    sprite = world[line][num]
                    if type(sprite) == list:
                        size = sprite[0].get_rect()
                        # print('line:', line, 'num:', num, '|', num * 64 + size[2], self.screen_start_x, line * 64 + size[3], self.screen_start_y)
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
        for i in barrier_sprites:
            if i.get_x() + self.screen_start_x + i.get_sprite_size()[0] < self.screen_start_x:
                i.kill()
                # print(len(barrier_sprites))
        if screen_sprites[0][0].get_x() + self.screen_start_x + screen_sprites[0][0].get_sprite_size()[0] < self.screen_start_x:
            for i in range(len(screen_sprites)):
                screen_sprites[i][0].kill()
                screen_sprites[i].pop(0)
        if screen_sprites[0][-1].get_x() + self.screen_start_x + screen_sprites[0][-1].get_sprite_size()[0] < self.screen_end_x:
            cell_sy = self.screen_start_y // 64
            cell_ex = self.screen_end_x // 64
            num = self.screen_end_x // 64
            for line in range(0, ceil(self.screen_end_y / 64)):
                sprite = world[line][num]
                if type(sprite) == list:
                    if sprite[0].get_rect()[3] + line * 64 >= self.screen_start_y:
                        Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, barrier_sprites)
            for i in range(len(screen_sprites)):
                if type(world[cell_sy + i][cell_ex]) is not list:
                    screen_sprites[i].append(Sprite(world[cell_sy + i][cell_ex], screen_sprites[i][-1].get_x() + 64, screen_sprites[i][0].get_y(), all_sprites))
                else:
                    screen_sprites[i].append(Sprite(world[cell_sy + i][cell_ex][1], screen_sprites[i][-1].get_x() + 64, screen_sprites[i][0].get_y(), all_sprites))

    def move_up(self, screen_sprites):
        self.screen_start_y -= velocity
        self.screen_end_y -= velocity
        all_sprites.update(0, velocity)
        barrier_sprites.update(0, velocity)
        for i in barrier_sprites:
            if i.get_y() + self.screen_start_y > self.screen_end_y:
                i.kill()
        if screen_sprites[-1][0].get_y() + self.screen_start_y > self.screen_end_y:
            screen_sprites.pop(-1)
        if screen_sprites[0][0].get_y() + self.screen_start_y > self.screen_start_y:
            cell_sy = self.screen_start_y // 64
            cell_ex = self.screen_end_x // 64
            cell_sx = self.screen_start_x // 64
            for line in range(0, ceil(self.screen_start_y / 64)):
                for num in range(0, ceil(self.screen_end_x / 64)):
                    sprite = world[line][num]
                    if type(sprite) == list:
                        size = sprite[0].get_rect()
                        # print(size[3] + line * 64, self.screen_start_y)
                        if size[3] + line * 64 >= self.screen_start_y:
                            print('a')
                            if size[3] + line * 64 - velocity <= self.screen_start_y:
                                Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, barrier_sprites)
            screen_sprites.insert(0, [])
            for x in range(len(screen_sprites[1])):
                sprite = world[cell_sy][cell_sx + x]
                if type(sprite) == list:
                    screen_sprites[0].append(Sprite(sprite[1], screen_sprites[1][x].get_x(), screen_sprites[1][0].get_y() - 64, all_sprites))
                else:
                    screen_sprites[0].append(Sprite(sprite, screen_sprites[1][x].get_x(), screen_sprites[1][0].get_y() - 64, all_sprites))

    def move_down(self, screen_sprites):
        self.screen_start_y += velocity
        self.screen_end_y += velocity
        all_sprites.update(0, -velocity)
        barrier_sprites.update(0, -velocity)
        for i in barrier_sprites:
            if i.get_y() + self.screen_start_y + i.get_sprite_size()[1] < self.screen_start_y:
                # print(len(barrier_sprites), 'bar')
                i.kill()
        if screen_sprites[0][0].get_y() + self.screen_start_y + screen_sprites[0][0].get_sprite_size()[1] < self.screen_start_y:
            # print(len(screen_sprites), 'sc')
            screen_sprites.pop(0)
        if screen_sprites[-1][0].get_y() + self.screen_start_y + screen_sprites[0][0].get_sprite_size()[1] < self.screen_end_y:
            cell_sy = self.screen_start_y // 64
            cell_ex = self.screen_end_x // 64
            cell_sx = self.screen_start_x // 64
            cell_ey = self.screen_end_y // 64
            line = self.screen_end_y // 64
            for num in range(0, ceil(self.screen_end_x / 64)):
                sprite = world[line][num]
                if type(sprite) is list:
                    if sprite[0].get_rect()[2] + num * 64 >= self.screen_start_x:
                        Sprite(sprite[0], num * 64 - self.screen_start_x, line * 64 - self.screen_start_y, barrier_sprites)
            screen_sprites.append([])
            for x in range(len(screen_sprites[-2])):
                sprite = world[cell_ey][cell_sx + x]
                if type(sprite) == list:
                    screen_sprites[-1].append(Sprite(sprite[1], screen_sprites[-2][x].get_x(), screen_sprites[-2][x].get_y() + screen_sprites[-2][x].get_sprite_size()[1], all_sprites))
                    # print(len(barrier_sprites), 'bar')
                else:
                    screen_sprites[-1].append(Sprite(sprite, screen_sprites[-2][x].get_x(), screen_sprites[-2][x].get_y() + screen_sprites[-2][x].get_sprite_size()[1], all_sprites))


if __name__ == '__main__':
    pygame.init()
    all_sprites = YAwareGroup()
    barrier_sprites = YAwareGroup()
    characters = YAwareGroup()
    size = 1280, 720
    screen = pygame.display.set_mode(size)
    running = True
    fps = 60
    clock = pygame.time.Clock()
    velocity = 5
    screen_start_x = 0
    screen_start_y = 0
    sprite_now = 0
    screen_end_x = screen_start_x + size[0]
    screen_end_y = screen_start_y + size[1]
    camera = Camera(screen_start_x, screen_start_y, screen_end_x, screen_end_y)
    screen_sprites = render(screen_start_x, screen_start_y, screen_end_x, screen_end_y)
    Hero = Hero(sprites_for_hero_animation[0], int(size[0] / 2 - sprites_for_hero_animation[0].get_size()[0] / 2), int(size[1] / 2 - sprites_for_hero_animation[0].get_size()[1] / 2), characters)
    # print(len(barrier_sprites))
    # print(screen_end_x // 64)
    # print(screen_start_x // 64)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # при нажатии номер спрайта обнуляется, чтобы
                if event.key == pygame.K_s:
                    sprite_now = 0
                elif event.key == pygame.K_d:
                    sprite_now = 2
                elif event.key == pygame.K_a:
                    sprite_now = 6
            elif event.type == pygame.KEYUP:  # при отпускании, спрайт возвращается в своё
                if event.key == pygame.K_d:
                    Hero.set_image(sprites_for_hero_animation[3], 2)
                elif event.key == pygame.K_a:
                    Hero.set_image(sprites_for_hero_animation[7], 6)
        pygame.event.pump()  # нужно, чтобы при зажатой мыши действие происходило несколько раз
        # print(len(screen_sprites), len(screen_sprites[0]), len(barrier_sprites))
        if pygame.key.get_pressed()[pygame.K_a]:
            camera.move_left(screen_sprites)
            Hero.move_left()
        elif pygame.key.get_pressed()[pygame.K_d]:
            camera.move_right(screen_sprites)
            Hero.move_right()
        elif pygame.key.get_pressed()[pygame.K_w]:
            camera.move_up(screen_sprites)
            Hero.move_up()
        elif pygame.key.get_pressed()[pygame.K_s]:
            camera.move_down(screen_sprites)
            Hero.move_down()
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        characters.draw(screen)
        barrier_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


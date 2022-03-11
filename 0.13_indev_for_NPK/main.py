import pygame
import pytmx
from os import path


def collideLineLine(l1_p1, l1_p2, l2_p1, l2_p2):

    # normalized direction of the lines and start of the lines
    P = pygame.math.Vector2(*l1_p1)
    line1_vec = pygame.math.Vector2(*l1_p2) - P
    R = line1_vec.normalize()
    Q = pygame.math.Vector2(*l2_p1)
    line2_vec = pygame.math.Vector2(*l2_p2) - Q
    S = line2_vec.normalize()

    # normal vectors to the lines
    RNV = pygame.math.Vector2(R[1], -R[0])
    SNV = pygame.math.Vector2(S[1], -S[0])
    RdotSVN = R.dot(SNV)
    if RdotSVN == 0:
        return False

    # distance to the intersection point
    QP = Q - P
    t = QP.dot(SNV) / RdotSVN
    u = QP.dot(RNV) / RdotSVN

    return t > 0 and u > 0 and t*t < line1_vec.magnitude_squared() and u*u < line2_vec.magnitude_squared()


def colideRectLine(rect, p1, p2):
    return (collideLineLine(p1, p2, rect.topleft, rect.bottomleft) or
            collideLineLine(p1, p2, rect.bottomleft, rect.bottomright) or
            collideLineLine(p1, p2, rect.bottomright, rect.topright) or
            collideLineLine(p1, p2, rect.topright, rect.topleft))


def collideRectPolygon(rect, polygon):
    for i in range(len(polygon)-1):
        if colideRectLine(rect, polygon[i], polygon[i+1]):
            return True
    return False


def draw_with_layers(sprite, group, surface):
    bottom_layer = []
    top_layer = []
    for spr in group:
        if spr.collide_top > sprite.rect.bottom - 1 or ((spr.down_layer is not None) and (sprite.hit_rect.colliderect(spr.down_layer))):
            top_layer.append(spr)
        else:
            bottom_layer.append(spr)
    for spr in bottom_layer:
        surface.blit(spr.image, camera.apply(spr))
    surface.blit(player.image, camera.apply(player))
    for spr in top_layer:
        surface.blit(spr.image, camera.apply(spr))


def collide_with_walls(sprite, group, dir):
    x, y = 0, 0
    if sprite.vel[0] > 0:
        x = -1
    elif sprite.vel[0] < 0:
        x = 1
    if sprite.vel[1] > 0:
        y = -1
    elif sprite.vel[1] < 0:
        y = 1
    hits = pygame.sprite.spritecollide(sprite, group, False)
    if hits:
        for collide in hits:
            while collideRectPolygon(sprite.hit_rect, collide.hit_polygon):
                sprite.pos[0] += x
                sprite.rect.x += x
                sprite.hit_rect.x += x
                sprite.pos[1] += y
                sprite.rect.y += y
                sprite.hit_rect.y += y


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.tilewidth = tm.tilewidth
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.map_image = pygame.Surface((self.width, self.height))
        self.map_rect = self.map_image.get_rect()
        self.render()

    def render(self):  # cчитываю карту и переношу всё на холст и в группы добавляю
        objects.empty()
        walls.empty()
        tile_obj = dict()
        ti = self.tmxdata.get_tile_image_by_gid
        for gid, collides in self.tmxdata.get_tile_colliders():  # возвращает все объекты спрайтов
            tile_obj[gid] = collides
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        self.map_image.blit(tile, (x * self.tmxdata.tilewidth,
                                            (y + 1) * self.tmxdata.tileheight - tile.get_size()[1]))
                        if layer.name == 'Objects':
                            collider = []
                            try:
                                collider = tile_obj[gid]
                            except:
                                pass
                            Walls(tile, x * self.tmxdata.tilewidth, (y + 1) * self.tmxdata.tileheight - tile.get_size()[1], collider, walls)
        for group in self.tmxdata.objectgroups:
            if group.name == 'Obstacles':
                for obj in group:
                    Obstacle(obj, objects)

    def load_level(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.tilewidth = tm.tilewidth
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.map_image = pygame.Surface((self.width, self.height))
        self.map_rect = self.map_image.get_rect()
        self.render()


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.vel = (0, 0)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def apply_collide(self, collide):
        return collide.hit_rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)
        # limit scrolling to map size
        # x = min(0, x)  # lef
        # y = min(0, y)  # top
        # x = max(-(self.width - width), x)  # right
        # y = max(-(self.height - height), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = [x, y]
        self.rect.topleft = self.pos
        self.sprite_size = self.image.get_size()
        self.vel = (0, 0)

    def update(self, target):
        self.rect.center = (target.rect.centerx, target.rect.centery)

    def get_image(self):
        return self.image

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

    def get_sprite_size(self):
        return self.sprite_size


class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = [x, y]
        self.rect.center = self.pos
        self.sprite_size = self.image.get_size()
        self.hit_rect = pygame.Rect(self.rect.left, self.rect.bottom - 12, self.rect.width, 12)
        self.vel = (0, 0)
        self.half_height = self.rect[3] / 2
        self._layer = self.rect.bottom

    def update(self):
        self.get_keys()
        x, y = self.vel[0] * dt, self.vel[1] * dt
        self.pos[0] += x
        self.hit_rect.centerx = self.pos[0]
        self.pos[1] += y
        self.hit_rect.y = self.pos[1] + self.half_height - 12
        self.rect.center = self.pos
        # self.interaction(screen_objects)
        self.interaction(screen_objects)
        collide_with_walls(player, screen_sprites, 'x')

    def get_keys(self):
        self.vel = (0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel = (-speed, 0)
            # all_sprites.change_layer(player, player.rect.bottom)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel = (speed, 0)
            # all_sprites.change_layer(player, player.rect.bottom)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = (0, -speed)
            # all_sprites.change_layer(player, player.rect.bottom)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = (0, speed)
            # all_sprites.change_layer(player, player.rect.bottom)

    def interaction(self, group):
        for obj in group:
            if collideRectPolygon(self.hit_rect, obj.hit_polygon):
                name = obj.data.name.split(' ')
                if name[0] == 'door':
                    screen.fill((0, 0, 0))
                    map.load_level(path.join(map_folder, name[2]))
                    for object in objects:
                        name2 = object.data.name.split(' ')
                        if name[1] == name2[1]:
                            if object.rect.width > object.rect.height:
                                if name2[3] == 'down':
                                    pos = object.rect.midbottom
                                    self.rect.midbottom = (pos[0], pos[1] + map.tilewidth)
                                    self.pos = list(self.rect.center)
                                    self.hit_rect.centerx = self.pos[0]
                                    self.hit_rect.y = self.pos[1] + self.half_height - 12
                                elif name2[3] == 'up':
                                    pos = object.rect.midtop
                                    self.rect.midbottom = (pos[0], pos[1] - map.tilewidth)
                                    self.pos = list(self.rect.center)
                                    self.hit_rect.centerx = self.pos[0]
                                    self.hit_rect.y = self.pos[1] + self.half_height - 12
                            else:
                                if name2[3] == 'down':
                                    pos = object.rect.midleft
                                    self.rect.bottomright = (pos[0] - map.tilewidth, pos[1])
                                    self.pos = list(self.rect.center)
                                    self.hit_rect.centerx = self.pos[0]
                                    self.hit_rect.y = self.pos[1] + self.half_height - 12
                                elif name2[3] == 'up':
                                    pos = object.rect.midright
                                    self.rect.bottomleft = (pos[0] + map.tilewidth, pos[1])
                                    self.pos = list(self.rect.center)
                                    self.hit_rect.centerx = self.pos[0]
                                    self.hit_rect.y = self.pos[1] + self.half_height - 12
                            break
                    break


class Walls(pygame.sprite.Sprite):
    def __init__(self, image, x, y, collide, *group):  # с помощью супера все созданные спрайты скидываю в группу спрайтов
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = [x, y]
        self.rect.topleft = (x, y)
        self.sprite_size = self.image.get_size()
        self.vel = (0, 0)
        self._layer = self.rect.bottom
        self.hit_polygon = []
        self.down_layer = None
        for collider in collide:
            if collider.name == 'bottom_layer':
                self.down_layer = pygame.Rect(collider.x + x, collider.y + y, collider.width, collider.height)
            elif collider.name is None:
                points = collider.points
                for coords in points:
                    self.hit_polygon.append([coords[0] + x, coords[1] + y])
                self.hit_polygon.append([points[0][0] + x, points[0][1] + y])
        self.collide_top = self.rect.bottom
        for coords in self.hit_polygon:
            if coords[1] < self.collide_top:
                self.collide_top = coords[1]


    # def polygon(self):
    #     return self.hit_polygon


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, object, *group):
        super().__init__(*group)
        self.data = object
        self.rect = pygame.Rect(object.x, object.y, object.width, object.height)
        self.pos = [object.x, object.y]
        # print(self.rect)
        self.hit_polygon = []
        for points in self.data.points:
            self.hit_polygon.append([points[0], points[1]])
        self.hit_polygon.append([self.data.points[0][0], self.data.points[0][1]])

    def update(self, target):
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)
        self.rect.center = (x, y)


class YAwareGroup(pygame.sprite.Group):

    def sprites_update(self, group):
        cam = camera.camera
        self.empty()
        for spr in group:
            rect = spr.rect
            if rect[0] <= -cam[0] + cam[2] and rect[0] + rect[2] >= -cam[0] and rect[1] <= -cam[1] + cam[3] and rect[1] + rect[3] >= -cam[1]:
                self.add(spr)


pygame.init()

width = 1920
height = 1016
screen = pygame.display.set_mode((width, height))

camera = Camera(width, height)
clock = pygame.time.Clock()

game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')

walls = YAwareGroup()  # все стены
objects = YAwareGroup()  # все объекты
screen_sprites = YAwareGroup()  # только стены, которые на экране
screen_objects = YAwareGroup()  # объекты, которые на экране

map = TiledMap(path.join(map_folder, 'test.tmx'))
player = Player(pygame.image.load("data/main1.png").convert_alpha(), width / 2, height / 2)
img = pygame.image.load("data/junk_can.png").convert_alpha()
running = True
fps = 10000
speed = 300
time = 0
sec = 0
dt = 0  # коэффицент который зависит от FPS и определяет скорость персонажа

while running:
    time += clock.get_time()
    player.update()
    camera.update(player)

    if time // 1000 == sec:
        sec += 1
        pygame.display.set_caption("fps: " + str(clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen_sprites.sprites_update(walls)
    screen_objects.sprites_update(objects)

    screen.blit(map.map_image, camera.apply_rect(map.map_rect))
    draw_with_layers(player, screen_sprites, screen)

    # for j in range(0, 16):
    #     for i in range(0, 30):
    #         screen.blit(img, (64 * i, 64 * j))

    # for i in screen_objects:
    #     print(i.rect, player.rect)
    pygame.display.flip()
    dt = clock.tick(fps) / 1000


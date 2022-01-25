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
        if spr.collide_top >= sprite.rect.bottom or ((spr.down_layer is not None) and (sprite.hit_rect.colliderect(spr.down_layer))):
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
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        print(self.width, self.height)
        self.tmxdata = tm

    def render(self, surface): # cчитываю карту и переношу всё на холст и в группы добавляю
        tile_obj = dict()
        ti = self.tmxdata.get_tile_image_by_gid
        for gid, collides in self.tmxdata.get_tile_colliders(): # возвращает все объекты спрайтов
            tile_obj[gid] = collides
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            (y + 1) * self.tmxdata.tileheight - tile.get_size()[1]))
                        if layer.name == 'Objects':
                            try:
                                collider = tile_obj[gid]
                            except:
                                collider = []
                            Walls(tile, x * self.tmxdata.tilewidth, (y + 1) * self.tmxdata.tileheight - tile.get_size()[1], collider, walls)

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface.convert()


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
        self.hit_rect = pygame.Rect(self.rect.left, self.rect.bottom - 12, 44, 12)
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
                print(self.down_layer)
            elif collider.name is None:
                points = collider.points
                for coords in points:
                    self.hit_polygon.append([coords[0] + x, coords[1] + y])
                self.hit_polygon.append([points[0][0] + x, points[0][1] + y])
        self.collide_top = self.rect.bottom
        for coords in self.hit_polygon:
            if coords[1] < self.collide_top:
                self.collide_top = coords[1]
        # print(self.collide_top)


    def update(self, target):
        x = -target.rect.x + int(width / 2)
        y = -target.rect.x + int(height / 2)
        self.rect.topleft = (x, y)
        self.hit_rect.move(x, y)

    def polygon(self):
        return self.hit_polygon


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        # print(self.rect)
        self.hit_rect = self.rect

    def update(self, target):
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)
        self.rect.center = (x, y)


class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.rect.bottom - spr.hit_rect[3]

    def sprites_update(self, group):
        cam = camera.camera
        self.empty()
        for spr in group:
            rect = spr.rect
            if rect[0] <= -cam[0] + cam[2] and rect[0] + rect[2] >= -cam[0] and rect[1] <= -cam[1] + cam[3] and rect[1] + rect[3] >= -cam[1]:
                all_sprites.add(spr)


pygame.init()
width = 1920
height = 1016
game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')
print(game_folder)
all_sprites = YAwareGroup()
walls = YAwareGroup()
obstacles = YAwareGroup()
screen = pygame.display.set_mode((width, height))
map = TiledMap(path.join(map_folder, 'test.tmx'))
# for tile_object in map.tmxdata.objects:
#     print(tile_object.points)
map_img = map.make_map()
map.rect = map_img.get_rect()
running = True
clock = pygame.time.Clock()
fps = 500
speed = 300
camera = Camera(width, height)
player = Player(pygame.image.load("data/main1.png").convert_alpha(), width / 2, height / 2)
time = 0
sec = 0
dt = 0

while running:
    time += clock.get_time()
    player.update()
    collide_with_walls(player, all_sprites, 'x')
    camera.update(player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(map_img, camera.apply_rect(map.rect))
    all_sprites.sprites_update(walls)
    draw_with_layers(player, all_sprites, screen)

    if time // 1000 == sec:
        sec += 1
        pygame.display.set_caption("fps: " + str(clock.get_fps()))

    dt = clock.tick(fps) / 1000
    pygame.display.flip()

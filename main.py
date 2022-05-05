import pygame
import pytmx
from os import path
import moderngl
import numpy as np


# подправить столкновение прямоугольников
# класс полигона ---
# наследственность -
# прямоугольники и полигоны (одновременная поддержка) -
# столкновение между полигонами, прямоугольниками и смешанное -
# смешать столкновение и взаимодействие персонажа - (вроде не надо)
# сделать взаимодействие по нажатию клавиши и отдельный хитбокс взаимводействия
# анимация перса
# смена хитбокса при повороте или квадратом сделать
# отход персонажа при повороте если хитбокс не вмещается
# сделать множества спрайтов и обновлять размеры текстур через них

def set_uniform(u_name, u_value):
    try:
        prog[u_name] = u_value
    except KeyError:
        print(f'uniform: {u_name} - not used in shader')


def convert_vertex(pt, surface_size):
    return pt[0] / surface_size[0] * 2 - 1, 1 - pt[1] / surface_size[1] * 2


def convert_texture_pos(texture_pos, source_size):
    vert1 = texture_pos[0] / source_size[0], 1 - texture_pos[1] / source_size[1]
    vert2 = (texture_pos[0] + texture_pos[2]) / source_size[0], 1 - (texture_pos[1] + texture_pos[3]) / source_size[1]
    return *vert1, *vert2


def get_vertices(objects, window_size):
    verts = []
    for object in objects:
        rect = camera.apply_rect(object.get_rect())
        image_pos = object.texture_pos
        source = object.source_id
        vert1 = convert_vertex((rect[0], rect[1]), window_size)
        vert2 = convert_vertex((rect[0] + rect[2], rect[1]), window_size)
        vert3 = convert_vertex((rect[0] + rect[2], rect[1] + rect[3]), window_size)
        vert4 = convert_vertex((rect[0], rect[1] + rect[3]), window_size)
        img_vert1 = image_pos[0], image_pos[1]
        img_vert2 = image_pos[2], image_pos[1]
        img_vert3 = image_pos[2], image_pos[3]
        img_vert4 = image_pos[0], image_pos[3]
        verts.append([*vert1, *img_vert1, source, *vert2, *img_vert2, source, *vert3, *img_vert3, source,
                      *vert1, *img_vert1, source, *vert3, *img_vert3, source, *vert4, *img_vert4, source])
    return verts


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


def collidePolygonLine(polygon, p1, p2):
    for point in polygon.points:
        if collideLineLine(p1, p2, point[0], point[1]):
            return True
    return False


def collideRectPolygon(rect, polygon):
    points = polygon.points
    for i in range(len(points)-1):
        if colideRectLine(rect, points[i], points[i+1]):
            return True
    return False


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
            if collide.hit_polygon is not None:
                if collide.hit_polygon.__class__.__name__ == 'Polygon':
                    while collideRectPolygon(sprite.hit_polygon, collide.hit_polygon):
                        sprite.set_coords(x, y)
                elif collide.hit_polygon.__class__.__name__ == 'Rect':
                    while pygame.Rect.colliderect(sprite.hit_polygon, collide.hit_polygon):
                        # print(collide.hit_polygon)
                        sprite.set_coords(x, y)


def draw(vertices):
    vertices = np.array(vertices, dtype='f4').tobytes()
    Buffer = ctx.buffer(vertices)
    vao = ctx.vertex_array(prog, [(Buffer, "2f4 2f4 f4", "in_position", "in_uv", "num")])
    vao.render()


def draw_with_layers(first_layer, second_layer, sprite):
    # all_sprites = ist(second_layer)
    # # print(all_sprites)
    # for wall in range(len(all_sprites)):
    #     if sprite.rect.bottom < all_sprites[wall].rect.bottom and sprite.rect.right <= all_sprites[wall].rect.left:
    #         all_sprites.insert(wall, sprite)
    #         break
    # print(wall)
    all_sprites = []
    bottom_layer = [first_layer]
    top_layer = []

    for spr in second_layer:
        if spr.hit_polygon is None:
            if spr.rect.bottom >= sprite.rect.bottom - 1:
                top_layer.append(spr)
        elif spr.hit_polygon.top >= sprite.rect.bottom - 1 or ((spr.down_layer is not None) and (sprite.hit_polygon.colliderect(spr.down_layer))):
            top_layer.append(spr)
        else:
            bottom_layer.append(spr)
    all_sprites.extend(bottom_layer)
    all_sprites.append(sprite)
    all_sprites.extend(top_layer)

    vertices = get_vertices(all_sprites, screen_size)
    draw(vertices)


# def save_game():


class Polygon:
    def __init__(self, points, pos=(0, 0)):
        self.points = []
        self.top = points[0][1]
        for point in points:
            if point[1] < self.top:
                self.top = point[1]
            self.points.append([point[0] + pos[0], point[1] + pos[1]])
        self.points.append(self.points[0])
        self.top += pos[1]

    def move(self, pos):
        pass


class TiledMap:
    source = None
    source_id = 1
    source_size = None

    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.tilewidth = tm.tilewidth
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.map_image = pygame.Surface((self.width, self.height)).convert_alpha()
        TiledMap.source_size = self.map_image.get_size()
        self.map_rect = self.map_image.get_rect()
        self.texture_pos = convert_texture_pos(self.map_rect, self.map_image.get_size())
        self.objects_atlas = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
        self.render()

    def render(self):  # cчитываю карту и переношу всё на холст и в группы добавляю
        objects.empty()
        walls.empty()
        tile_obj = dict()
        ti = self.tmxdata.get_tile_image_by_gid
        atlas_pos = dict()
        for gid, colliders in self.tmxdata.get_tile_colliders():  # возвращает все объекты спрайтов
            tile_obj[gid] = colliders
        # print(tile_obj)
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        x_pos = x * self.tmxdata.tilewidth
                        y_pos = (y + 1) * self.tmxdata.tileheight - tile.get_size()[1]
                        if tile not in atlas_pos.keys():
                            size = self.objects_atlas.get_size()
                            copy = self.objects_atlas.copy()
                            self.objects_atlas = pygame.Surface((size[0] + tile.get_width(), max(size[1], tile.get_height())), pygame.SRCALPHA, 32)
                            self.objects_atlas.blit(copy, (0, 0))
                            self.objects_atlas.blit(tile, (size[0], 0))
                            atlas_pos[tile] = (size[0], 0, *tile.get_size())
                        self.map_image.blit(tile, (x_pos, y_pos))
                        if layer.name == 'Objects':
                            collider = []
                            try:
                                collider = tile_obj[gid]
                            except:
                                pass
                            Walls(atlas_pos[tile], x_pos, y_pos, collider)
        for group in self.tmxdata.objectgroups:
            if group.name == 'Obstacles':
                for obj in group:
                    Obstacle(obj)

        Walls.source_size = self.objects_atlas.get_size()
        for wall in walls:
            wall.convert_texture_pos()
        # pygame.image.save(self.objects_atlas, 'ahh.png')
        dirt_bytes = pygame.image.tostring(self.map_image, 'RGBA', False)
        texture = ctx.texture(self.map_image.get_size(), 4, dirt_bytes)
        texture.use(location=1)
        dirt_bytes = pygame.image.tostring(self.objects_atlas, 'RGBA', False)
        texture = ctx.texture(self.objects_atlas.get_size(), 4, dirt_bytes)
        texture.use(location=2)

    def load_level(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.tilewidth = tm.tilewidth
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.map_image = pygame.Surface((self.width, self.height)).convert_alpha()
        TiledMap.source_size = self.map_image.get_size()
        self.map_rect = self.map_image.get_rect()
        self.texture_pos = convert_texture_pos(self.map_rect, self.map_image.get_size())
        self.objects_atlas = pygame.Surface((0, 0))
        self.render()

    def get_rect(self):
        return self.map_rect


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


class ActiveSprite(pygame.sprite.Sprite):
    source = None
    source_id = None
    source_size = None

    def __init__(self, texture_pos, x, y, colliders, *group):
        pygame.sprite.Sprite.__init__(*group)
        self.texture_pos = texture_pos
        self.sprite_size = self.texture_pos[2:]
        self.rect = pygame.Rect(0, 0, self.sprite_size)
        self.pos = [x, y]
        self.rect.topleft = self.pos
        self.hit_polygon = pygame.Rect(0, 0, 0, 0)
        self.vel = (0, 0)
        self.down_layer = None
        for collider in colliders:
            if collider.name == 'bottom_layer':
                self.down_layer = pygame.Rect(collider.x + x, collider.y + y, collider.width, collider.height)
            elif collider.name is None:
                try:
                    self.hit_polygon = Polygon(self.pos, collider.points)
                except AttributeError:
                    self.hit_polygon = pygame.Rect(collider.x + x, collider.y + y, collider.width, collider.height)

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
    source = None
    source_id = 3
    source_size = None

    def __init__(self, texture_pos, x, y):
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.texture_pos = convert_texture_pos(texture_pos, Player.source_size)
        self.sprite_size = texture_pos[2:]
        self.rect = pygame.Rect(0, 0, *self.sprite_size)
        self.pos = [x, y]
        self.rect.center = self.pos
        self.hit_polygon = pygame.Rect(self.rect.left, self.rect.bottom - 12, self.rect.width, 12)
        self.interaction_box = pygame.Rect(0, 0, self.sprite_size[0] * 0.75, self.hit_polygon.height * 5)
        self.interaction_box.midbottom = self.rect.midbottom
        self.vel = (0, 0)
        self.half_height = self.rect[3] / 2
        self._layer = self.rect.bottom
        self.offsetX, self.offsetY = 0, 0

    def get_keys(self):
        self.vel = (0, 0)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_l:
                    self.interaction(screen_objects)
            if event.type == pygame.QUIT:
                quit()
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

    def update(self):
        self.get_keys()
        x, y = self.vel[0] * dt, self.vel[1] * dt
        self.offsetX += x
        self.offsetY += y
        self.pos[0] += x
        self.pos[1] += y
        if self.offsetX >= 1 or self.offsetX <= -1:
            self.rect.move_ip(self.offsetX, 0)
            self.hit_polygon.move_ip(self.offsetX, 0)
            self.interaction_box.move_ip(self.offsetX, 0)
            if self.offsetX <= 0:
                self.offsetX += 1
            else:
                self.offsetX -= 1
        if self.offsetY >= 1 or self.offsetY <= -1:
            self.rect.move_ip(0, self.offsetY)
            self.hit_polygon.move_ip(0, self.offsetY)
            self.interaction_box.move_ip(0, self.offsetY)
            if self.offsetY <= 0:
                self.offsetY += 1
            else:
                self.offsetY -= 1
        # self.interaction(screen_objects)
        collide_with_walls(player, screen_sprites, 'x')

    def interaction(self, group):
        for obj in group:
            collision = False
            try:
                if collideRectPolygon(self.interaction_box, obj.hit_polygon):
                    collision = True
            except AttributeError:
                if pygame.Rect.colliderect(self.interaction_box, obj.hit_polygon):
                    collision = True
            if collision is True:
                name = obj.data.name.split(' ')
                if name[0] == 'door':
                    map.load_level(path.join(map_folder, name[2]))
                    for obj2 in objects:
                        name2 = obj2.data.name.split(' ')
                        if name[1] == name2[1]:
                            if obj2.rect.width > obj2.rect.height:
                                if name2[3] == 'down':
                                    pos = obj2.rect.midbottom
                                    self.rect.midbottom = (pos[0], pos[1] + map.tilewidth)
                                    self.pos = list(self.rect.center)
                                    self.hit_polygon.centerx = self.pos[0]
                                    self.hit_polygon.y = self.pos[1] + self.half_height - 12
                                elif name2[3] == 'up':
                                    pos = obj2.rect.midtop
                                    self.rect.midbottom = (pos[0], pos[1] - map.tilewidth)
                                    self.pos = list(self.rect.center)
                                    self.hit_polygon.centerx = self.pos[0]
                                    self.hit_polygon.y = self.pos[1] + self.half_height - 12
                            else:
                                if name2[3] == 'down':
                                    pos = obj2.rect.midleft
                                    self.rect.bottomright = (pos[0] - map.tilewidth, pos[1])
                                    self.pos = list(self.rect.center)
                                    self.hit_polygon.centerx = self.pos[0]
                                    self.hit_polygon.y = self.pos[1] + self.half_height - 12
                                elif name2[3] == 'up':
                                    pos = obj2.rect.midright
                                    self.rect.bottomleft = (pos[0] + map.tilewidth, pos[1])
                                    self.pos = list(self.rect.center)
                                    self.hit_polygon.centerx = self.pos[0]
                                    self.hit_polygon.y = self.pos[1] + self.half_height - 12
                            break
                    break

    def set_coords(self, x, y):
        self.pos[0] += x
        self.rect.x += x
        self.hit_polygon.x += x
        self.pos[1] += y
        self.rect.y += y
        self.hit_polygon.y += y
        self.interaction_box.x += x
        self.interaction_box.y += y

    def get_rect(self):
        return self.rect


class Walls(pygame.sprite.Sprite):
    source = None
    source_id = 2
    source_size = None

    def __init__(self, texture_pos, x, y, collide):  # с помощью супера все созданные спрайты скидываю в группу спрайтов
        self.groups = all_sprites, walls
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.texture_pos = texture_pos
        # print(self.texture_pos)
        self.spite_size = texture_pos[2:]
        self.rect = pygame.Rect(0, 0, *self.spite_size)
        self.pos = [x, y]
        self.rect.topleft = self.pos
        self.vel = (0, 0)
        self._layer = self.rect.bottom
        self.hit_polygon = None
        self.down_layer = None
        for collider in collide:
            if collider.name == 'bottom_layer':
                self.down_layer = pygame.Rect(collider.x + x, collider.y + y, collider.width, collider.height)
            elif collider.name is None:
                try:
                    self.hit_polygon = Polygon(collider.points, self.pos)
                except AttributeError:
                    self.hit_polygon = pygame.Rect(collider.x + x, collider.y + y, collider.width, collider.height)

    def get_rect(self):
        return self.rect

    def convert_texture_pos(self):
        self.texture_pos = convert_texture_pos(self.texture_pos, Walls.source_size)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, object):
        self.groups = all_sprites, objects
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.data = object
        self.rect = pygame.Rect(object.x, object.y, object.width, object.height)
        self.pos = [object.x, object.y]
        # print(self.rect)
        try:
            self.hit_polygon = Polygon(self.data.points)
        except AttributeError:
            self.hit_polygon = pygame.Rect(object.x, object.y, object.width, object.height)
        # self.hit_polygon = []
        # for points in self.data.points:
        #     self.hit_polygon.append([points[0], points[1]])
        # self.hit_polygon.append([self.data.points[0][0], self.data.points[0][1]])

    def update(self, target):
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)
        self.rect.center = (x, y)


# class SpriteObstacle:
#     def __init__(self, x, y, rect=None, points=None):
#         self.hit_box = pygame.Rect(0, 0, 0, 0)
#         if rect is not None:


class ScreenGroup(pygame.sprite.Group):

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
screen_size = (width, height)
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)


camera = Camera(width, height)
clock = pygame.time.Clock()
ctx = moderngl.create_context()
ctx.enable(moderngl.BLEND)

prog = ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_position;
            in vec2 in_uv;
            in float num;
            out vec2 v_uv;
            out float v_num;
            void main()
            {
                v_uv = in_uv;
                v_num = num;
                gl_Position = vec4(in_position, 0.0, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            out vec4 fragColor;
            uniform sampler2D u_texture;
            uniform sampler2D u_texture2;
            uniform sampler2D u_texture3;
            in vec2 v_uv;
            in float v_num;
            void main() 
            {
                if (int(v_num) == 1) {
                    fragColor = texture(u_texture, vec2(v_uv[0], -v_uv[1]));
                }
                else if (int(v_num) == 2) {
                    fragColor = texture(u_texture2, vec2(v_uv[0], -v_uv[1]));
                } 
                else if (int(v_num) == 3) {
                    fragColor = texture(u_texture3, vec2(v_uv[0], -v_uv[1]));
                } 
            }
            """)

set_uniform('u_texture', 1)
set_uniform('u_texture2', 2)
set_uniform('u_texture3', 3)

game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')

all_sprites = pygame.sprite.LayeredUpdates()
walls = pygame.sprite.Group()  # все стены
objects = pygame.sprite.Group()  # все объекты
screen_sprites = ScreenGroup()  # только стены, которые на экране
screen_objects = ScreenGroup()  # объекты, которые на экране

player_sprite = pygame.image.load('data/main1.png').convert_alpha()

bytes_player_image = pygame.image.tostring(player_sprite, 'RGBA', False)
player_texture = ctx.texture(player_sprite.get_size(), 4, bytes_player_image)
player_texture.use(location=3)
Player.source_size = player_sprite.get_size()
print(player_sprite.get_size())

map = TiledMap('maps/test.tmx')
player = Player(player_sprite.get_rect(), width / 2, height / 2)

running = True
fps = 10000
speed = 300
time = 0
sec = 0
dt = 0  # коэффицент который зависит от FPS и определяет скорость персонажа

print('end')
while running:
    time += clock.get_time()
    player.update()
    camera.update(player)

    if time // 1000 == sec:
        sec += 1
        pygame.display.set_caption("fps: " + str(clock.get_fps()))

    screen_sprites.sprites_update(walls)
    screen_objects.sprites_update(objects)

    ctx.clear(0, 0, 0, 1)
    draw_with_layers(map, screen_sprites, player)

    pygame.display.flip()
    dt = clock.tick(fps) / 1000


import pygame
import pytmx
from os import path
import moderngl
import numpy as np
import json
from items import all_items


# хранить данные об изменении карт в файлах
# по х, у и layer находить свойства объекта
# при изменении карты, в файл добавлять ид нового или заменяющего спрайта
# sprite info в tiled map
# walls, objects, all_sprites в tiledmap

# подправить столкновение прямоугольников
# класс полигона ---
# наследственность -
# прямоугольники и полигоны (одновременная поддержка) -
# столкновение между полигонами, прямоугольниками и смешанное -
# смешать столкновение и взаимодействие персонажа - (вроде не надо)
# сделать взаимодействие по нажатию клавиши и отдельный хитбокс взаимводействия -
# анимация перса -
# смена хитбокса при повороте или квадратом сделать - (пока скип)
# отход персонажа при повороте если хитбокс не вмещается - (скип так как прошлое скип)
# сделать множества спрайтов и обновлять размеры текстур через них
# отрисовка хрень кста. Слои неверные. Переделать

# изменять переменную direction, когда повороты -
# преписать переходы с использованием тп -
# дописать столковение для всех направлений -
# добавить отталкивание при столкновении-
# округлять точки препятствий -
# прямоугольные тригеры

# что должен уметь соприкосновение с объектами
# 1 Переход между локациями
# 1.1 Анимации / эффекты при переходе
# 1.2 сменить локацию и положение персонажа (направление взгляда, хитбоксов, координаты)
#
# 2 Простое взаимодействие
# 2.1 Получить предмет (Какой, сколько его, сколько раз получить, переодичность, проверить на условиz)
# 2.2 Поменять текстуру (Какую (по клетке), На какую (id), место новой текстуры, навсегда)
# 2.3 проиграть анимацию/эффекты/звук
# 2.4 добавить новый объект (куда (клетку), какой(id), хитбокс(id))
# 2.5 Выдать диалоговое окно (текст)
# 2.6 выдать инвентарь, чтобы использоловать предмет
# 2.7 запустить события (бой, переход, катсцена, что-то забрать, прокачать и т.д.)
#
#
#

# Диалоговое окно
# примититивные статы героя (хп, уровень, ехп, атака, защита)
# НПС
# Бои
# Инвентарь визуальный, удаление предметов, чек инфы, использовать вещи


def texture(image):
    pass


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


def get_points(points):
    side_points = []
    x_lines = dict()
    y_lines = dict()
    if len(points) > 0:
        for i in range(len(points)-1):
            point = points[i]
            point2 = points[i + 1]
            if point2[0] > point[0]:
                lesser_x, greater_x = point[0], point2[0]
            else:
                lesser_x, greater_x = point2[0], point[0]
            if point2[1] > point[1]:
                lesser_y, greater_y = point[1], point2[1]
            else:
                lesser_y, greater_y = point2[1], point[1]

            if point2[1] == point[1]:
                y = point2[1]
                for x in range(lesser_x, greater_x + 1):
                    side_points.append((x, y))
            elif point2[0] == point[0]:
                x = point2[0]
                for y in range(lesser_y, greater_y + 1):
                    side_points.append((x, y))

            else:
                k = (point2[1] - point[1]) / (point2[0] - point[0])
                b = point2[1] - k * point2[0]
                for x in range(lesser_x, greater_x + 1):
                    y = round(k * x + b)
                    side_points.append((x, y))

                for y in range(lesser_y, greater_y + 1):
                    x = round((y - b) / k)
                    side_points.append((x, y))
        side_points = set(side_points)
        for point in side_points:
            try:
                x_lines[point[1]].append(point[0])
            except KeyError:
                x_lines[point[1]] = [point[0]]
            try:
                y_lines[point[0]].append(point[1])
            except KeyError:
                y_lines[point[0]] = [point[1]]
        for y in x_lines.keys():
            x_lines[y] = sorted(x_lines[y])
        for x in y_lines.keys():
            y_lines[x] = sorted(y_lines[x])
    return side_points, x_lines, y_lines


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


def collide_with_walls(sprite, group):
    hits = pygame.sprite.spritecollide(sprite, group, False)
    if hits:
        for collide in hits:
            if collide.hit_polygon is not None:
                if collide.hit_polygon.__class__.__name__ == 'Polygon':
                    collide_points = []
                    # print(sprite.hit_polygon.top, sprite.hit_polygon.bottom + 1, " ", sprite.hit_polygon.left)
                    # print(collide.hit_polygon.x_lines)
                    if sprite.direction == 'left':
                        for y in range(sprite.hit_polygon.top + 1, sprite.hit_polygon.bottom):
                            if collide.hit_polygon.collidepoint((sprite.hit_polygon.left, y), 'x'):
                                for y2 in range(y, sprite.hit_polygon.bottom):
                                    collide_points.extend(collide.hit_polygon.get_collidepoint((sprite.hit_polygon.left, y2), 'x'))
                                if collide_points:
                                    sprite.tp(max(collide_points), sprite.hit_polygon.y)
                                break
                    elif sprite.direction == 'right':
                        for y in range(sprite.hit_polygon.top + 1, sprite.hit_polygon.bottom):
                            if collide.hit_polygon.collidepoint((sprite.hit_polygon.right, y), 'x'):
                                for y2 in range(y, sprite.hit_polygon.bottom):
                                    collide_points.extend(collide.hit_polygon.get_collidepoint((sprite.hit_polygon.right, y2), 'x'))
                                if collide_points:
                                    sprite.tp(min(collide_points) - sprite.hit_polygon.width, sprite.hit_polygon.y)
                                break
                    elif sprite.direction == 'up':
                        for x in range(sprite.hit_polygon.left + 1, sprite.hit_polygon.right):
                            if collide.hit_polygon.collidepoint((sprite.hit_polygon.top, x), 'y'):
                                for x2 in range(x, sprite.hit_polygon.right):
                                    collide_points.extend(collide.hit_polygon.get_collidepoint((sprite.hit_polygon.top, x2), 'y'))
                                if collide_points:
                                    sprite.tp(sprite.hit_polygon.x, max(collide_points))
                                break
                    elif sprite.direction == 'down':
                        for x in range(sprite.hit_polygon.left + 1, sprite.hit_polygon.right):
                            if collide.hit_polygon.collidepoint((sprite.hit_polygon.bottom, x), 'y'):
                                for x2 in range(x, sprite.hit_polygon.right):
                                    collide_points.extend(collide.hit_polygon.get_collidepoint((sprite.hit_polygon.bottom, x2), 'y'))
                                if collide_points:
                                    sprite.tp(sprite.hit_polygon.x, min(collide_points) - sprite.hit_polygon.height)
                                break
                elif collide.hit_polygon.__class__.__name__ == 'Rect':
                    if sprite.hit_polygon.colliderect(collide.hit_polygon):
                        if sprite.direction == "up":
                            sprite.tp(sprite.hit_polygon.topleft[0], collide.hit_polygon.bottom)
                        elif sprite.direction == "down":
                            sprite.tp(sprite.hit_polygon.topleft[0], collide.hit_polygon.top - sprite.hit_polygon.height)
                        if sprite.direction == "left":
                            sprite.tp(collide.hit_polygon.right, sprite.hit_polygon.topleft[1])
                        elif sprite.direction == "right":
                            sprite.tp(collide.hit_polygon.left - sprite.hit_polygon.width, sprite.hit_polygon.topleft[1])
                #     while collideRectPolygon(sprite.hit_polygon, collide.hit_polygon ):
                #         sprite.set_coords(x, y)
                # elif collide.hit_polygon.__class__.__name__ == 'Rect':
                #     while pygame.Rect.colliderect(sprite.hit_polygon, collide.hit_polygon):
                #         # print(collide.hit_polygon)
                #         sprite.set_coords(x, y)


def load_opengl_image(image, source):
    bytes_image = bytes(pygame.image.tostring(image, 'RGBA', False))
    new_texture = ctx.texture(image.get_size(), 4, bytes_image)
    new_texture.use(location=source)


def draw(vertices):
    vertices = np.array(vertices, dtype='f4').tobytes()
    buffer = ctx.buffer(vertices)
    vao = ctx.vertex_array(prog, [(buffer, "2f4 2f4 f4", "in_position", "in_uv", "num")])
    vao.render()
    buffer.release()
    vao.release()


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
    if dialog_event:
        vertices.extend(text_window.vertices)
    draw(vertices)


def save_game():
    # saves_folder = path.join(game_folder, 'saves')
    player_info = dict()
    player_info['rect'] = list(player.rect)
    player_info['hit_polygon_rect'] = list(player.hit_polygon)
    player_info['interaction_box'] = list(player.interaction_box)
    player_info['source'] = Player.source
    player_info['texture_pos'] = player.texture_pos
    player_info['location'] = map.tmxdata.filename
    json_player_info = json.dumps(player_info, indent=4)

    with open('saves/slot 1/player_info.json', 'w') as outfile:
        outfile.write(json_player_info)
        outfile.close()


def load_game():
    with open(f'saves/slot 1/player_info.json', 'r') as infile:
        player_info = json.load(infile)
        map.load_level(player_info['location'])
        player.rect = pygame.Rect(player_info['rect'])
        player.pos = [*player.rect.center]
        player.hit_polygon = pygame.Rect(player_info['hit_polygon_rect'])
        player.hit_polygon_pos = [*player.hit_polygon.topleft]
        player.interaction_box = pygame.Rect(player_info['interaction_box'])
        player.interaction_box_pos = [*player.interaction_box.topleft]
        Player.source = player_info['source']
        player.texture_pos = player_info['texture_pos']
        infile.close()


def replace_sprite_by_id(old_sprite, new_sprite_id):
    old_sprite.set_sprite_pos(sprite_info.get_image_pos_by_id(new_sprite_id))
    old_sprite.set_sprite_colliders(sprite_info.get_collider_by_id(new_sprite_id))


def display_info():
    print('x', player.rect.centerx)
    print('y', player.rect.centery)
    print('source', player.source)
    print('texture_pos', player.texture_pos)
    print('location', map.tmxdata.filename)


class SpriteInfo:
    def __init__(self, sprite_colliders, image_positions):
        self.colliders = sprite_colliders
        self.poses = image_positions

    def get_collider_by_id(self, id):
        try:
            return self.colliders[id]
        except KeyError:
            return []

    def get_image_pos_by_id(self, id):
        return self.poses[id]

    def set_colliders(self, sprite_colliders):
        self.colliders = sprite_colliders

    def set_image_poses(self, image_positions):
        self.poses = image_positions


class Polygon:
    def __init__(self, points, pos=(0, 0)):
        self.points = []
        self.top = points[0][1]
        self.bottom = points[0][1]
        for point in points:
            if point[1] < self.top:
                self.top = point[1]
            if point[1] > self.bottom:
                self.bottom = point[1]
            self.points.append([round(point[0]) + pos[0], round(point[1]) + pos[-1]])
        self.points.append(self.points[0])
        self.side_points, self.x_lines, self.y_lines = get_points(self.points) # sussy
        self.top += pos[1]
        self.bottom += pos[1]

    def collidepoint(self, point, side):
        try:
            lines = None
            if side == "x":
                lines = self.x_lines
            elif side == "y":
                lines = self.y_lines
            # print(lines[point[1]], 'y', point[1], 'x', point[0], player.hit_polygon.top)
            x1 = lines[point[1]][0]
            x2 = lines[point[1]][-1]
            if x1 < point[0] < x2:
                return True
            return False
        except KeyError:
            return False

    def get_collidepoint(self, point, side):
            try:
                lines = None
                if side == "x":
                    lines = self.x_lines
                elif side == "y":
                    lines = self.y_lines
                # print(lines[point[1]], 'y', point[1], 'x', point[0], player.hit_polygon.top)
                x1 = lines[point[1]][0]
                x2 = lines[point[1]][-1]
                if x1 < point[0] < x2:
                    return [x1, x2]
                return []
            except KeyError:
                return []

    def move_ip(self, x, y):
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
        self.texture1 = ctx.texture((0, 0), 4)
        self.texture2 = ctx.texture((0, 0), 4)
        self.render()

    def render(self):
        all_sprites.empty()
        objects.empty()
        walls.empty()
        tile_obj = dict()
        ti = self.tmxdata.get_tile_image_by_gid
        atlas_pos = dict()
        for tileset in self.tmxdata.tilesets:
            for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
                try:
                    tile = ti(gid)
                    size = self.objects_atlas.get_size()
                    copy = self.objects_atlas.copy()
                    self.objects_atlas = pygame.Surface((size[0] + tile.get_width(), max(size[1], tile.get_height())), pygame.SRCALPHA, 32)
                    self.objects_atlas.blit(copy, (0, 0))
                    self.objects_atlas.blit(tile, (size[0], 0))
                    atlas_pos[gid] = (size[0], 0, *tile.get_size())
                except IndexError:
                    pass
        pygame.image.save(self.objects_atlas, 'hren.png')
        for gid, colliders in self.tmxdata.get_tile_colliders():  # возвращает все объекты спрайтов
            print(gid, colliders, 'pen')
            tile_obj[gid] = colliders

        sprite_info.set_colliders(tile_obj)
        sprite_info.set_image_poses(atlas_pos)

        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        x_pos = x * self.tmxdata.tilewidth
                        y_pos = (y + 1) * self.tmxdata.tileheight - tile.get_size()[1]
                        self.map_image.blit(tile, (x_pos, y_pos))
                        if layer.name == 'Objects':
                            Walls(gid, x_pos, y_pos)

        for group in self.tmxdata.objectgroups:
            print(group, group.name)
            if group.name == 'Obstacles':
                for obj in group:
                    Obstacle(obj)

        Walls.source_size = self.objects_atlas.get_size()
        for wall in walls:  # perdelat'
            wall.convert_texture_pos()

        dirt_bytes = pygame.image.tostring(self.map_image, 'RGBA', False)
        self.texture1.release()
        self.texture1 = ctx.texture(self.map_image.get_size(), 4, bytes(dirt_bytes))
        self.texture1.use(location=1)
        dirt_bytes = pygame.image.tostring(self.objects_atlas, 'RGBA', False)
        self.texture2.release()
        self.texture2 = ctx.texture(self.objects_atlas.get_size(), 4, bytes(dirt_bytes))
        self.texture2.use(location=2)

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
        self.objects_atlas = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
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

    def __init__(self, texture_size, x, y):
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.sprite_size = texture_size[0] / 4, texture_size[1] / 5
        self.texture_pos = convert_texture_pos((0, 0, *self.sprite_size), Player.source_size)
        self.pos = [x, y]
        self.rect = pygame.Rect(0, 0, *self.sprite_size)
        self.rect.topleft = self.pos

        self.hit_polygon_height = 24
        self.hit_polygon = pygame.Rect(self.rect.left, self.rect.bottom - self.hit_polygon_height, self.rect.width, self.hit_polygon_height)
        self.hit_polygon_pos = [*self.hit_polygon.topleft]
        self.hit_polygon_x = 0 # Положение относительно верхней левой точки игрока
        self.hit_polygon_y = self.rect.height - self.hit_polygon_height

        self.interaction_box_width = self.sprite_size[0] * 0.75
        self.interaction_box_height = self.hit_polygon.height * 5
        self.interaction_box_width2 = self.hit_polygon.height * 3
        self.interaction_box_height2 = self.hit_polygon.height

        self.interaction_box = pygame.Rect(0, 0, self.interaction_box_width, self.interaction_box_height)
        self.interaction_box.midbottom = self.rect.midbottom
        self.interaction_box_pos = [*self.interaction_box.topleft]
        self.vel = (0, 0)
        self.half_height = self.rect[3] / 2
        self._layer = self.rect.bottom

        self.direction = 'left'
        self.front = convert_texture_pos((0, 0, *self.sprite_size), Player.source_size)
        self.back = convert_texture_pos((self.sprite_size[0] * 2, 0, *self.sprite_size), Player.source_size)
        self.left = convert_texture_pos((self.sprite_size[0] * 3, 0, *self.sprite_size), Player.source_size)
        self.right = convert_texture_pos((self.sprite_size[0], 0, *self.sprite_size), Player.source_size)

        self.inventory = []

    def turn_right(self):
        self.direction = 'right'
        self.texture_pos = self.right
        self.interaction_box.size = (self.interaction_box_width2, self.interaction_box_height2)
        self.interaction_box.midleft = self.hit_polygon.bottomright
        self.interaction_box_pos = list(self.interaction_box.topleft)

    def turn_left(self):
        self.direction = 'left'
        self.texture_pos = self.left
        self.interaction_box.size = (self.interaction_box_width2, self.interaction_box_height2)
        self.interaction_box.midright = self.hit_polygon.bottomleft
        self.interaction_box_pos = list(self.interaction_box.topleft)

    def turn_down(self):
        self.direction = 'down'
        self.texture_pos = self.front
        self.interaction_box.size = (self.interaction_box_width, self.interaction_box_height)
        self.interaction_box.topleft = self.hit_polygon.bottomleft
        self.interaction_box_pos = list(self.interaction_box.topleft)

    def turn_up(self):
        self.direction = 'up'
        self.texture_pos = self.back
        self.interaction_box.size = (self.interaction_box_width, self.interaction_box_height)
        self.interaction_box.bottomleft = self.hit_polygon.topleft
        self.interaction_box_pos = list(self.interaction_box.topleft)

    def get_keys(self, events):
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_l:
                    self.interaction(screen_objects)
                if event.key == pygame.K_UP:
                    self.tp(self.hit_polygon.x, self.hit_polygon.y - 1)
                if event.key == pygame.K_DOWN:
                    self.tp(self.hit_polygon.x, self.hit_polygon.y + 1)
                if event.key == pygame.K_LEFT:
                    self.tp(self.hit_polygon.x - 1, self.hit_polygon.y)
                if event.key == pygame.K_RIGHT:
                    self.tp(self.hit_polygon.x + 1, self.hit_polygon.y)

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.vel = (-speed, 0)
                    self.turn_left()

                elif keys[pygame.K_d]:
                    self.vel = (speed, 0)
                    self.turn_right()

                elif keys[pygame.K_w]:
                    self.vel = (0, -speed)
                    self.turn_up()

                elif keys[pygame.K_s]:
                    self.vel = (0, speed)
                    self.turn_down()

                elif not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
                    self.vel = (0, 0)

    def update(self, events):
        self.get_keys(events)
        x, y = self.vel[0] * dt, self.vel[1] * dt
        # print('--------------')
        # print(self.rect.bottom, self.hit_polygon.bottom, self.pos, self.hit_polygon_pos)
        self.pos[0] = round(self.pos[0] + x, 6)
        self.pos[1] = round(self.pos[1] + y, 6)
        # self.hit_polygon_pos[0] = round(self.hit_polygon_pos[0] + x, 6)
        # self.hit_polygon_pos[1] = round(self.hit_polygon_pos[1] + y, 6)
        self.interaction_box_pos[0] = round(self.interaction_box_pos[0] + x, 6)
        self.interaction_box_pos[1] = round(self.interaction_box_pos[1] + y, 6)

        self.rect.topleft = self.pos
        self.hit_polygon.topleft = (self.rect.x + self.hit_polygon_x, self.rect.y + self.hit_polygon_y)
        self.interaction_box.topleft = self.interaction_box_pos
        # print(self.rect.bottom, self.hit_polygon.bottom, self.pos, self.hit_polygon_pos)
        collide_with_walls(player, screen_sprites)

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
                # print(name)
                if name[0] == "file":
                    file = open("maps/special/" + name[1] + '.txt')
                    for n, line in enumerate(file.read().split('\n')):
                        act = line.split(' ')
                        # print(act)
                        if act[0] == 'chest':
                            try:
                                self.inventory.append(all_items[act[2]])
                            except KeyError:
                                print(f"Item {act[2]} does not exist in all_items")
                            except IndexError:
                                print(f" {line} Wrong format of object")
                            print(self.inventory)
                        elif act[0] == 'change':
                            x = int(act[1]) * map.tilewidth
                            y = int(act[2]) * map.tilewidth
                            for wall in walls:
                                if wall.rect.x == x and wall.rect.y == y:
                                    # print('wwww')
                                    # print(wall.texture_pos, wall.hit_polygon.points)
                                    replace_sprite_by_id(wall, int(act[4]))
                                    obj.data.name = "file " + act[5]
                        elif act[0] == 'door':
                            map.load_level("maps/" + act[2] + '.tmx')
                            for obj2 in objects:
                                try:
                                    name2 = obj2.data.name.split(' ')
                                except AttributeError:
                                    name2 = [None, None, None]
                                try:
                                    if name2[2] == name[2]:
                                        if name2[0] == 'file':
                                            file2 = open("maps/special/" + name[1] + '.txt')
                                            for n, line in enumerate(file2.read().split('\n')):
                                                act2 = line.split(' ')
                                                if act2[0] == 'door':
                                                    if act2[3] == "down":
                                                        pos = obj2.rect.midbottom
                                                        self.turn_down()
                                                        self.tp(pos[0] - self.hit_polygon.width / 2, pos[1] + map.tilewidth)
                                                    elif act2[3] == "up":
                                                        pos = obj2.rect.midtop
                                                        self.turn_up()
                                                        self.tp(pos[0] - self.hit_polygon.width / 2, pos[1] - self.hit_polygon.height - map.tilewidth)
                                                    elif act2[3] == "left":
                                                        pos = obj2.rect.midleft
                                                        self.turn_left()
                                                        self.tp(pos[0] - self.hit_polygon.width - map.tilewidth, pos[1] - self.hit_polygon.height / 2)
                                                    elif act2[3] == "right":
                                                        pos = obj2.rect.midright
                                                        self.turn_right()
                                                        self.tp(pos[0] + map.tilewidth, pos[1] - self.hit_polygon.height / 2)
                                            file2.close()
                                except IndexError:
                                    pass
                    file.close()
                break

    def tp(self, x, y):
        # print('---------ana')
        # print(self.rect.left, self.hit_polygon.left)
        # print(self.pos, self.hit_polygon_pos)
        delta_x = x - self.hit_polygon.topleft[0]
        delta_y = y - self.hit_polygon.topleft[1]
        self.rect.move_ip(delta_x, delta_y)
        self.hit_polygon.move_ip(delta_x, delta_y)
        self.interaction_box.move_ip(delta_x, delta_y)

        self.pos = list(self.rect.topleft)
        self.interaction_box_pos = list(self.interaction_box.topleft)
        # print(self.hit_polygon_pos[0], self.hit_polygon.topleft)

    def get_rect(self):
        return self.rect


class Walls(pygame.sprite.Sprite):
    source = None
    source_id = 2
    source_size = None

    def __init__(self, map_id, x, y):  # с помощью супера все созданные спрайты скидываю в группу спрайтов
        self.groups = all_sprites, walls
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.texture_pos = sprite_info.get_image_pos_by_id(map_id)
        # print(self.texture_pos)
        self.spite_size = self.texture_pos[2:]
        self.rect = pygame.Rect(0, 0, *self.spite_size)
        self.pos = [x, y]
        self.rect.topleft = self.pos
        self.vel = (0, 0)
        self._layer = self.rect.bottom
        self.hit_polygon = None
        self.down_layer = None
        for collider in sprite_info.get_collider_by_id(map_id):
            if collider.name == 'bottom_layer':
                self.down_layer = pygame.Rect(collider.x + x, collider.y + y, collider.width, collider.height)
            elif collider.name is None:
                try:
                    self.hit_polygon = Polygon(collider.points, self.pos)
                except AttributeError:
                    print(round(collider.x), round(collider.y), round(collider.width), round(collider.height))
                    self.hit_polygon = pygame.Rect(round(collider.x) + x, round(collider.y) + y, round(collider.width), round(collider.height))

    def get_rect(self):
        return self.rect

    def convert_texture_pos(self):
        self.texture_pos = convert_texture_pos(self.texture_pos, Walls.source_size)

    def set_sprite_pos(self, new_pos):
        self.texture_pos = new_pos
        self.spite_size = self.texture_pos[2:]
        self.rect = pygame.Rect(0, 0, *self.spite_size)
        self.rect.topleft = self.pos
        self.texture_pos = convert_texture_pos(new_pos, Walls.source_size)

    def set_sprite_colliders(self, new_colliders):
        for collider in new_colliders:
            if collider.name == 'bottom_layer':
                self.down_layer = pygame.Rect(collider.x + self.pos[0], collider.y + self.pos[1], collider.width, collider.height)
            elif collider.name is None:
                try:
                    self.hit_polygon = Polygon(collider.points, self.pos)
                except AttributeError:
                    self.hit_polygon = pygame.Rect(collider.x + self.pos[0], collider.y + self.pos[1], collider.width, collider.height)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, object):
        self.groups = all_sprites, objects
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.data = object
        print(self.data)
        self.rect = pygame.Rect(object.x, object.y, object.width, object.height)
        self.pos = [object.x, object.y]
        # print(self.rect)
        try:
            self.hit_polygon = Polygon(self.data.points)
        except AttributeError:
            self.hit_polygon = pygame.Rect(round(object.x), round(object.y), round(object.width), round(object.height))
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


class TextWindow:
    source_id = 4

    def __init__(self, filename, font, message):
        self.window = pygame.image.load(filename).convert_alpha()
        self.image = self.window.copy()
        self.font = font
        self.rect = self.image.get_rect()
        self.x = width / 2 - self.rect.width / 2
        self.y = height - self.rect.height
        self.texture_pos = convert_texture_pos(self.rect, self.rect.size)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vertices = get_vertices([self], screen_size)
        self.text = self.font.render(message, True, (255, 255, 255))
        self.image.blit(self.text, (20, 20))
        load_opengl_image(self.image, 4)

    def get_rect(self):
        return self.rect

    def set_text(self, message):
        self.image.blit(self.window, (0, 0))
        self.text = self.font.render(message, True)
        self.image.blit(self.text, (20, 20))

        
pygame.init()

width = 1920
height = 1016
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size, pygame.DOUBLEBUF | pygame.OPENGL)
ctx = moderngl.create_context()
ctx.enable(moderngl.BLEND)
camera = Camera(width, height)
clock = pygame.time.Clock()

prog = ctx.program(
            vertex_shader="""
            #version 430
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
            #version 430
            out vec4 fragColor;
            uniform sampler2D u_texture;
            uniform sampler2D u_texture2;
            uniform sampler2D u_texture3;
            uniform sampler2D u_texture4;
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
                else if (int(v_num) == 4) {
                    fragColor = texture(u_texture4, vec2(v_uv[0], -v_uv[1]));
                }
            }
            """)

set_uniform('u_texture', 1)
set_uniform('u_texture2', 2)
set_uniform('u_texture3', 3)
set_uniform("u_texture4", 4)

game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')

all_sprites = pygame.sprite.LayeredUpdates()
walls = pygame.sprite.Group()  # все стены
objects = pygame.sprite.Group()  # все объекты
screen_sprites = ScreenGroup()  # только стены, которые на экране
screen_objects = ScreenGroup()  # объекты, которые на экране

font = pygame.font.Font("data/fonts/Undertale-Battle-Font.ttf", 26)


player_sprite = pygame.image.load('data/hero.png').convert_alpha()
bytes_player_image = pygame.image.tostring(player_sprite, 'RGBA', False)
player_texture = ctx.texture(player_sprite.get_size(), 4, bytes(bytes_player_image))
player_texture.use(location=3)
Player.source_size = player_sprite.get_size()


text_window = TextWindow("data/general/dialog_window.png", font, "W A S D - move | l - interaction | Space - close text window")

sprite_info = SpriteInfo(None, None)
map = TiledMap('maps/test.tmx')
player = Player(player_sprite.get_size(), width / 2 - player_sprite.get_size()[0] / 2, height / 2 - player_sprite.get_size()[1] / 2)

pause = False
save_process = False
dialog_event = True

running = True
fps = 2000
speed = 300
time = 0
sec = 0
dt = 0  # коэффицент который зависит от FPS и определяет скорость персонажа

display_info()
player.update([])
camera.update(player)
screen_sprites.sprites_update(walls)
screen_objects.sprites_update(objects)

print('end')
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                dialog_event = False
            if keys[pygame.K_LCTRL] and keys[pygame.K_DOWN]:
                save_process = True
                pygame.display.set_caption("Save the game? 1 - Yes 2 - No")
            elif keys[pygame.K_LCTRL] and keys[pygame.K_l]:
                load_game()

    if save_process:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            save_game()
            save_process = False
        elif keys[pygame.K_2]:
            save_process = False
        pygame.display.set_caption("pygame window")

    else:
        ctx.clear(0, 0, 0, 1)
        draw_with_layers(map, screen_sprites, player)
        if dialog_event:
            pass
        else:
            player.update(events)
            camera.update(player)
            screen_sprites.sprites_update(walls)
            screen_objects.sprites_update(objects)

    dt = clock.tick(fps) / 1000
    pygame.display.flip()



















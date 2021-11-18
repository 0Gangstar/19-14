class Hero(Sprite):
    def __init__(self, image, x, y, base, *group):
        super().__init__(image, x, y, base, *group)
        self.x = x
        self.y = y
        self.sprite_now = 0
        self.hor_animation_speed = 2 / 32
        self.ver_animation_speed = 2 / 32
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
                elif self.sprite_now >= 12:
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

import pygame as pg
import random
from settings import *


class Spaceship(pg.sprite.Sprite):
    def __init__(self, pos, image, damage, thruster, shield):
        super().__init__()
        self.image = image
        self.damage = damage
        self.rect = image.get_rect()
        self.start_pos = pos
        self.rect.center = pos
        self.hp = 4
        self.score = 0
        self.DESTROY = pg.USEREVENT + 1

        self.thruster = thruster
        self.frame = 0

        self.shield_power = 0
        self.shield_images = shield
        self.shield_rect = shield[0].get_rect()





    def draw(self, surf: pg.Surface):
        self.draw_shield(surf)
        self.draw_thruster(surf)
        if self.hp > 0:
            surf.blit(self.image, self.rect)
            if self.hp < 4:
                surf.blit(self.damage[-self.hp + 1], self.rect, special_flags=pg.BLEND_RGBA_SUB)

    def draw_thruster(self, surf):
        self.frame += 0.3
        if self.frame >= len(self.thruster):
            self.frame = 0
        img = self.thruster[int(self.frame)]

        pos_1 = (self.rect.centerx - 35, self.rect.bottom - 18)
        pos_2 = (self.rect.centerx + 21, self.rect.bottom - 18)
        pos_3 = (self.rect.centerx - 7, self.rect.bottom)

        surf.blit(img, pos_1)
        surf.blit(img, pos_2)
        surf.blit(img, pos_3)

    def draw_shield(self, surf):
        if self.shield_power > 0:
            self.shield_rect.center = self.rect.center
            if self.shield_power != 1:
                self.shield_rect.move_ip((-5, -5))

            surf.blit(self.shield_images[self.shield_power - 1], self.shield_rect)

    def get_damage(self):
        if self.shield_power > 0:
            self.shield_power -= 1
        else:
            self.hp -= 1
            if self.hp == 0:
                pg.event.post(pg.event.Event(self.DESTROY))

    def rebuild(self):
        self.rect.center = self.start_pos
        self.hp = 4
        self.score = 0

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y -= 6
        if keys[pg.K_s]:
            self.rect.y += 6
        if keys[pg.K_a]:
            self.rect.x -= 6
        if keys[pg.K_d]:
            self.rect.x += 6
        self.move_ship()

    def move_ship(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.x <= 0:
            self.rect.x = 0

    def apply_shield(self):
        self.shield_power = 3

    def apply_star(self):
        if self.hp < 4:
            self.hp += 1

class Metiors(pg.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = image.get_rect()
        self.angle = 0
        self.rotation_speed = random.randint(-3, 3)

        self.rect.center = pos
        self.speed_x, self.speed_y = random.randint(-5, 5), random.randint(1, 5)

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()

    def rotate(self):
        self.angle += self.rotation_speed
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Button:
    def __init__(self, pos, text, font):
        self.image = pg.Surface((240, 90))
        self.image.fill(pg.Color("white"))
        self.rect = self.image.get_rect(center=pos)

        self.text_surf, self.text_rect = font.render(text, size=42)
        self.text_rect.center = self.rect.center

    def draw(self, surf: pg.Surface):
        surf.blit(self.image, self.rect)
        surf.blit(self.text_surf, self.text_rect)


class PowerUp(pg.sprite.Sprite):
    def __init__(self, image, type_):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), -10))
        self.type = type_

    def update(self):
        self.rect.y += 4
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()


class Laser(pg.sprite.Sprite):
    def __init__(self, pos, images):
        super().__init__()

        self.frame = 0
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 14

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()

        self.frame += 0.25
        if self.frame == len(self.images):
            self.frame = 0
        self.image = self.images[int(self.frame)]

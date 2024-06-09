import os
import random

import pygame as pg
import scripts as s
from settings import *
from pygame import freetype


def draw():
    soup.draw(screen)
    meteors.draw(screen)
    laser_group.draw(screen)
    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    main_font.render_to(screen, (88, 24), str(soup.hp), pg.Color("orange"))
    main_font.render_to(screen, (SCREEN_WIDTH - 180, 24), str(soup.score).zfill(5), pg.Color("orange"))
    powerups_group.draw(screen)


def draw_menu():
    screen.fill(pg.Color("black"))
    button_res.draw(screen)


def update():
    soup.move()
    meteors.update()
    laser_group.update()
    soup_collide()
    laser_collide()
    powerups_group.update()
    powerup_collusion()


def make_metiors():
    meteors.add(
        s.Metiors(
            (random.randint(0, SCREEN_WIDTH), -20),
            random.choice(meteor_images)
        )
    )


def make_powerup():
    powerup = random.choice(powerups)
    powerups_group.add(s.PowerUp(**powerup))


def res_game():
    pg.mouse.set_visible(False)
    pg.mixer.music.play(-1)
    soup.rebuild()
    new_game_sound.play()


def stop_game():
    pg.mixer.music.fadeout(5000)
    pg.mouse.set_visible(True)
    meteors.empty()
    laser_group.empty()


def make_laser():
    fire_laser_sound.play()
    laser_group.add(s.Laser(soup.rect.center, laser_image))


def soup_collide():
    if pg.sprite.spritecollide(soup, meteors, True):
        shield_lost_sound.play()
        soup.get_damage()


def laser_collide():
    for laser in laser_group:
        if pg.sprite.spritecollide(laser, meteors, True):
            hit_m_sound.play()
            laser.kill()
            soup.score += 1


def powerup_collusion():
    powerup: s.PowerUp = pg.sprite.spritecollideany(soup, powerups_group)
    if powerup is None:
        return
    if powerup.type == "shield":
        soup.apply_shield()
        powerup.kill()
    elif powerup.type == "star":
        soup.apply_star()
        powerup.kill()
    elif powerup.type == "bolt":
        max_lasers = 9
        powerup.kill()


# Иницализация окна
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Asteroids')
game_state = "GAME"

# Sounds
fire_laser_sound = pg.mixer.Sound("Bonus/sfx_laser2.ogg")
hit_m_sound = pg.mixer.Sound("Bonus/sfx_laser1.ogg")
shield_lost_sound = pg.mixer.Sound("Bonus/sfx_shieldDown.ogg")
game_over_sound = pg.mixer.Sound("Bonus/sfx_lose.ogg")
new_game_sound = pg.mixer.Sound("Bonus/sfx_twoTone.ogg")
pg.mixer.music.load("Bonus/Minima (2).mp3")
pg.mixer.music.play(-1)
# Game objects
thruster_images = [pg.image.load(f"PNG/Effects/fire{i}.png") for i in range(11, 18)]
shield_images = [pg.image.load(f"PNG/Effects/shield{i}.png") for i in range(1, 4)]
soup = s.Spaceship(
    (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 45),
    pg.image.load("PNG/playerShip2_orange.png"),
    [pg.image.load(f"PNG/Damage/playerShip2_damage{i}.png") for i in range(1, 4)],
    thruster_images, shield_images

)

powerups = [
    {
        "image": pg.image.load("PNG/Power-ups/shield_silver.png"),
        "type_": "shield"
    },
    {
        "image": pg.image.load("PNG/Power-ups/star_silver.png"),
        "type_": "star"

    },
    {
        "image": pg.image.load("PNG/Power-ups/powerupRed_bolt.png"),
        "type_": "bolt"
    }
]

hp_img = pg.image.load("PNG/UI/playerLife2_orange.png")
x_img = pg.image.load("PNG/UI/numeralX.png")
main_font = pg.freetype.Font("Bonus/kenvector_future.ttf", 32)
button_res = s.Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), "RESTART", main_font)

backgrounds = pg.image.load("Backgrounds/black.png")
backgrounds = pg.transform.scale(backgrounds, (SCREEN_WIDTH, SCREEN_HEIGHT))
meteor_images = [pg.image.load("PNG/Meteors/" + i) for i in os.listdir("PNG/Meteors")]
meteors = pg.sprite.Group()

pg.mouse.set_visible(False)

meteors.add(
    s.Metiors((0, 0), meteor_images[0])
)

laser_image = [pg.image.load(f"PNG/Lasers/laserBlue{str(i).zfill(2)}.png") for i in range(8, 12)]
laser_group = pg.sprite.GroupSingle()
max_lasers = 1

powerups_group = pg.sprite.Group()
SPAWN_METEOR = pg.USEREVENT
SPAWN_POWERUPS = pg.USEREVENT + 2
pg.time.set_timer(SPAWN_METEOR, 1000)
pg.time.set_timer(SPAWN_POWERUPS, 3000)
# Игровой цикл
running = True
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if game_state == "GAME":
            if event.type == pg.MOUSEBUTTONDOWN:
                if len(laser_group) <= max_lasers - 1:
                    make_laser()
            if event.type == SPAWN_METEOR:
                make_metiors()
            if event.type == soup.DESTROY:
                game_state = "MENU"
                stop_game()
            if event.type == SPAWN_POWERUPS:
                make_powerup()
        else:
            if event.type == pg.MOUSEBUTTONDOWN and button_res.rect.collidepoint(event.pos):
                game_state = "GAME"
                res_game()

    screen.blit(backgrounds, (0, 0))

    if game_state == "GAME":
        update()
        draw()
    else:
        draw_menu()

    dt = clock.tick(60) / 1000
    pg.display.update()
pg.quit()

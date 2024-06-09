import pygame as p

class Frog(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animate = False
        self.sprites = [p.image.load(f"frog/Frog/attack_{i}.png") for i in range (1, 11)]
        self.frame = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect()

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self):
        if self.animate:
            self.frame += 0.25
            if self.frame == len(self.sprites):
                self.frame = 0
                self.animate = False
            self.image = self.sprites[int(self.frame)]



SCREEN_WIDTH = 300

SCREEN_HEIGHT = 300
p.init()
clock = p.time.Clock()
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Frog')
running = True

frog = Frog()

while running:

    for event in p.event.get():

        if event.type == p.QUIT or (event.type == p.KEYDOWN

                                    and event.key == p.K_ESCAPE):
            running = False
        if event.type == p.MOUSEBUTTONDOWN:
            frog.animate = True
    frog.update()

    screen.fill((255, 255, 255))
    frog.draw(screen)
    clock.tick(60)

    p.display.flip()
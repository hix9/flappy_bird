import pygame

from constants import FLYING, FLAP_COLLDOWN


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in FLYING:
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self, flying, game_over):
        if flying is True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        if game_over is False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            # handle the animation
            self.counter += 1
            if self.counter > FLAP_COLLDOWN:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            # rotate the bird
            self.image = pygame.transform.rotate(
                self.images[self.index], self.vel * -2
            )
        else:
            self.image = pygame.transform.rotate(
                self.images[self.index], -90
            )

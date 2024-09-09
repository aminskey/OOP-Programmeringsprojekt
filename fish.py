from variables import *
from math import degrees
import random
from vector import Vector

class Bubble(pygame.sprite.Sprite):
    def __init__(self, screen, pos, sizeF=1):
        super().__init__()
        self.screen = screen
        self.image = pygame.transform.scale_by(pygame.image.load("assets/misc/bubble.png"), sizeF)
        self.rect = self.image.get_rect()

        self.rect.topleft = pos
    def update(self):
        if self.rect.midbottom[1] > 0:
            self.rect.y -= 1
        else:
            self.rect.y = self.screen.get_height()
            self.rect.x = random.randint(0, self.screen.get_width())

class Fish(pygame.sprite.Sprite):
    def __init__(self, screen, image, sizeF, v=(0, 0)):
        super().__init__()
        self.screen = screen
        self.base_image = pygame.transform.scale_by(pygame.image.load(image), sizeF)
        self.image = self.base_image.copy()

        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))

        if v[0] != 0 and v[1] != 0:
            self.__vel = Vector(v[0], v[1])
        else:
            self.__vel = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
    def borderHandle(self):
        if not isInRange(self.rect.centerx, self.base_image.get_width(), 0, self.screen.get_width()):
            self.__vel.x = -self.__vel.x
            self.vel.y *= random.randint(-3, 3) / 5
            self.rect.centerx += self.__vel.x * 2

        if not isInRange(self.rect.centery, self.base_image.get_height(), 0, self.screen.get_height()):
            self.__vel.y = -self.__vel.y
            self.rect.centery += self.__vel.y*2
    def screenConfinement(self, d=30):
        if not isInRange(self.rect.centerx, self.base_image.get_width() + d, 0, self.screen.get_width()):
            self.__vel.x += 1-(self.rect.x/(d*10))
        if not isInRange(self.rect.centery, self.base_image.get_height() + d, 0, self.screen.get_height()):
            self.__vel.y += 1-(self.rect.y/(d*10))

    def update(self):
        self.screenConfinement()
        if self.__vel.x < 0:
            tmp = pygame.transform.flip(self.base_image, False, True)
        else:
            tmp = self.base_image.copy()
        self.image = pygame.transform.rotate(tmp, -degrees(self.__vel.polar360))

        if self.rect.centery < 0 or self.rect.centery > self.screen.get_height():
            self.rect.centery = self.screen.get_rect().centery

        self.rect.centerx += self.__vel.x * dTime
        self.rect.centery += self.__vel.y * dTime
    def draw(self):
        self.screen.blit(self.image, self.rect)

    @property
    def angle(self):
        return self.__vel.polar360

    @property
    def pos(self):
        return self.rect.center

    @property
    def vel(self):
        return self.__vel

    @vel.setter
    def vel(self, others):
        self.__vel = others

class Flock:
    def __init__(self, l):
        self.list = l

    def update(self):
        for i in self.list:
            i.update()
            print(i.vel.length, end=" ")
        print(" ")

    def draw(self):
        for i in self.list:
            i.draw()

    @property
    def length(self):
        return len(self.list)
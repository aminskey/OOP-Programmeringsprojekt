import pygame.mouse

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
    def __init__(self, screen, image, sizeF, v=(0, 0), vis=30):
        super().__init__()
        self.screen = screen
        self.base_image = pygame.transform.scale_by(pygame.image.load(image), sizeF)
        self.image = self.base_image.copy()
        self.parent = None

        self.pos = Vector(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
        self.center = self.pos + Vector(self.image.get_width()//2, self.image.get_height()//2)
        self.vision = vis
        self.maxSpeed = 7
        self.maxForce = 10

        if v[0] != 0 and v[1] != 0:
            self.__vel = Vector(v[0], v[1])
        else:
            self.__vel = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
    def screenConfinement(self):
        if not isInRange(self.center.x, self.base_image.get_width() + self.vision, 0, self.screen.get_width()):
            self.__vel.x += 1 - (self.center.x/(self.vision*10))**2
            #self.__vel.y += random.randint(-10, 10) % 3
        if not isInRange(self.center.y, self.base_image.get_height() + self.vision, 0, self.screen.get_height()):
            self.__vel.y += 1 - (self.center.y/(self.vision*10))**2
            self.__vel.x += random.randint(-10, 10)/10

    def screenConfinement2(self):
        if not isInBounds(self.pos.tuple, self.base_image.get_height(), (0, 0), self.screen.get_size()):
            self.__vel = Vector(pygame.mouse.get_pos()[0] - self.pos.x, pygame.mouse.get_pos()[1] - self.pos.y)
            self.__vel /= self.__vel.length

    def screenLoop(self):
        if self.pos.x + self.image.get_width() < 0:
            self.pos.x = self.screen.get_width()
        elif self.pos.x > self.screen.get_width():
            self.pos.x = -self.image.get_width()

        if self.pos.y > self.screen.get_height():
            self.pos.y = -self.image.get_height()
        elif self.pos.y < -self.image.get_height():
            self.pos.y = self.screen.get_height()

    """
        * Boids Algorithm
            - Seperation
            - Alignment
            - Cohesion
    """
    # seperation part of the algorithm.
    def separation(self, tooClose: int, separation_factor: float):
        sepVec = Vector(0, 0)
        count = 0

        # iterate through fish in parent list
        for fish in self.parent.list:
            if fish is not self:
                # if the fish is too close
                if dist(self.center, fish.pos) < tooClose:
                    # get a vector describing the distance between each fish
                    tmp = self.pos - fish.pos

                    tmp = tmp.normalize()

                    # divide by the distance to weight it by the distance
                    tmp /= dist(self.pos, fish.pos)

                    # add the tmp vector to seperation vector
                    sepVec += tmp

                    # increment number of encountered fish
                    count += 1
        # if the count > 0 then divide sepVec by count
        if count > 0:
            sepVec /= count

        # return the vector / factor to create proper weighting.
        return sepVec * separation_factor

    def alignment(self, al_factor):
        avg_vel = Vector(0, 0)
        count = 0
        for fish in self.parent.list:
            if fish != self:
                avg_vel += fish.vel
                count += 1
        if count > 0:
            avg_vel /= count
            avg_vel = avg_vel.normalize() * self.maxSpeed
        return avg_vel * al_factor

    def isIsolated(self, isol_dist):
        for fish in self.parent.list:
            if fish != self:
                dist = self.pos - fish.pos
                if dist.length < isol_dist:
                    return False
        return True

    def steer(self, target: Vector):
        des = target - self.pos
        des = des.normalize() * self.maxSpeed

        steer = des - self.__vel
        steer.limit(self.maxForce) # self.maxForce

        return steer

    def cohesion(self, cohesion_factor: float, isol_dist: int):
        if self.isIsolated(isol_dist):
            return Vector(0, 0)
        avg_pos = Vector(0, 0)
        count = 0

        for fish in self.parent.list:
            if fish != self:
                avg_pos += fish.pos
                count += 1

        if count > 0:
            avg_pos /= count
            v = self.pos - avg_pos
            v = v.normalize() * self.maxSpeed
            sVec = self.steer(self.vel - v)
            sVec.limit(self.maxForce)
            return sVec * cohesion_factor
        return Vector(0, 0)


    def update(self):
        self.screenConfinement()
        #self.screenConfinement2()
        self.center = self.pos + Vector(self.image.get_width() // 2, self.image.get_height() // 2)

        self.__vel += self.separation(self.image.get_width(), 10)
        self.__vel += self.alignment(0.05)
        self.__vel += self.cohesion(0.01, 100)
        #self.__vel -= (self.pos - Vector(self.screen.get_width()//2, self.screen.get_height()//2)).normalize() * 0.5

        if self.__vel.x < 0:
            tmp = pygame.transform.flip(self.base_image, False, True)
        else:
            tmp = self.base_image.copy()
        self.image = pygame.transform.rotate(tmp, -degrees(self.__vel.polar360))

        """
        if not isInBounds(self.center.tuple, 0, (0, 0), self.screen.get_size()):
            self.pos = Vector(self.screen.get_rect().centerx, self.screen.get_rect().centery)
            self.__vel %= 3
        """

        if self.__vel.length > self.maxSpeed:
            self.__vel /= self.__vel.length*0.25

        self.pos += self.__vel * dTime
    def draw(self):
        self.screen.blit(self.image, self.pos.tuple)

    @property
    def angle(self):
        return self.__vel.polar360

    @property
    def vel(self):
        return self.__vel

    @vel.setter
    def vel(self, others):
        self.__vel = others

class Flock:
    def __init__(self, l):
        self.list = l
        for fish in self.list:
            fish.parent = self

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
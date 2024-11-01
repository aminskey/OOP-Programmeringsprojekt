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

class Fish:
    def __init__(self, screen, image, sizeF, v=(0, 0), vis=30):
        self.screen = screen
        self.base_image = pygame.transform.scale_by(pygame.image.load(image), sizeF)
        self.image = self.base_image.copy()
        self.parent = None

        self.pos = Vector(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
        self.center = self.pos + Vector(self.image.get_width()//2, self.image.get_height()//2)
        self.vision = vis
        self.maxSpeed = 7
        self.maxForce = 10

        self.sep = 5
        self.alig = 0.05
        self.coh = 0.01

        if v[0] != 0 and v[1] != 0:
            self.__vel = Vector(v[0], v[1])
        else:
            self.__vel = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
    def screenConfinement(self):
        if self.pos.x < self.vision:
            self.vel.x += (1 - self.pos.x/self.vision)**2
        if self.pos.x - self.screen.get_width() > self.vision:
            self.vel.x -= (1-(self.pos.x - self.screen.get_width())/self.vision)**2

        if self.pos.y < self.vision:
            self.vel.y += (1 - self.pos.y/self.vision)**2
        if self.pos.y - self.screen.get_height() > self.vision:
            self.vel.y -= (1 - (self.pos.y - self.screen.get_height())/self.vision)**2
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
    def separation(self, list, tooClose: int, separation_factor: float):
        sepVec = Vector(0, 0)
        count = 0

        # iterate through fish in parent list
        for fish in list:
            if fish is not self:
                # if the fish is too close
                if dist(self.center, fish.center) < tooClose:
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


    def alignment(self, list, al_factor):
        avg_vel = Vector(0, 0)
        count = 0
        for fish in list:
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
        # des is vector to destination.
        des = target - self.pos
        des = des.normalize() * self.maxSpeed

        steerVec = des - self.__vel
        steerVec.limit(self.maxForce) # self.maxForce

        return steerVec

    def cohesion(self, list, cohesion_factor: float, isol_dist: int):
        if self.isIsolated(isol_dist):
            #return self.pos
            return Vector(0, 0)
        avg_pos = Vector(0, 0)
        count = 0

        for fish in list:
            if fish != self:
                avg_pos += fish.pos
                count += 1

        if count > 0:
            avg_pos /= count
            avg_pos = (avg_pos - self.pos)*cohesion_factor
            """
            v: Vector = self.pos - avg_pos
            v = v.normalize() * self.maxSpeed
            sVec : Vector = self.steer(v - self.vel)
            sVec.limit(self.maxForce)
            return sVec * cohesion_factor
            """
        return avg_pos


    def update(self, *args, **kwargs):
        self.screenConfinement()
        #self.screenLoop()
        self.center = self.pos + Vector(self.image.get_width() // 2, self.image.get_height() // 2)

        self.__vel += self.separation(self.parent.list, self.image.get_width(), self.sep)
        self.__vel += self.alignment(self.parent.list, self.alig)
        self.__vel += self.cohesion(self.parent.list, self.coh, 100)

        if self.__vel.x < 0:
            tmp = pygame.transform.flip(self.base_image, False, True)
        else:
            tmp = self.base_image.copy()

        self.image = pygame.transform.rotate(tmp, -degrees(self.__vel.polar360))

        if self.__vel.length > self.maxSpeed:
            self.__vel /= self.__vel.length*0.25

        self.pos += self.__vel * dTime
    def draw(self):
        self.screen.blit(self.image, self.pos.tuple)

    @property
    def vel(self):
        return self.__vel

    @vel.setter
    def vel(self, others):
        self.__vel = others

class FoodFish(Fish):
    def __init__(self, screen, image, sizeF, v=(0, 0), vis=30):
        super().__init__(screen, image, sizeF, v, vis)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.vel += self.separation(kwargs["sharkFlock"].list, self.image.get_width()*3, 1)

class Shark(Fish):
    def __init__(self, screen, sizeF, v=(0, 0), vis=30):
        super().__init__(screen, "assets/fish/Sharks/shark_standard.png", sizeF, v, vis)
        self.__hungry = pygame.transform.scale(pygame.image.load("assets/fish/Sharks/shark_hungry.png"), self.base_image.get_size())
        self.__copy = self.base_image.copy()

        self.b_right = Vector(0, 0)

        self.maxSpeed = 4
        self.maxForce = 3

    def update(self, *args, **kwargs):

        # bottom_right position
        self.b_right = self.pos + Vector(self.image.get_width(), self.image.get_height())

        if len(kwargs["foodFlock"].list) > 0:
            if distToCenter(kwargs["foodFlock"], self.pos) < max(self.image.get_width(), self.image.get_height()) * 1.5:
                self.base_image = self.__hungry.copy()
            else:
                self.base_image = self.__copy.copy()
        else:
            self.base_image = self.__copy.copy()

        for fish in kwargs["foodFlock"].list:
            if isInBounds(fish.center.tuple, 0, (self.pos + Vector(self.image.get_width() - 10, 0)).tuple, self.b_right.tuple):
                kwargs["foodFlock"].list.remove(fish)
                tmp = Shark(self.screen, random.randint(5,10)/10)
                tmp.parent = self.parent
                self.parent.list.append(tmp)

        super().update(*args, **kwargs)
        #self.vel += self.cohesion(kwargs["foodFlock"].list, 0.01, 10)
        self.vel -= self.separation(kwargs["foodFlock"].list, 100, 10)


class Flock:
    def __init__(self, l: list):
        self.list = l
        for fish in self.list:
            fish.parent = self

    def update(self, *args, **kwargs):
        for i in self.list:
            i.update(*args, **kwargs)
            print(i.vel.length, end=" ")
        print(" ")

    def draw(self):
        for i in self.list:
            i.draw()

    def setattrall(self, attr, val):
        for i in self.list:
            if hasattr(i, attr):
                setattr(i, attr, val)

    @property
    def length(self):
        return len(self.list)


def distToCenter(flock: Flock, pos: Vector):
    avg_pos = Vector(0, 0)

    for i in flock.list:
        avg_pos += i.pos

    if len(flock.list) > 0:
        avg_pos /= len(flock.list)
    else:
        return 0
    return dist(pos, avg_pos)
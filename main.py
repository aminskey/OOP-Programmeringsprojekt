import random
import pygame

from vector import Vector
from pygame.locals import *
from math import degrees
from os import listdir
from variables import *
from fish import Fish, Bubble, Flock

pygame.init()
screen = pygame.display.set_mode((600, 400), SCALED | FULLSCREEN)
pygame.display.set_caption("Fish - Testing Vectors")

clock = pygame.time.Clock()
flock = Flock([])

def main():
    global flock
    for i in range(10):
        f = random.choice(listdir("./assets/fish"))
        tmp = Fish(screen, f"./assets/fish/{f}",
                   random.randrange(1, 5)/10,
                   (random.randint(0, screen.get_width()),
                    random.randint(0, screen.get_height())),
                   random.randint(-1, 2),
                   random.randint(0, 2)
                   )
        bub = Bubble(screen,
            (
                random.randint(0, screen.get_width()),
                random.randint(0, screen.get_height())
            ),
            random.randint(25, 125)/100
        )
        flock.list.append(tmp)
        if not pygame.sprite.spritecollideany(bub, bubbleGrp):
            bub.add(bubbleGrp)
            if i % 3 == 0:
                frontBub.add(bub)
            else:
                bub.image.set_alpha(200)
                backBub.add(bub)

    bg = pygame.Surface(screen.get_size())
    bg.fill(BLUE)
    bg.set_alpha(150)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
                break

        flock.update()
        bubbleGrp.update()

        screen.blit(bg, (0, 0))
        backBub.draw(screen)
        flock.draw()
        frontBub.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

        print(clock.get_fps())

    pygame.quit()

if __name__ == "__main__":
    main()

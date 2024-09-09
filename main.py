import pygame
import random

from pygame.locals import *
from variables import *
from fish import Fish, Bubble, Flock
from os import listdir

pygame.init()
screen = pygame.display.set_mode((600, 400), SCALED | FULLSCREEN)
pygame.display.set_caption("Fish - Testing Vectors")

clock = pygame.time.Clock()

def main():

    flock = Flock([Fish(screen, f"./assets/fish/{random.choice(listdir('./assets/fish'))}", random.randrange(1, 5)/10) for i in range(10)])

    global dTime

    for i in range(10):
        bub = Bubble(screen,
            (
                random.randint(0, screen.get_width()),
                random.randint(0, screen.get_height())
            ),
            random.randint(25, 125)/100
        )
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

        try:
            dTime = stdFPS/clock.get_fps()
            print(dTime)
        except:
            dTime = stdFPS/FPS

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

import pygame
import random
import time

import pygame_widgets
from pygame.locals import *
from variables import *
from fish import *
from os import listdir
from slider import Slider_w_labels


pygame.init()
screen = pygame.display.set_mode((600, 400), SCALED | FULLSCREEN)
pygame.display.set_caption("Fish - Testing Vectors")

clock = pygame.time.Clock()

def main():

    preyflock = Flock([FoodFish(screen, f"./assets/fish/Prey/{random.choice(listdir('./assets/fish/Prey'))}", random.randrange(1, 3)/10, vis=random.randint(20,30)) for i in range(12)])
    sharks = Flock([Shark(screen, 2, vis=random.randint(20, 30)) for i in range(2)])

    first_shark = sharks.list[-1]

    names = ["sep", "alig", "coh"]
    sliders = [Slider_w_labels(screen, i, 0, 10, 0.01, names[i]) for i in range(len(names))]

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

    startTime = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                    break
                if event.key == pygame.K_r:
                    preyflock.list.clear()
                    sharks.list.clear()
                    break
                if event.key == pygame.K_t:
                    preyflock.list.clear()
                    sharks.list.clear()

                    first_shark.pos = Vector(screen.get_width()//2, screen.get_height()//2)
                    first_shark.vel = Vector(1,1)
                    sharks.list.append(first_shark)
                    break
        try:
            dTime = stdFPS/clock.get_fps()
            print(dTime)
        except:
            dTime = stdFPS/FPS

        currTime = time.time()
        if (currTime - startTime) > 3:
            for i in range(random.randint(1, 10)):
                tmp = FoodFish(screen, f"./assets/fish/Prey/{random.choice(listdir('./assets/fish/Prey'))}", random.randrange(1, 3)/10, vis=random.randint(20,30))
                tmp.parent = preyflock
                preyflock.list.append(tmp)
                startTime = currTime

        pygame_widgets.update(pygame.event.get())

        if sharks.length > 5:
            sharks.list.pop(0)
        if preyflock.length >= 10:
            preyflock.list.pop(-1)

        for i in sliders:
            i.update()
        preyflock.update(sharkFlock=sharks)
        sharks.update(foodFlock=preyflock)
        bubbleGrp.update()

        for s in sliders:
            preyflock.setattrall(s.text, s.slider.getValue())

        screen.blit(bg, (0, 0))
        backBub.draw(screen)
        preyflock.draw()
        sharks.draw()
        frontBub.draw(screen)
        for i in sliders:
            i.draw()

        pygame.display.update()
        clock.tick(FPS)

        print(clock.get_fps())

    pygame.quit()

if __name__ == "__main__":
    main()

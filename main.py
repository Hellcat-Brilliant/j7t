import pygame
import sys
from sprites.platforms import GreenPlatform as gp
from sprites.platforms import RedPlatform as rp
from sprites.platforms import BluePlatform as bp
from sprites.doodle import Player
from sprites.spring import Spring
from sprites.fon import Score
from random import randint as rn

pygame.init()

# Константы/Constants
WIDTH = 600
HEIGHT = 600
FPS = 20

# Создание окна/Window creating
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")
clock = pygame.time.Clock()


def main():
    # Спрайты/Sprites
    doode = Player()
    score = Score()
    offset = 0
    springs = pygame.sprite.Group()
    plats = pygame.sprite.Group()
    for i in range(10):
        x = rn(0, 100)
        if x in range(10, 90):
            plats.add(gp((rn(50, screen.get_width() - 50), screen.get_height() - 37 - (screen.get_height() // 10) * i)))
        elif x in range(0, 10):
            plats.add(bp((rn(50, screen.get_width() - 50), screen.get_height() - 37 - (screen.get_height() // 10) * i)))
        else:
            plats.add(rp((rn(50, screen.get_width() - 50), screen.get_height() - 37 - (screen.get_height() // 10) * i)))

    running = True
    while running:
        # Частота обновления экрана/Screen refresh rate
        clock.tick(FPS)

        # События/Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
                    with open("results.txt", 'w') as f1:
                        f1.write(str(score.steps))

        if doode.rect.bottom < screen.get_height() // 2:
            offset = doode.gravity
        else:
            offset = 0

        for platform in plats:
            if platform.rect.collidepoint(doode.rect.bottomleft) or platform.rect.collidepoint(doode.rect.bottomright) and doode.gravity < 0:
                if not isinstance(platform, rp):
                    doode.gravity = 15
                else:
                    platform.image = platform.image2

        for spring in springs:
            if spring.rect.collidepoint(doode.rect.bottomleft) or spring.rect.collidepoint(doode.rect.bottomright) and doode.gravity < 0:
                doode.gravity = 50


        # Рендеринг/Rendering
        screen.fill((255, 255, 255))
        for x in range(0, screen.get_width(), 10):
            pygame.draw.line(screen, (222, 222, 222), (x, 0), (x, screen.get_height()))
            pygame.draw.line(screen, (222, 222, 222), (0, x), (screen.get_width(), x))

        if len(plats) < 10:
            x = rn(0, 100)
            if x in range(10, 90):
                x = gp((rn(50, screen.get_width() - 50), -10))
                plats.add(x)
                if True:
                    springs.add(Spring(x.rect.topleft))
            elif x in range(0, 10):
                plats.add(bp((rn(50, screen.get_width() - 50), -10)))
            else:
                plats.add(rp((rn(50, screen.get_width() - 50), -10)))


        plats.draw(screen)
        doode.draw(screen)
        springs.draw(screen)
        score.draw(screen)


        # Обновление спрайтов/Updating sprites
        plats.update(offset)
        doode.update(offset)
        springs.update(offset)
        score.update(offset)

        # Обновление экрана/Screen Refresh
        pygame.display.update()


if __name__ == "__main__":
    main()
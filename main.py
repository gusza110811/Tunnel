from objects import *
import pygame
import random
import threading

class Game:
    def __init__(self, scrWidth, scrHeight):
        self.objects:list[obj] = []
        self.screenwidth = scrWidth
        self.screenheight = scrHeight
        self.degToPos = self.screenwidth/360

        self.timeToGen = 0
        self.genTime = 120

    def start(self):
        self.player = player(180,500,friction=0.2)
        self.relx = self.player.x

        self.objects.append(self.player)

        return

    def wall_gen(self):
        start = random.randint(0,360//36)
        length = random.randint(2,8)

        for i in range(length):
            x = ((i+start)*36) % 360
            y = -72
            self.objects.append(wall(x,y))


    def update(self):
        if self.timeToGen <= 0:
            self.wall_gen()
            self.timeToGen = self.genTime
        else:
            self.timeToGen -= 1


        accel = 0.5

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.player.vx < 5:
            self.player.vx -= accel
        if keys[pygame.K_d] and self.player.vx > -5:
            self.player.vx += accel

        for object in self.objects:
            object.physic()

            if object.y > self.screenheight:
                self.objects.remove(object)

        return

    def render(self, screen:pygame.Surface):
        relxdist = (self.player.x-self.relx)/3
        if abs(relxdist) > 100:
            self.relx = self.player.x
        else:
            self.relx += relxdist

        for object in self.objects:
            if not isinstance(object,obj):
                continue
            width = 36*self.degToPos
            height = 72
            x = ((object.x-self.relx+180)% 360) * self.degToPos - width//2
            y = object.y - height/2
            if isinstance(object,player):
                surf = pygame.image.load("sprites/player.png")
            if isinstance(object, wall):
                surf = pygame.image.load("sprites/wall.png")
            surf = pygame.transform.scale(surf,(width, height))
            screen.blit(surf,dest=(x,y))
        return


if __name__ == "__main__":
    clock = pygame.time.Clock()

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    game = Game(WIDTH,HEIGHT)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()
    dbgtxt = pygame.sysfont.SysFont("Helvetica",12)
    running = True
    dbg_active = True
    def dbg_render():
        screen.blit(
            dbgtxt.render(str(clock.get_fps()),False,pygame.Color(0,255,0)),
            dest=(16,16)
        )
        screen.blit(
            dbgtxt.render(str(len(game.objects)),False,pygame.Color(0,255,0)),
            dest=(16,32)
        )

    game.start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    dbg_active = not dbg_active
        game.update()
        screen.fill(pygame.Color(0,0,0))
        game.render(screen)
        if dbg_active:dbg_render()

        pygame.display.flip()
        clock.tick(60)
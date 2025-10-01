from objects import *
import pygame
import random

class Game:
    def __init__(self, scrWidth, scrHeight):
        self.objects:list[obj] = []
        self.screenwidth = scrWidth
        self.screenheight = scrHeight
        self.degToPos = self.screenwidth/360

        self.alive = True

        self.timeToGen = 0
        self.genTime = (45,90)

    def start(self):
        self.player = player(180,500,friction=0.1)
        self.relx = self.player.x

        self.objects.append(self.player)

        return

    def wall_gen(self):
        start = random.randint(0,360//36)
        length = random.randint(2,8)

        for i in range(length):
            x = ((i+start)*36) % 360
            y = -72
            wallter = wall(x,y)
            wallter.vy = 7
            self.objects.append(wallter)


    def update(self):
        if self.timeToGen <= 0:
            self.wall_gen()
            self.timeToGen = random.randint(*self.genTime)
        else:
            self.timeToGen -= 1


        MAX_SPEED = 7
        ACCEL = MAX_SPEED/15

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.player.vx < MAX_SPEED:
            self.player.vx -= ACCEL
        if keys[pygame.K_d] and self.player.vx > -MAX_SPEED:
            self.player.vx += ACCEL

        for object in self.objects:
            object.physic()

            if object.y > self.screenheight:
                self.objects.remove(object)
        playery = self.player.y - 72
        for Wall in [object for object in self.objects if isinstance(object,wall)]:
            if Wall.y > playery:
                self.alive = not Wall.x_overlap(self.player)
                if not self.alive:
                    break

        return

    def render(self, screen:pygame.Surface):
        self.relx += ((self.player.x - self.relx + 540) % 360 - 180)/3

        for object in self.objects:
            if not isinstance(object,obj):
                continue
            width = object.width*self.degToPos
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

class GameOverScreen:
    def __init__(self):
        pass
    def update(self):
        if pygame.key.get_pressed()[pygame.K_r]:
            global game
            global scene
            global WIDTH
            global HEIGHT
            game = Game(WIDTH,HEIGHT)
            scene = game
            game.start()

    def render(self,screen:pygame.Surface):
        deathFont = pygame.Font("Helvetica.ttf",size=screen.width//8)
        deathLabel = deathFont.render("YOU DIED",True,pygame.Color(255,255,255))
        screen.blit(deathLabel, dest=(screen.width//2-(deathLabel.width//2),50))

        respawnFont = pygame.Font("Helvetica.ttf",size=20)
        respawnLabel = respawnFont.render("Press R to retry",True,pygame.Color(0,255,255))
        screen.blit(respawnLabel, dest=(screen.width//2-(respawnLabel.width//2),150))


if __name__ == "__main__":
    clock = pygame.time.Clock()

    pygame.init()
    WIDTH, HEIGHT = 800, 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()
    running = True

    dbgtxt = pygame.Font("Helvetica.ttf",size=16)
    dbg_active = True
    def dbg_render():
        screen.blit(
            dbgtxt.render("FPS: "+str(clock.get_fps()),False,pygame.Color(0,255,0)),
            dest=(16,16)
        )
        screen.blit(
            dbgtxt.render("Obj count: "+str(len(game.objects)),False,pygame.Color(0,255,0)),
            dest=(16,32)
        )
        screen.blit(
            dbgtxt.render("Player is alive: "+str(game.alive),False,pygame.Color(0,255,0)),
            dest=(16,48)
        )

    game = Game(WIDTH,HEIGHT)
    game.start()
    deathScreen = GameOverScreen()

    scene = game
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    dbg_active = not dbg_active

        scene.update()
        if scene == game and not game.alive:
            scene = deathScreen
        screen.fill(pygame.Color(0,0,0))
        scene.render(screen)


        if dbg_active:dbg_render()

        pygame.display.flip()
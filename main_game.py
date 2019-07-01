"""
Dinosaur Game by Joachim Dekker and Thijs Boerefijn
Under license!
"""

import pygame
import random
import inspect

pygame.init()

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("test")
CLOCK = pygame.time.Clock()

SCREEN = pygame.display.get_surface().get_size()
BACKGROUND = pygame.Surface(SCREEN)
BACKGROUND.fill((30, 90, 120))

FPS = 60
SCORE = 0
Running = True

myfont = pygame.font.SysFont('Comic Sans MS', 30)
betterFont = pygame.font.SysFont("Comic Sans MS", 100) #Merriweather-Black.ttf

PATH = inspect.getfile(inspect.currentframe()).strip('main_game.py')
walkRight = [pygame.image.load(PATH + 'png\Walk1.png'), pygame.image.load(PATH + 'png\Walk2.png'), pygame.image.load(PATH + 'png\Walk3.png'), pygame.image.load(PATH + 'png\Walk4.png'), pygame.image.load(PATH + 'png\Walk5.png'), pygame.image.load(PATH + 'png\Walk6.png'), pygame.image.load(PATH + 'png\Walk7.png'), pygame.image.load(PATH + 'png\Walk8.png'), pygame.image.load(PATH + 'png\Walk9.png'), pygame.image.load(PATH + 'png\Walk10.png')]
jumpList = [pygame.image.load(PATH + 'png\Jump1.png'), pygame.image.load(PATH + 'png\Jump2.png'), pygame.image.load(PATH + 'png\Jump3.png'), pygame.image.load(PATH + 'png\Jump4.png'), pygame.image.load(PATH + 'png\Jump5.png'), pygame.image.load(PATH + 'png\Jump6.png'), pygame.image.load(PATH + 'png\Jump7.png'), pygame.image.load(PATH + 'png\Jump8.png'), pygame.image.load(PATH + 'png\Jump9.png'), pygame.image.load(PATH + 'png\Jump10.png'), pygame.image.load(PATH + 'png\Jump11.png'), pygame.image.load(PATH + 'png\Jump12.png')]
birdList = [pygame.image.load(PATH + 'png\Bird1.png'), pygame.image.load(PATH + 'png\Bird2.png')]
cactusList = [pygame.image.load(PATH + 'png\Cactus1.png'), pygame.image.load(PATH + 'png\Cactus2.png'), pygame.image.load(PATH + 'png\Cactus3.png')]
enemylist = []

class Player():
    """
    PLAYER Class: This is the class that is controlled by the PLAYER.
    XXX TO DO:
    [] Make the PLAYER ?DIVE?
    """
    def __init__(self, x: int, y: int, width: int, height: int, jumpForce: float = 10):
        self.x_coord = x
        self.y_coord = y
        self.width = width
        self.height = height

        self.jumpforce = 0
        self.gravity = 3

        self.jumping = False
        self.in_air = False

        self.init_jf = jumpForce

        self.walkCount = 0
        self.jumpCount = 0
        self.right = True

        self.hitbox = (self.x_coord + 15, self.y_coord + 5, self.width, self.height)

    def jump(self):
        """
        Makes the PLAYER jump
        """
        if self.jumpCount + 1 > 27:
            self.jumpCount = 0

        if self.jumping:
            self.jumpforce -= self.gravity * 1/FPS
            self.y_coord -= round(self.jumpforce, 2)
            
            self.right = False
            self.hitbox = (self.x_coord + 15, self.y_coord + 5, self.width, self.height)
            pygame.draw.rect(WIN, (0, 255, 0), self.hitbox)
            WIN.blit(pygame.transform.scale(jumpList[self.jumpCount // 3],(150,150)), (self.x_coord, self.y_coord))
            self.jumpCount += 1

            if self.y_coord > SCREEN[1] / 2.3:
                self.jumping = False
                self.right = True
                self.jumpforce = 0
                self.y_coord = SCREEN[1] / 2.3

    def walk(self):
        if self.walkCount + 1 > 27:
            self.walkCount = 0

        if self.right:
            self.hitbox = (self.x_coord + 15, self.y_coord + 5, self.width, self.height)
            pygame.draw.rect(WIN, (0, 255, 0), self.hitbox)
            WIN.blit(pygame.transform.scale(walkRight[self.walkCount // 3],(150,150)), (self.x_coord, self.y_coord))
            self.walkCount += 1

class Enemy():
    """
    ENEMY Class: This is the class that makes the ENEMY.
    XXX TO DO:
    [] make hitbox work
    """
    def __init__(self):
        self.time = 0
        self.running = True
        self.hitbox = (0, 0, 0, 0)
    
    def timer(self):
        self.time -= 1
        if self.time < 0:
            self.spawn()
            self.time = 300

    def spawn(self):
        random_int = random.randint(0,1)
        if random_int == 0:
            random_int2 = random.randint(0,1)
            if random_int2 == 0:
                get_cactus = 0
            elif random_int2 == 1:
                get_cactus = 1
            elif random_int2 == 2:
                get_cactus = 2
            enemylist.append(Plant(SCREEN[0], SCREEN[1] / 2, 50, 60, get_cactus))
        elif random_int == 1:
            enemylist.append(Bird(SCREEN[0], SCREEN[1] / 3, 50, 60))

    def collision(self, c_object):
        c = c_object
        if c.y_coord < self.hitbox[1] + self.hitbox[3] and c.y_coord + c.height > self.hitbox[1]:
            if c.x_coord + c.width > self.hitbox[0] and c.x_coord + c.width < self.hitbox[0] + self.hitbox[2]:
                self.running = False
                return False

class Bird(Enemy):
    """
    BIRD Class: This is the class that makes the BIRD.
    XXX TO DO:
    [] Make sprites for BIRD
    [] Import sprites for BIRD
    """
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x_coord = x
        self.y_coord = y
        self.width = width
        self.height = height
        self.fly_count = 0
        self.fly = True
        self.hitbox = (self.x_coord + 50, self.y_coord + 40, width, height)

    def draw(self):
        """
        Draws the BIRD on the screen
        """
        if self.fly_count + 1 > 12:
            self.fly_count = 0

        if self.fly:
            self.hitbox = (self.x_coord + 50, self.y_coord + 40, self.width, self.height)
            pygame.draw.rect(WIN, (0, 255, 0), self.hitbox)
            WIN.blit(pygame.transform.scale(birdList[self.fly_count // 6], (170, 150)), (self.x_coord, self.y_coord))


class Plant(Enemy):
    """
    PLANT Class: This is the class that makes the PLANT.
    XXX TO DO:
    [] Make sprites for PLANT
    [] Import sprites for PLANT
    """
    def __init__(self, x: int, y: int, width: int, height: int, get_cactus: int):
        self.x_coord = x
        self.y_coord = y
        self.width = width
        self.height = height
        self.hitbox = (self.x_coord, self.y_coord + 5, 50, 60)
        self.get_cactus = get_cactus


    def draw(self):
        """
        Draws the PLANT on the screen
        """
        self.hitbox = (self.x_coord, self.y_coord + 5, 70, 60)
        pygame.draw.rect(WIN, (0, 255, 0), (self.hitbox))
        WIN.blit(pygame.transform.scale(cactusList[self.get_cactus], (80, 70)), (self.x_coord, self.y_coord))

class Score():
    def __init__(self, input_score: int):
        self.input_score = input_score
    
    def score(self):
        textsurface = myfont.render(f'Je score is {str(self.input_score)}', False, (255, 255, 255))
        WIN.blit(textsurface,(10, 10))
        self.input_score += 1

    def death(self):
        BACKGROUND.fill((0, 0, 0))

        textsurface = betterFont.render(f'YOU DIED', False, (255, 255, 255))
        size = betterFont.size("YOU DIED")
        WIN.blit(textsurface,(SCREEN[0]/2-size[0]/2,SCREEN[1]/2-size[1]/2))

        textsurface = betterFont.render(f'You had a score of {SCORE.input_score}', False, (255, 255, 255))
        size = betterFont.size(f'You had a score of {SCORE.input_score}')
        WIN.blit(textsurface,(SCREEN[0]/2-size[0]/2,SCREEN[1]/1.6-size[1]/2))


PLAYER = Player(SCREEN[0] / 3, SCREEN[1] / 2.3, 75, 140, 4)
SCORE = Score(0)
THE_ENEMY = Enemy()
RunRun = True
Death = False

while Running:
    WIN.blit(BACKGROUND, (0, 0))
    if not Death:
        for enemy in enemylist:
            enemy.x_coord -= 2
            enemy.draw()
            RunRun = enemy.collision(PLAYER)
            if RunRun == False:
                Death = True

        THE_ENEMY.timer()
        PLAYER.jump()
        SCORE.score()
    else:
        SCORE.death()

    
    KEYS = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or KEYS[pygame.K_ESCAPE]:
            Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not PLAYER.jumping:
                PLAYER.jumping = True
                PLAYER.jumpforce = PLAYER.init_jf

    CLOCK.tick(FPS)
    PLAYER.walk()

    pygame.display.update()

    if Running == None:
        Running = True

pygame.quit()

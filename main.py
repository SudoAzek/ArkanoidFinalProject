import pygame
import sys
from pygame.locals import *

# Constants#

DISPLAY_WIDTH = 740
DISPLAY_HEIGHT = 580

#### Colors ####

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COMBLUE = (233, 232, 255)

BG_COLOR = BLACK
BLOCK_GAP = 2
BLOCK_WIDTH = 62
BLOCK_HEIGHT = 25
ARRAY_WIDTH = 10
ARRAY_HEIGHT = 5
PADDLE_WIDTH = 130
PADDLE_HEIGHT = 15
BALL_RADIUS = 20
BALL_COLOR = RED
BLOCK = 'block'
BALL = 'ball'
PADDLE = 'paddle'
BALL_SPEED = 1


class Block(pygame.sprite.Sprite):

    def __init__(self):
        self.blockWidth = BLOCK_WIDTH
        self.blockHeight = BLOCK_HEIGHT
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.blockWidth, self.blockHeight))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.name = BLOCK


class Ball(pygame.sprite.Sprite):
    def __init__(self, displaySurf):
        pygame.sprite.Sprite.__init__(self)
        self.name = BALL
        self.moving = False
        self.image = pygame.Surface((15, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vectorx = BALL_SPEED
        self.vectory = BALL_SPEED * -1
        self.score = 0

    def update(self, mousex, blocks, paddle, *args):
        if self.moving == False:
            self.rect.centerx = mousex

        else:
            self.rect.y += self.vectory

            hitGroup = pygame.sprite.Group(paddle, blocks)

            spriteHitList = pygame.sprite.spritecollide(self, hitGroup, False)
            if len(spriteHitList) > 0:
                for sprite in spriteHitList:
                    if sprite.name == BLOCK:
                        sprite.kill()
                        self.score += 1
                self.vectory *= -1
                self.rect.y += self.vectory

            self.rect.x += self.vectorx

            blockHitList = pygame.sprite.spritecollide(self, blocks, True)

            if len(blockHitList) > 0:
                self.vectorx *= -1
                self.score += 1

            if self.rect.right > DISPLAY_WIDTH:
                self.vectorx *= -1
                self.rect.right = DISPLAY_WIDTH

            elif self.rect.left < 0:
                self.vectorx *= -1
                self.rect.left = 0

            if self.rect.top < 0:
                self.vectory *= -1
                self.rect.top = 0


class Paddle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.name = PADDLE

    def update(self, mousex, *args):
        if self.rect.x >= 0 and self.rect.right <= DISPLAY_WIDTH:
            self.rect.centerx = mousex

        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > DISPLAY_WIDTH:
            self.rect.right = DISPLAY_WIDTH


class Score(object):
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont('Helvetica', 25)
        self.render = self.font.render('Score: ' + str(self.score), True, RED, BLACK)
        self.rect = self.render.get_rect()
        self.rect.x = 0
        self.rect.bottom = DISPLAY_HEIGHT


class App(object):
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.mousex = 0
        self.blocks = self.createBlocks()
        self.paddle = self.createPaddle()
        self.ball = self.createBall()
        self.score = Score()

        self.allSprites = pygame.sprite.Group(self.blocks, self.paddle, self.ball)

    def updateScore(self):
        self.score.score = self.ball.score
        self.score.render = self.score.font.render('Score: ' + str(self.score.score), True, RED, BLACK)
        self.score.rect = self.score.render.get_rect()
        self.score.rect.x = 0
        self.score.rect.bottom = DISPLAY_HEIGHT

    def makeScreen(self):
        pygame.display.set_caption('Arkanoid')
        displaySurf = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        displayRect = displaySurf.get_rect()
        displaySurf.fill(BG_COLOR)
        displaySurf.convert()

        return displaySurf, displayRect

    def createBall(self):
        ball = Ball(self.displaySurf)
        ball.rect.centerx = self.paddle.rect.centerx
        ball.rect.bottom = self.paddle.rect.top

        return ball

    def createPaddle(self):
        paddle = Paddle()
        paddle.rect.centerx = self.displayRect.centerx
        paddle.rect.bottom = self.displayRect.bottom

        return paddle

    def createBlocks(self):
        blocks = pygame.sprite.Group()

        for row in range(ARRAY_HEIGHT):
            for i in range(ARRAY_WIDTH):
                block = Block()
                block.rect.x = i * (BLOCK_WIDTH + BLOCK_GAP)
                block.rect.y = row * (BLOCK_HEIGHT + BLOCK_GAP)
                block.color = self.setBlockColor(block, row, i)
                block.image.fill(block.color)
                blocks.add(block)

        return blocks

    def setBlockColor(self, block, row, column):
        if column == 0 or column % 2 == 0:
            return GREEN
        else:
            return COMBLUE

    def checkInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()

            if event.type == MOUSEMOTION:
                # We only need the x value of a mousemotion, so we grab
                # only the first value of the event.pos tuple
                self.mousex = event.pos[0]

            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    self.ball.moving = True

    def terminate(self):
        pygame.quit()
        sys.exit()

    def mainLoop(self):
        while True:
            self.displaySurf.fill(BG_COLOR)
            self.updateScore()
            self.displaySurf.blit(self.score.render, self.score.rect)
            self.allSprites.update(self.mousex, self.blocks, self.paddle)
            self.allSprites.draw(self.displaySurf)
            pygame.display.update()
            self.checkInput()


if __name__ == '__main__':
    runGame = App()
    runGame.mainLoop()

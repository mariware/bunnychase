import pygame
import time

width = 1000
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bunny Chase")

class Player():

    walkLeft = [pygame.image.load('sprites/tile012.png'), pygame.image.load('sprites/tile014.png'), pygame.image.load('sprites/tile013.png')]
    walkRight = [pygame.image.load('sprites/tile024.png'), pygame.image.load('sprites/tile026.png'), pygame.image.load('sprites/tile025.png')]
    walkUp = [pygame.image.load('sprites/tile036.png'), pygame.image.load('sprites/tile038.png'), pygame.image.load('sprites/tile037.png')]
    walkDown = [pygame.image.load('sprites/tile000.png'), pygame.image.load('sprites/tile001.png'), pygame.image.load('sprites/tile002.png')]
    carrot = pygame.image.load('sprites/tile096.png')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.left = False
        self.right = False
        self.up = False
        self.down = True
        self.moving  = False
        self.it = False
        self.hitbox = pygame.Rect(self.x + 6, self.y + 12, 20, 20)
        self.walkCount = 0
        self.vel = 3
        self.collisionCD = 0

    def draw(self, win):
        if self.walkCount + 1 >= 15:
            self.walkCount = 0

        if self.moving:
            if self.left:
                win.blit(self.walkLeft[self.walkCount // 5], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount // 5], (self.x, self.y))
                self.walkCount += 1
            elif self.up:
                win.blit(self.walkUp[self.walkCount // 5], (self.x, self.y))
                self.walkCount += 1
            elif self.down:
                win.blit(self.walkDown[self.walkCount // 5], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left: win.blit(self.walkLeft[2], (self.x, self.y))
            elif self.right: win.blit(self.walkRight[2], (self.x, self.y))
            elif self.up: win.blit(self.walkUp[2], (self.x, self.y))
            elif self.down: win.blit(self.walkDown[2], (self.x, self.y))
        
        if self.it: win.blit(self.carrot, (self.x + 9, self.y - 15))

    def move(self):
        keys = pygame.key.get_pressed()
        
        if self.x < 0:
            self.x = 0 
            return 
        elif self.x > width - self.width:
            self.x = width - self.width 
            return

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            self.moving = True
            self.x -= self.vel
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.left = False
            self.right = True
            self.up = False
            self.down = False
            self.moving = True
            self.x += self.vel
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.left = False
            self.right = False
            self.up = True
            self.down = False
            self.moving = True
            self.y -= self.vel
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.left = False
            self.right = False
            self.up = False
            self.down = True
            self.moving = True
            self.y += self.vel
        else:
            self.moving = False

        self.hitbox = pygame.Rect(self.x + 6, self.y + 12, 20, 20)
        self.draw(win)
        
        

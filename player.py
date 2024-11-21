import pygame
import uuid
# import time

width = 1000
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("bunnychase!")

mini_cam_size = 200
zoom_factor = 2
mini_cam_rect = pygame.Rect(width - mini_cam_size - 10, height - mini_cam_size - 10, mini_cam_size, mini_cam_size)


class Player():

    walkLeft = [pygame.image.load('sprites/tile012.png'), pygame.image.load('sprites/tile014.png'), pygame.image.load('sprites/tile013.png')]
    walkRight = [pygame.image.load('sprites/tile024.png'), pygame.image.load('sprites/tile026.png'), pygame.image.load('sprites/tile025.png')]
    walkUp = [pygame.image.load('sprites/tile036.png'), pygame.image.load('sprites/tile038.png'), pygame.image.load('sprites/tile037.png')]
    walkDown = [pygame.image.load('sprites/tile000.png'), pygame.image.load('sprites/tile001.png'), pygame.image.load('sprites/tile002.png')]
    carrot = pygame.image.load('sprites/tile096.png')
    
    def __init__(self, x, y):
        self.id = str(uuid.uuid4())
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
        self.score = 0
        
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
        
        if self.y < 0:
            self.y = 0 
            return 
        elif self.y > height - self.height:
            self.y = height - self.height 
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
    
    def draw_mini_cam(win, player):
        mini_cam_size = 200
        zoom_factor = 2
        mini_cam_rect = pygame.Rect(width - mini_cam_size - 10, height - mini_cam_size - 10, mini_cam_size, mini_cam_size)
        
        mini_cam_surface = pygame.Surface((mini_cam_size, mini_cam_size))
        
        cam_x = max(0, player.x - mini_cam_size // (zoom_factor * 2))
        cam_y = max(0, player.y - mini_cam_size // (zoom_factor * 2))
        
        mini_cam_surface.blit(win, (0, 0), pygame.Rect(cam_x, cam_y, mini_cam_size * zoom_factor, mini_cam_size * zoom_factor))
        mini_cam_surface = pygame.transform.scale(mini_cam_surface, (mini_cam_size, mini_cam_size))
    
        pygame.draw.rect(win, (0, 0, 0), mini_cam_rect, 2)
        win.blit(mini_cam_surface, mini_cam_rect.topleft)
    
         
    
        
        

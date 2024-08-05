import pygame
#from pygame.sprite import _Group
import random
import math

#init pygame
pygame.init()



#game window dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('JumperHen')

#set framrate
clock = pygame.time.Clock()
FPS = 60

#game variables
GRAVITY = 1
MAX_PLATFORMS = 10
SCROLL_THRESH = 600
scroll = 0


#define colors
WHITE = (255,255,255)


#load images
jumper_image = pygame.image.load('assets/images/entities/player/Idle/player.png').convert_alpha()
bg_image = pygame.image.load('assets/images/background.png').convert_alpha()
platform_img = pygame.image.load('assets/images/platform.png').convert_alpha()
bg_image_1 = 0
bg_image_2 = bg_image.get_width()

#Scroll background
#def draw_bg(scroll):
    #screen.blit(bg_image, (0,0 + scroll))
    #screen.blit(bg_image, (800,1200 + scroll))
#create sprite groups
platform_group = pygame.sprite.Group()
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumper_image, (95, 95))
        self.width = 25
        self.height = 80
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = (x,y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        #reset variables
        dx = 0
        dy = 0
        scroll = 0 
        
        #process keypress
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False
        

        #gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #check player pos to screen left-right
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #check collision platform
        for platform in platform_group:
            #check y pos
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        #self.vel_y = -30
        #check collision ground
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            self.vel_y = -30
        
        #check if player has bounced top
        if self.rect.top <= SCROLL_THRESH:
            scroll = -dy

        # update rectangel position
        self.rect.x += dx
        self.rect.y += dy
        return scroll
       

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x -41, self.rect.y -14))
        pygame.draw.rect(screen, WHITE, self.rect, 2)



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):

        #update platform scroll
        self.rect.x -= scroll
        if self.rect == self.rect.left :
            self.kill()


x = int(SCREEN_WIDTH // 2)
y = int(SCREEN_HEIGHT - 150)
#player instance
jumper = Player(x,y)




#create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 200)
platform_group.add(platform)

def redrawWindow():
    
    screen.blit(bg_image, (bg_image_1, 0))
    screen.blit(bg_image, (bg_image_2,0))
    platform_group.draw(screen)
    jumper.draw()
    if len(platform_group) < 20:
          
        p_w = random.randint(40, 80)
        p_x = random.randint(0, SCREEN_WIDTH - p_w)
        p_y = random.randint(0, SCREEN_HEIGHT - p_w)
        platform = Platform(p_x, p_y, p_w)
        platform_group.add(platform)

    platform_group.update(scroll)
    #Platform.update(self=)
    pygame.display.update()


speed = 30
#game loop
run = True
while run:
    
    #move player
    jumper.move()
    #draw background
    scroll += 0.01
    
    bg_image_1 -= 1.4  # Move both background images back
    bg_image_2 -= 1.4

    if bg_image_1 < bg_image.get_width() * -1:  # If our bg is at the -width then reset its position
        bg_image_1 = bg_image.get_width()
    
    if bg_image_2 < bg_image.get_width() * -1:
        bgbg_image_2 = bg_image.get_width()

    
    #create platform


    #print(bg_scroll)
    #pygame.draw.line(screen, WHITE, (0, SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))
    #update platforms
    
    #draw sprites
    
    #jumper.draw()
    #reset scroll


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # add scroll  
    
    clock.tick(speed)  # NEW
    redrawWindow()
  
pygame.quit()


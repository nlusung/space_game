import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Game Window
WIDTH , HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

# Ship/ Bullet colorr
WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0
YELLOW = 255,255,0

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets','Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comincsans', 40)
WINNER_FONT = pygame.font.SysFont('comincsans', 100)

FPS = 60
VELOCITY = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)


RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets','space.png')),(WIDTH,HEIGHT))


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WINDOW.blit(SPACE_BACKGROUND,(0,0))
    pygame.draw.rect(WINDOW,BLACK,BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health),1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health),1,WHITE)
    WINDOW.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text,(10,10))
    
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x , red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW,RED,bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW,YELLOW,bullet)
    
    pygame.display.update()
    
def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x > 0:    #LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x:  #RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT - 15:  #DOWN
        yellow.y += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y > 0:   #UP
        yellow.y -= VELOCITY

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:    #LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH:  #RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT-15:  #DOWN
        red.y += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y > 0:   #UP
        red.y -= VELOCITY

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.EventType(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet )


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WINDOW.blit(draw_text,(WIDTH/2 - draw_text.get_width()/
                           2,HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700,250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10
    
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10 , 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
         
        
        winner_text = ""   
        if red_health <= 0:
            winner_text = "Yellow Wins!"
            
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break
                   
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        
        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        
            
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
    
    main()
    

if __name__ == "__main__":
    main()
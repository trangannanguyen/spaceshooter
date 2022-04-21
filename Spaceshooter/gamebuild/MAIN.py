from msilib.schema import Class
from turtle import window_width
from pygame import *
from random import randint

font.init()

font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

# Parent Sprite Class
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
 
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player sprite class
class Player(GameSprite):
    #method to control the sprite with A & D keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #method to "shoot" (use the player position to create a bullet there)
    def fire(self):
        print('pew pew') # Testing line later we add more code
        offset = 0
        for i in range(3):
            bullet = Bullet(img_bullet, self.rect.centerx-25+offset, self.rect.top, 15, 20, 15)
            bullets.add(bullet)
            offset += 25


# Enemy sprite class  
class Enemy(GameSprite):
    #enemy movement
    def update(self):
        # Move the enemy down on the y axis by self.speed
        self.rect.y += self.speed
        global enemies_escaped
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = - 40
            self.speed = randint(2, 5)/2
            enemies_escaped += 1

# bullet sprite class   
class Bullet(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y -= self.speed
        # disappears if it reaches the edge of the screen
        if self.rect.y < 0:
            self.kill()

#Boss ufo sprite class
class boss(GameSprite):
    #boss movement
    def update(self):
        # Move the enemy down on the y axis by self.speed
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = - 40
            self.speed = randint(2, 5)/2

# Game variables
FPS = 60
clock = time.Clock()
game = True
win_width = 700
win_height = 650
bullets = sprite.Group()
score = 0
enemies_escaped = 0
game_over = False
boss_won = False

# Game sprites
img_player = 'rocket.png'
img_enemy = 'ufoblack.png'
img_bullet = 'bullet.png'
img_boss = 'MASTERUFO.png'


# Create our game sprites (image, x pos, y pos, x size, y size, speed)
ship = Player(img_player, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5)/2)
    monsters.add(monster)

# Create a game window
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('wargalaxy.jpg'), (win_width, win_height))


# Game loop
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not game_over:

        window.blit(background,(0, 0))

        text = font2.render("Score " + str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))

        text_lose = font2.render("Enemies escaped: " + str(enemies_escaped), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # this loop will be repeated as many times as monsters are killed
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5)/2)
            monsters.add(monster)

        if enemies_escaped >= 5:
            window.blit(lose, (200,200))
            game_over = True

        if score >= 20:
            window.blit(win, (200,200))
            game_over = True
        
        if score >= 15 and boss_won == False:
            #create boss ufo
            ufo = boss(img_boss, randint(80, win_width - 80), -40, 150, 100, randint(2, 5)/2)
            boss_won = True
            monsters.add(ufo)
        
        if boss_won == True:
            ufo.update()
            ufo.reset()
        

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        display.update()
        clock.tick(FPS)
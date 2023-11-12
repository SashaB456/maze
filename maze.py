import pygame
width = 800
height = 600
size = (width,height)
FPS = 60
window = pygame.display.set_mode(size)
background = pygame.transform.scale(pygame.image.load("background.jpg"), size)
clock = pygame.time.Clock()
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x,y, speed):
        self.image = pygame.transform.scale(pygame.image.load(image), (65,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def uptade(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            if self.rect.y > 0:
                self.rect.y -= self.speed
#            else:
#                self.rect.y = height
        if keys_pressed[pygame.K_DOWN]:
            if self.rect.y < height-85:
                self.rect.y += self.speed
#            else:
#               self.rect.y = 0
        if keys_pressed[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
#            else:
#                self.rect.x = width
        if keys_pressed[pygame.K_RIGHT]:
            if self.rect.x < width-70:
                self.rect.x += self.speed
#            else:
#                self.rect.x = 0
class Enemy(GameSprite):
    direction = "left"
    def uptade(self):
        if self.rect.x <= width/2:
            self.direction = "right"
        if self.rect.x >= width-70:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= 5
        elif self.direction == "right":
            self.rect.x += 5
class Wall(pygame.sprite.Sprite):
    def __init__(self, r, g, b, x, y, lenght, width):
        super().__init__()
        self.color = (r, g, b)
        self.rect = pygame.Rect(x, y, lenght, width)
    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)
        
player = Player('hero.png', 70, 400, 5)
enemy = Enemy('cyborg.png', width-80, 280, 5)
gold = GameSprite('treasure.png', width-100, height-100, 0)
pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()
pygame.font.init()
kick = pygame.mixer.Sound('kick.ogg')
money = pygame.mixer.Sound('money.ogg')
font1 = pygame.font.Font(None, 70)
font2 = pygame.font.Font(None, 50)
font3 = pygame.font.Font(None, 30)
text_win = font1.render('Ви перемогли :)', True, (0, 255, 0))
text_lose = font1.render('Ви програли :( ', True, (255, 0, 0))
text_again = font2.render("Натисніть на 'r', щоб ви змогли грати знову.", True, (255, 255, 255))
text_next = font3.render("Натисніть на пробіл, щоб ви змогли перейти на наступний рівень.", True, (255, 255, 255))
walls = [
    Wall(150, 180, 0, 20, 0, 10, 550),
    Wall(150, 180, 0, 170, 100, 10, 450),
    Wall(150, 180, 0, 20, 550, 160, 10),
    Wall(150, 180, 0, 20, 0, 650, 10),
    Wall(150, 180, 0, 170, 100, 400, 10),
    Wall(150, 180, 0, 670, 0, 10, 260),
    Wall(150, 180, 0, 560, 100, 10, 160),
    Wall(150, 180, 0, 390, 260, 180, 10),
    Wall(150, 180, 0, 670, 260, 160, 10),
    Wall(150, 180, 0, 390, 360, 150, 10),
    Wall(150, 180, 0, 390, 260, 10, 100),
    Wall(150, 180, 0, 670, 360, 150, 10),
    Wall(150, 180, 0, 790, 260, 10, 100),
    Wall(150, 180, 0, 540, 360, 10, 250)
]
walls2 = [
    Wall(0, 0, 255, width/2, 0, 10, height/2-50),
    Wall(0, 0, 255, width/2, height/2+50, 10, height/2-50),
    Wall(0, 0, 255, 150, height/2+50, width/2, 10),
    Wall(0, 0, 255, width/2-100, 120, 10, height/2)
]
level = 1
win = False
game_over = False
finish = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    if not finish and level == 1:
        window.blit(background, (0, 0))
        for i in walls:
            i.draw()
        player.uptade()
        player.reset()
        enemy.uptade()
        enemy.reset()
        gold.reset()
    if not finish and level == 2:
        window.blit(background, (0, 0))
        for i in walls2:
            i.draw()
        player.uptade()
        player.reset()
        enemy.uptade()
        enemy.reset()
        gold.reset()
    if pygame.sprite.collide_rect(player, gold) and level == 1:
        money.play()
        finish = True
        window.blit(text_win, (width/3, height/3))
        window.blit(text_next, (50, height/3+50))
        win = True
    elif pygame.sprite.collide_rect(player, gold) and level == 2:
        money.play()
        finish = True
        window.blit(text_win, (width/3, height/3))
        win = True
    if level == 1:
        wall_collision = any(pygame.sprite.collide_rect(player, i) for i in walls)
    elif level == 2:
        wall_collision = any(pygame.sprite.collide_rect(player, i) for i in walls2)
    if pygame.sprite.collide_rect(player, enemy) or wall_collision:
        kick.play()
        finish = True
        window.blit(text_lose, (width/3, height/3))
        window.blit(text_again, (50, height/3+50))
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_r] and win == False and finish == True and level == 1:
        finish = False
        player.rect.x = 70
        player.rect.y = 400
        kick.stop()
    elif keys_pressed[pygame.K_r] and win == False and finish == True and level == 2:
        finish = False
        player.rect.x = 260
        player.rect.y = 500
        kick.stop()
    if keys_pressed[pygame.K_SPACE] and win == True and finish == True and level == 1:
        money.stop()
        level = 2
        finish = False
        win = False
        player.rect.x = 260
        player.rect.y = 500
    pygame.display.update()
    clock.tick(FPS)
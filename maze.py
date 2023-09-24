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
            else:
                self.rect.y = height
        if keys_pressed[pygame.K_DOWN]:
            if self.rect.y < height-85:
                self.rect.y += self.speed
            else:
                self.rect.y = 0
        if keys_pressed[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
            else:
                self.rect.x = width
        if keys_pressed[pygame.K_RIGHT]:
            if self.rect.x < width-70:
                self.rect.x += self.speed
            else:
                self.rect.x = 0
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
text_win = font1.render('Ти переміг :)', True, (0, 255, 0))
text_lose = font1.render('Ти програв :(', True, (255, 0, 0))
walls = [
    Wall(150, 180, 0, 20, 0, 10, 550),
    Wall(150, 180, 0, 170, 100, 10, 450),
    Wall(150, 180, 0, 20, 550, 160, 10),
    Wall(150, 180, 0, 20, 0, 650, 10),
    Wall(150, 180, 0, 170, 100, 400, 10),
    Wall(150, 180, 0, 670, 0, 10, 260),
    Wall(150, 180, 0, 560, 100, 10, 160),
    Wall(150, 180, 0, 390, 260, 180, 10),
    Wall(150, 180, 0, 670, 260, 160, 10)
]
game_over = False
finish = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    if not finish:
        window.blit(background, (0, 0))
        for i in walls:
            i.draw()
        player.uptade()
        player.reset()
        enemy.uptade()
        enemy.reset()
        gold.reset()
    if pygame.sprite.collide_rect(player, gold):
        money.play()
        finish = True
        window.blit(text_win, (width/3, height/3))
    wall_collision = any(pygame.sprite.collide_rect(player, i) for i in walls)
    if pygame.sprite.collide_rect(player, enemy) or wall_collision:
        kick.play()
        finish = True
        window.blit(text_lose, (width/3, height/3))
    pygame.display.update()
    clock.tick(FPS)
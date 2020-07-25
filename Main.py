import pygame
import random

pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game")

screen_width = 500

bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
bulletSound = pygame.mixer.Sound('bullet.wav')
#hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()


class display(object):
    def __init__(self):
        self.font = pygame.font.SysFont('helevtica', 30, True)
        self.score = 0
        self.go = False
        self.time_count = 0


    def draw(self, win):
        score_text = self.font.render("Score: {s}".format(s=self.score), 1, (0, 0, 0))
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(score_text, (390, 10))
        if man.hp > man.max_hp // 2:
            hp_color = (9, 217, 64)
            pygame.draw.rect(win, hp_color, (390, 30, 100, 10), 2)
            pygame.draw.rect(win, hp_color, (390, 30, man.hp * 10, 10), 0)
        else:
            hp_color = (255, 25, 0)
            pygame.draw.rect(win, hp_color, (390, 30, 100, 10), 2)
            pygame.draw.rect(win, hp_color, (390, 30, man.hp * 10, 10), 0)

        if self.go is True and self.time_count < 50:
            print("inside loop")
            go_text = self.font.render("Game Over!", 1, (255, 0, 0))
            win.blit(go_text, (man.x, man.y + (man.height//2)))
            self.time_count += 1
        elif self.time_count > 100:
            self.time_count = 0
            self.go = False

    def game_over(self):
        self.go = True
        man.hp = man.max_hp


class player(object):
    walkRight = [pygame.image.load('R%s.png' % frame) for frame in range(1, 10)]
    walkLeft = [pygame.image.load('L%s.png' % frame) for frame in range(1, 10)]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 18, self.y + 12, 28, 50)
        self.hp = 10
        self.max_hp = 10

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            else:
                win.blit(self.walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 18, self.y + 12, 28, 50)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)


    def hit(self):
        self.hp -= 1
        man.isJump = True



class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R%sE.png' % frame) for frame in range(1, 12)]
    walkLeft = [pygame.image.load('L%sE.png' % frame) for frame in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 1
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health_bar = (self.x + 20, self.y, 10, 3)
        self.hp = 2
        self.max_hp = 2

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)

        if self.hp == self.max_hp:
            self.health_bar = (self.x + 20, self.y, 10, 3)
            pygame.draw.rect(win, (9, 217, 64), self.health_bar, 0)
        elif self.hp == self.max_hp // 2:
            self.health_bar = (self.x + 20, self.y, 5, 3)
            pygame.draw.rect(win, (255, 25, 0), self.health_bar, 0)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def move(self):
        """
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        """
        if man.x > self.x:
            if self.vel > 0:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        elif man.x < self.x:
            if self.vel < 0:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.vel > 0:
                self.x += self.vel
            else:
                self.x -= self.vel


    def hit(self):
        self.hp -= 1
        return self.hp


def redrawGameWindow():
    win.blit(bg, (0, 0))

    for bullet in bullets:
        bullet.draw(win)
    man.draw(win)
    for i in enemies:
        i.draw(win)
    # goblin.draw(win)
    dis.draw(win)
    pygame.display.update()



# MainLoop
dis = display()
man = player(300, 410, 64, 64)
enemies = []
goblin = enemy(100, 410, 64, 64, 450)
enemies.append(goblin)
bullets = []
run = True
while run:
    clock.tick(27)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bulletSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                bullets.append(
                    projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            enemies.append(enemy(random.randrange(50, screen_width-50), 410, 64, 64, 450))


    for bullet in bullets:
        for i in enemies:
            if bullet.y - bullet.radius < i.hitbox[1] + i.hitbox[3] and bullet.y + bullet.radius > i.hitbox[1]:
                if bullet.x + bullet.radius > i.hitbox[0] and bullet.x - bullet.radius < i.hitbox[0] + i.hitbox[2]:
                    if i.hit() <= 0:
                        enemies.pop(enemies.index(i))
                        dis.score += 1
                    bullets.pop(bullets.index(bullet))

        if bullet.x < screen_width and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    for j in enemies:
        if j.y < man.hitbox[1] + man.hitbox[3] and j.y + j.height > man.hitbox[1]:
            if j.x + j.width > man.hitbox[0] and j.x < man.hitbox[0] + man.hitbox[2]:
                if man.hp <= 0:
                    dis.game_over()
                else:
                    man.hit()
                    if j.hit() <= 0:
                        enemies.pop(enemies.index(j))
                        dis.score += 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screen_width - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= int((man.jumpCount ** 2) * 0.5 * neg)
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10


    redrawGameWindow()

pygame.quit

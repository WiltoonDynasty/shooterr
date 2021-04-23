from pygame import *
from random import randint
from time import time as timer
#подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
 
font2 = font.SysFont('Arial', 36)
 
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_bullet = "bullet.png" #пуля
img_hero = "rocket.png" #герой
img_enemy = "ufo.png" #враг
img_enemy2 = "ufo5.png" #враг
img_ast = "asteroid.png"

score = 0 #сбито кораблей
goal = 10 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 3 #проиграли, если пропустили столько
life = 3
life_enemy = 2

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
#конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
#метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
#класс спрайта-врага  
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Enemy2(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 0

#класс спрайта-пули  
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
#создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

#создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

monsters2 = sprite.Group()
for i in range(1, 6):
    monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster2)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy2(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False

rel_time = False

num_fire = 0
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна

while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    if num_fire < 7 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire()
                    if num_fire >= 7 and rel_time == False:
                        last_time = timer()
                        rel_time = True
#сама игра: действия спрайтов, роверка правил игры, перерисовка
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
 
        #производим движения спрайтов
        ship.update()
        monsters.update()
        monsters2.update()
        bullets.update()
        asteroids.update()
 
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        monsters2.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render("Wait, reload..", 1,(150, 0 ,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        collides = sprite.groupcollide(monsters2, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters2.add(monster2)

        collides = sprite.groupcollide(asteroids, bullets, False, True)
        for c in collides:
            score = score + 0
            monster = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or sprite.spritecollide(ship, monsters2, False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200, 200))

        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters2.add(monster2)

        if sprite.spritecollide(ship, monsters,False) or sprite.spritecollide(ship,asteroids, False) or sprite.spritecollide(ship, monsters2,False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, monsters2, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        #проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
  
        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if life == 3:
            life_color = (3, 252, 73)
        if life == 2:
            life_color = (232, 232, 0)
        if life == 1:
            life_color = (232, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life,(650, 10))

        display.update()
    #бонус: автоматический перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for m in monsters2:
            m.kill()
 
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        time.delay(3000)
        for i in range(1, 5):
            monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
            monsters2.add(monster2)

    time.delay(50)
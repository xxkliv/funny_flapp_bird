# импортирование необходимых модулей
import pygame, sys
from pygame.locals import QUIT, K_SPACE # K_SPACE - пробел
from random import randint

# инициализация модуля Pygame
pygame.init()

# Скорость игры. ограничение количества кадров в игре
FPS = 60
Frames = pygame.time.Clock()

# размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# цвета
BG = (70, 195, 219)

# название в шапке графического интерфейса
pygame.display.set_caption('Funny flappy bird')

screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# создание класса определяющий состояние игры
class Game:
    def __init__(self):
        self.status = True
        # новые свойства определения очков
        self.points = 0 #Количество набранных очков
        self.distance = 0 #Расстояние, которое преодолела птичка
        self.points_color = (250, 238, 28) #Цвет отображаемых очков
        self.font = pygame.font.Font('freesansbold.ttf', 40) #Шрифт для текста
        self.text = self.font.render(f'Счёт: {str(self.points)}', True, self.points_color) #Объект текста для отображения
        self.rect = self.text.get_rect() #Объект текста для получения свойств его позиционирования на экране
        self.rect.left = SCREEN_WIDTH / 2 - self.rect.width / 2 #Положение по оси-х
        self.rect.top = 20 #Положение по оси-у

    # метод отображения очков
    def draw_points(self, surface):
        self.text = self.font.render(f'Счёт:{str(self.points)}', True, self.points_color)
        surface.blit(self.text, self.rect)

    # метод обновления очков
    def update_points(self):
        self.distance  += 1
        if not self.distance % 10 and self.status:
            self.points += 1

    def get_status(self):
        return self.status

    def end_game(self):
        self.status = False

    def end_title(self, surface):
        text_color = (254, 255, 137)
        #bg_color = (48, 58, 82)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('КОНЕЦ ИГРЫ', True, text_color)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        surface.blit(text, textRect)

# создание класса препятсвий
class Pipe:
    def __init__(self):
        # базовые свойства
        self.speed = -2
        self.width = 80 #Ширина препятствия
        self.heigth = 180 #Высота препятствия
        # верхнее препятствие
        self.image_top = pygame.image.load('pipe.png') #Загружаем спрайт препятствия в игру
        self.image_top = pygame.transform.rotate(self.image_top, 180)
        self.image_top = pygame.transform.smoothscale(self.image_top, (self.width, self.heigth))
        self.rect_top = self.image_top.get_rect()
        self.rect_top.top = 0
        self.rect_top.right = SCREEN_WIDTH + self.width
        # нижнее препятсвие
        self.image_bottom = pygame.image.load('pipe.png')
        self.image_bottom = pygame.transform.smoothscale(self.image_bottom, (self.width, self.heigth))
        self.rect_bottom = self.image_bottom.get_rect()
        self.rect_bottom.bottom = SCREEN_HEIGHT
        self.rect_bottom.right = SCREEN_WIDTH + self.width


    def update(self):
        # верхнее препятсвие
        self.rect_top.move_ip(self.speed, 0)
        # нижнее препятсвие
        self.rect_bottom.move_ip(self.speed, 0)
        if self.rect_top.right < 0:
            # верхнее препятсвие
            self.image_top = pygame.transform.smoothscale(self.image_top, (self.width, self.random_height()))
            self.rect_top = self.image_top.get_rect()
            self.rect_top.right = SCREEN_WIDTH + self.width
            # нижнее препятсвие
            self.image_bottom = pygame.transform.smoothscale(self.image_bottom, (self.width, self.random_height()))
            self.rect_bottom = self.image_bottom.get_rect()
            self.rect_bottom.bottom = SCREEN_HEIGHT
            self.rect_bottom.right = SCREEN_WIDTH + self.width


    def draw(self, surface):
        #верхнее препятсвие
        surface.blit(self.image_top, self.rect_top)
        # нижнее препятсвие
        surface.blit(self.image_bottom, self.rect_bottom)

    def random_height(self):
        return randint(100, 250)

# создание класса bird
class Bird:
    def __init__(self):
        self.image = pygame.image.load('flappy bird.png') # загружаем изображение
        self.rect = self.image.get_rect() # Создание базового объекта rectangle, с помощью которого мы сможем управлять нашей птичкой на графическом интерфейса
        self.rect.top = SCREEN_HEIGHT / 2 - self.rect.height / 2 #Определяем позицию этого четырехугольника на экране относительно верхней части экрана. В данном случае мы разместим птичку по вертикальному центру.
        self.rect.left = 20 #С помощью этого свойства мы разместим птичку на расстоянии в 20 пикселей, относительно левой части экрана.

        #создаем метод для изображения птички
        self.velocity = 1 # скорость падения
        self.gravity = 0.2 # гравитация

        # свойства наклона птички
        self.angle = 0 # текущее значение угла наклона
        self.angle_speed = 2.5 # скорость измерения угла наклона
        self.rising = False # определение взлёта или падения. True - взлет, False - падение

    # отображение птички в окне
    def draw(self, surface):
        # surface.blit(self.image, self.rect)
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        surface.blit(rotated_image, self.rect)

    # Метод обновления данных для объекта птичка
    def update(self):
        self.rect.move_ip(0, self.velocity)
        self.velocity += self.gravity
        self.key_press()

        # обновление наклона птички
        if self.velocity > 0: #Если скорость падения птички будет больше нуля это означает, что птичка начала падать,
            self.rising = False #поэтому мы изменяем свойство определяющее взлет или падение.

        if self.rising and self.angle < 25: #Если птичка взлетает и угол наклона меньше 25,
            self.angle += self.angle_speed #увеличиваем угол наклона птички на скорость наклона
        elif not self.rising and self.angle > -15: #Как и в случае взлета при падении мы ограничиваем максимальный градус наклона.
            self.angle -= self.angle_speed * 0.5 #Также скорость изменения угла падения будет в два раза меньше чем скорость изменения угла взлета

    # Метод определения нажатия на клавиши
    def key_press(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            self.velocity = -5
            self.rising = True # определение "взлёта"
            print('Нажали на пробел.')

    # проверка столкновений
    def check_collision(self, pipe):
        if (pipe.rect_top.left <= self.rect.right and pipe.rect_top.bottom >= self.rect.top) \
            or (pipe.rect_bottom.left <= self.rect.right and pipe.rect_bottom.top <= self.rect.bottom) or self.rect.bottom >= SCREEN_HEIGHT:
            game.end_game()

bird = Bird()
pipe = Pipe()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # обновление данных для объектов
    if game.get_status():
        bird.update()
        pipe.update()
        game.update_points()
        bird.check_collision(pipe) # проверка столконовений

    # отрисовка объектов
    screen_surface.fill(BG) # заполнение цветом созданного пространства
    bird.draw(screen_surface)
    pipe.draw(screen_surface)
    game.draw_points(screen_surface)
    if not game.get_status():
        game.end_title(screen_surface)
    pygame.display.update() #обновление всех свойств
    Frames.tick(FPS) #ограничение количества кадров в исполняемом графическом интерфейсе

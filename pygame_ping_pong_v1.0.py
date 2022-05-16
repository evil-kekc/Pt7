import sys
import pygame as pg


pg.init()

pg.display.set_caption('Ping pong')  # Создание названия приложения (в шапке)
img = pg.image.load('andr.png')  # Получение изображения и присваивание его переменной
pg.display.set_icon(img)  # Отрисовка иконки приложения

FPS = 120
window_width = 600
window_height = 400

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
background_colour = (192, 192, 192)
blue = (12, 56, 84)

r = 20

width_rect = 100
height_rect = 10

x_ball, y_ball = 100, 200
direct_x_ball, direct_y_ball = 1, 1

x_rect = (window_width // 2 - width_rect // 2)
y_rect = window_height - height_rect
direct_x_rect = 5

screen = pg.display.set_mode((window_width, window_height))

clock = pg.time.Clock()

score_count = 0

run = True

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEMOTION:
            position = event.pos
            x_rect = position[0]  - (width_rect // 2)

    """Анимация"""
    clock.tick(FPS)
    screen.fill(blue)
    pg.event.pump()

    ball = pg.draw.circle(screen, white, (x_ball, y_ball), r)
    pg.draw.line(screen, white, (window_width // 2, 0), (window_width // 2, window_height), 8)
    pg.draw.rect(screen, black,
                 (x_rect, y_rect, width_rect, height_rect)
                 )

    """Перемещение"""
    if pg.key.get_pressed()[pg.K_LEFT]:
        x_rect -= direct_x_rect

    if pg.key.get_pressed()[pg.K_RIGHT]:
        x_rect += direct_x_rect

    x_ball += direct_x_ball
    if x_ball >= window_width - r or x_ball <= 0 + r:
        direct_x_ball = -direct_x_ball

    y_ball += direct_y_ball
    if y_ball <= 0 + r:
        direct_y_ball = -direct_y_ball

    if x_ball in range(x_rect, x_rect + width_rect) and y_ball + r in range(y_rect, y_rect + height_rect):
        direct_y_ball = -direct_y_ball
        score_count += 1
        FPS += 10

    if y_ball + r >= window_height:
        font_ = pg.font.SysFont('tahoma', 32)
        text = font_.render(f'Ваш счет: {score_count}', True, red)
        screen.blit(text, (200, 175))
        FPS = 120
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_ENTER:
                    x_ball, y_ball = 100, 50
                    score_count = 0

    pg.display.update()

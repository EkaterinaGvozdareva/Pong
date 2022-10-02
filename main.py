import pygame
import random

pygame.init()
pygame.font.init()
black = (0, 0, 0)
green = (0, 200, 64)
yellow = (225, 225, 0)
white = (255, 255, 255)

title = 'Pong'
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))  # Создание окна
pygame.display.set_caption(title)  # Добавляем название

block_width = 100
block_height = 15
block_speed = 10
block_rect = pygame.rect.Rect(screen_width / 2 - block_width / 2, screen_height - block_height * 2, block_width,
                              block_height)

ball_radius = 15
ball_speed = 7
ball_first_collide = False
ball_x_speed = 0
ball_y_speed = ball_speed
ball_rect = pygame.rect.Rect(screen_width / 2 - ball_radius, screen_height / 2 - ball_radius, ball_radius * 2,
                             ball_radius * 2)

score = 0
arial_font = pygame.font.match_font('arial')
arial_font_48 = pygame.font.Font(arial_font, 48)
arial_font_36 = pygame.font.Font(arial_font, 36)
clock = pygame.time.Clock()

game_over = False
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверяем выход
            game = False
            continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game = False
                continue
            elif event.key == pygame.K_SPACE:
                game_over = False

                block_rect.centerx = screen_width / 2
                block_rect.bottom = screen_height - block_height

                ball_rect.center = [screen_width / 2, screen_height / 2]
                ball_x_speed = 0
                ball_y_speed = ball_speed

                score = 0
                ball_first_collide = False

    screen.fill(black)
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            block_rect.x -= block_speed
        elif keys[pygame.K_RIGHT]:
            block_rect.x += block_speed
        pygame.draw.rect(screen, green, block_rect)  # Блок
        if block_rect.colliderect(ball_rect):  # Если столкнулись
            if not ball_first_collide:
                if random.choice(['right', 'left']) == 'right':
                    ball_x_speed = ball_speed
                else:
                    ball_x_speed = -ball_speed
                ball_first_collide = True
            ball_y_speed = -ball_speed
            score += 1

    ball_rect.x += ball_x_speed
    ball_rect.y += ball_y_speed

    if ball_rect.bottom >= screen_height:
        game_over = True
        ball_y_speed = -ball_speed
    elif ball_rect.top <= 0:
        ball_y_speed = ball_speed
    elif ball_rect.left <= 0:
        ball_x_speed = ball_speed
    elif ball_rect.right >= screen_width:
        ball_x_speed = -ball_speed

    pygame.draw.circle(screen, yellow, ball_rect.center, ball_radius)  # Шарик

    score_print = arial_font_48.render('Score: ' + str(score), True, white)  # Печать очков
    if not game_over:
        screen.blit(score_print, [screen_width / 2 - score_print.get_width() / 2, 15])  # Расположение их на экране
    else:
        retry_surface = arial_font_36.render('press SPACE to restart', True, white)
        screen.blit(score_print,
                    [screen_width / 2 - score_print.get_width() / 2, screen_height / 4])
        screen.blit(retry_surface,
                    [screen_width / 2 - retry_surface.get_width() / 2,
                     screen_height / 3 + score_print.get_height()])

    clock.tick(60)  # Замедление блока
    pygame.display.flip()  # Обновление экрана

pygame.quit()

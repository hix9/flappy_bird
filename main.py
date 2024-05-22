import pygame
import random

from constants import (
    FPS, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, SCROLL_SPEED, PIPE_FREQ
)
from bird import Bird
from pipe import Pipe
from button import Button

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Initialize font
font = pygame.font.SysFont('Impact', 60)

#define game variables
ground_scroll = 0
flying = False
game_over = False
last_pipe = pygame.time.get_ticks() - PIPE_FREQ
score = 0
pass_pipe = False

#import images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    score = 0
    return score


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)
#create restart button instance
button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, button_img)


def main():
    global ground_scroll, flying, game_over, last_pipe, score, pass_pipe
    while True:
        clock.tick(FPS)
        #draw background
        screen.blit(bg, (0, 0))
        bird_group.draw(screen)
        bird_group.update(flying, game_over)
        pipe_group.draw(screen)
        #draw the ground
        screen.blit(ground_img, (ground_scroll, 768))
        draw_text(str(score), font, WHITE, int(SCREEN_WIDTH / 2), 20)
        #look for collision
        if (
            pygame.sprite.groupcollide(
                bird_group, pipe_group, False, False
            ) or flappy.rect.top < 0
        ):
            game_over = True
        #check the score
        if len(pipe_group) > 0:
            if (bird_group.sprites()[0].rect.left
                > pipe_group.sprites()[0].rect.left
                and bird_group.sprites()[0].rect.right
                < pipe_group.sprites()[0].rect.right
               and pass_pipe is False):
                pass_pipe = True
            if pass_pipe is True:
                if (
                    bird_group.sprites()[0].rect.left
                    > pipe_group.sprites()[0].rect.right
                ):
                    score += 1
                    pass_pipe = False
        #check if bird has hit the ground
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False
        if game_over is False and flying is True:
            #generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > PIPE_FREQ:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(
                    SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1
                )
                top_pipe = Pipe(
                    SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1
                )
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            #draw and scroll the ground
            ground_scroll -= SCROLL_SPEED
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe_group.update()
        #check for game over and reset
        if game_over is True:
            if button.draw() is True:
                game_over = False
                score = reset_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if (event.type == pygame.MOUSEBUTTONDOWN and
               flying is False and game_over is False):
                flying = True
        pygame.display.update()


if __name__ == "__main__":
    main()

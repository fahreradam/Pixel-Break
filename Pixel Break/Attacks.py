import pygame
import random


class Attacks:

    def __init__(self, direction, paddle_height, screen_w, screen_h):
        self.x = 0
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.wide = 0
        self.high = 0
        self.damage = 0
        self.speed = 700
        self.direction = direction
        self.attk_timer = 7
        self.y = 0
        self.ph = paddle_height
        if self.direction == 1:
            self.x = 1
            self.y = paddle_height
            self.high = 60
        if self.direction == 2:
            self.x = screen_w
            self.y = paddle_height
            self.high = 60


    def update(self, dt):

        if self.direction == 1:

            if self.wide < 200:
                self.wide += self.speed * dt
            if self.wide >= 200:
                self.x += self.speed * dt
            if self.x >= self.screen_w:
                self.direction = 0


    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, int(self.wide), int(self.high)))

done = False
win = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

left_attk = Attacks(1, 400, 800, 600)

while not done:
    dt = clock.tick() / 1000
    win.fill((0, 0, 0))
    left_attk.update(dt)
    if left_attk.direction != 0:
        print("true")
        left_attk.draw(win)
    pygame.display.flip()
pygame.quit()
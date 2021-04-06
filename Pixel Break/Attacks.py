import pygame
import random


class Attacks:

    def __init__(self, direction, paddle_height, paddle_width, screen_w, screen_h, paddle_x):
        self.is_attack = True
        self.x = 0
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.wide = 0
        self.high = 0
        self.damage = 0
        self.speed = 500
        self.direction = direction
        self.attk_timer = 7
        self.y = 0
        self.ph = paddle_height
        self.blink_timer = 2
        self.blink_timer2 = 0
        if self.direction == 1:
            self.x = 1
            self.y = paddle_height + 15
            self.high = 30
        if self.direction == 2:
            self.x = screen_w
            self.y = paddle_height + 30
            self.high = 30
        if self.direction == 3:
            self.y = screen_h
            self.wide = 30
            lr = random.randint(1, 2)
            if lr == 1:
                self.x = 400
            if lr == 2:
                self.x = 200
        if self.direction == 4:
            self.y = 1
            self.wide = 30
            lr = random.randint(1, 2)
            if lr == 1:
                self.x = paddle_x - 100
            if lr == 2:
                self.x = paddle_x + paddle_width + 100

    def update(self, dt):

        if self.direction == 1:

            if self.wide < 200:
                self.wide += self.speed * dt
            if self.wide >= 200:
                self.x += self.speed * dt
            if self.x >= self.screen_w:
                self.direction = 0

        if self.direction == 2:

            if self.wide < 200:
                self.wide += self.speed * dt
                self.x -= self.speed * dt
            if self.wide >= 200:
                self.x -= self.speed * dt
            if self.x + self.wide <= 0:
                self.direction = 0

        if self.direction == 3:

            if self.high < 200:
                self.high += self.speed * dt
                self.y -= self.speed * dt
            if self.high >= 200:
                self.y -= self.speed * dt
            if self.y + self.high <= 0:
                self.direction = 0

        if self.direction == 4:

            if self.high < 200:
                self.high += self.speed * dt
            if self.high >= 200:
                self.y += self.speed * dt
            if self.y >= self.screen_h:
                self.direction = 0

    def draw(self, win):

        self.rect = pygame.draw.rect(win, (150, 0, 255), (self.x, self.y, int(self.wide), int(self.high)))




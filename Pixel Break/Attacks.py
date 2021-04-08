import pygame
import random


class Attacks:

    def __init__(self, direction, paddle_height, paddle_width, screen_w, screen_h, paddle_x, other_x=0, attack2=False):
        self.is_attack2 = attack2
        self.ox = 0
        self.is_attack = True
        self.x = 0
        self.px = paddle_x
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
        self.rect = None
        if other_x != 0:
            self.x = self.ox

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

        if self.direction == 5:
            self.y = 1
            self.wide = 30
            if not attack2:
                lr = random.randint(1, 2)
                if lr == 1:
                    self.x = paddle_x - 100
                if lr == 2:
                    self.x = paddle_x + paddle_width + 100
            if attack2:
                self.x = other_x

        if self.direction == 6:
            self.y = 1
            self.wide = 30

            lr = random.randint(1, 2)
            if lr == 1:
                self.x = paddle_x - 100
                self.ox = paddle_x - 100
            if lr == 2:
                self.x = paddle_x + paddle_width + 100
                self.ox = paddle_x + paddle_width + 100
            self.attack2 = Attacks(5, paddle_height, paddle_width, screen_w, screen_h, paddle_x, self.ox, True)
        else:
            self.attack2 = None







    def update(self, dt, win):

        if self.direction == 1:

            if self.wide < 30:
                self.wide += self.speed * dt
            if self.wide >= 30:
                self.x += self.speed * dt
            if self.x >= self.screen_w:
                self.direction = 0

        if self.direction == 2:

            if self.wide < 30:
                self.wide += self.speed * dt
                self.x -= self.speed * dt
            if self.wide >= 30:
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

        if self.direction == 5:
            if self.high < 200:
                self.high += self.speed * dt

            if self.high >= 200 and self.y < self.ph - (self.high / 2):
                self.y += self.speed * dt
            if not self.is_attack2:
                if self.y >= self.ph - (self.high / 2):

                    if self.x <= self.px:

                        self.direction = 1


                    elif self.x >= self.px:

                        self.direction = 2
            else:
                if self.y >= self.ph - (self.high / 2):
                    print("TRUE")
                    self.direction = 2


        if self.direction == 6:
            if self.high < 200:
                self.high += self.speed * dt

            if self.high >= 200 and self.y < self.ph - (self.high / 2):
                self.y += self.speed * dt
            if self.y >= self.ph - (self.high / 2):
                self.direction = 1

        if self.attack2 != None:

            self.attack2.update(dt, win)
            self.attack2.draw(win)

    def draw(self, win):

        self.rect = pygame.draw.rect(win, (150, 0, 255), (self.x, self.y, int(self.wide), int(self.high)))




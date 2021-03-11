import pygame


class Paddle:
    def __init__(self, win, x, y):
        self.win = win
        self.speed = 100
        self.stamina = 100
        self.position = [x, y]

    def draw(self):
        pygame.draw.rect(self.win, (255, 0, 0), (self.position[0], self.position[1], self.stamina, 10))

    def move(self, keys, dt):
        if keys[pygame.K_a]:
            self.position[0] -= self.speed * dt
            if keys[pygame.K_SPACE] and self.stamina >= 1:
                self.speed = 200
                if self.stamina >= 1:
                    self.stamina -= 5 * dt
            else:
                self.speed = 100
        if keys[pygame.K_d]:
            self.position[0] += self.speed * dt
            if keys[pygame.K_SPACE] and self.stamina >= 1:
                self.speed = 200
                if self.stamina >= 1:
                    self.stamina -= 5 * dt
            else:
                self.speed = 100

    def collide(self):
        if self.position[0] <= 0:
            self.position[0] = 0
        if self.position[0] + self.stamina >= self.win.get_width():
            self.position[0] = self.win.get_width() - self.stamina

import pygame

class Ball:
    def __init__(self, x, y, surf):
        self.position = [x, y]
        self.win = surf
        self.direction = 0

    def draw(self):
        pygame.draw.circle(self.win, (255, 255, 255), self.position, 5)

    def move(self, dt, paddle, target_point):


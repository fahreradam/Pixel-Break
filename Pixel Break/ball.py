import pygame

class Ball:
    def __init__(self, x, y, surf):
        self.position = [x, y]
        self.win = surf
        self.direction = 0

    def draw(self):
        pygame.draw.circle(self.win, (255, 255, 255), self.position, 5)

    def move(self, dt, paddle_pos, target_point):
        v = [self.position[0] - paddle_pos[0], self.position[1] - paddle_pos[1]]

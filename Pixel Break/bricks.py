import pygame
import random

class Brick:
    def __init__(self, pos, wh, code, toughscore = 1):
        self.col_w_h = wh
        half_x = wh[0]/2
        half_y = wh[1]/2
        self.pos = [pos[0] + 135, pos[1] + 120]
        self.top_point      = (self.pos[0] + half_x, self.pos[1])
        self.bottom_point   = (self.pos[0] + half_x, self.pos[1] + wh[1])
        self.right_point    = (self.pos[0] + wh[0], self.pos[1] + half_y)
        self.left_point     = (self.pos[0],  self.pos[1] + half_y)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], wh[0], wh[1])
        self.code = code
        self.powerup = None
        self.toughness = toughscore
        if random.randint(0, 50) == 50:
            if random.randint(0, 1) == 0:
                self.powerup = "Heavy"
            elif random.randint(0, 1) == 1:
                self.powerup = "Speed"

    def get_rect(self):
        return self.rect
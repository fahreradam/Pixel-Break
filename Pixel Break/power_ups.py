import pygame


class Power_ups:
    def __init__(self, pos, tag, win):
        self.pos = pos
        self.power_up = tag
        self.win = win
        if self.power_up == "Heavy":
            self.im = pygame.image.load("images\\heavy_power_up.png")
        if self.power_up == "Speed":
            self.im = pygame.image.load("images\\speed_power_up.png")

    def draw(self):
        self.win.blit(self.im, self.pos)

    def move(self, dt):
        self.pos[1] += 100 * dt

import pygame

class Brick:
    def __init__(self, pos, wh, code):
        self.col_w_h = wh
        half_x = wh[0]/2
        half_y = wh[1]/2
        self.pos = pos
        self.top_point      = (pos[0] + half_x, pos[1])
        self.bottom_point   = (pos[0] + half_x, pos[1] + wh[1])
        self.right_point    = (pos[0] + wh[0], pos[1] + half_y)
        self.left_point     = (pos[0],  pos[1] + half_y)
        self.rect = pygame.Rect(pos[0], pos[1], wh[0], wh[1])
        self.code = code

    def get_rect(self):
        return self.rect
import pygame


class Ball:
    def __init__(self, x, y, surf):
        self.position = [x, y]
        self.win = surf
        self.direction = [1, 1]
        self.img = pygame.image.load("images\\Ball.png")
        self.img_scale = pygame.transform.scale(self.img, (10, 10))
        self.speed = 500
        self.radius = 5
        self.is_attack = False
    def draw(self):
        self.win.blit(self.img_scale, self.position)

    def move(self, dt):
        self.position = [(self.position[0] + self.direction[0] * dt * self.speed), (self.position[1] + self.direction[1]
                                                                                    * dt * self.speed)]

    def collision(self, paddle_pos, target_point, stamina):
        if pygame.Rect(self.position[0], self.position[1], 10, 10).colliderect(
                pygame.Rect(paddle_pos[0] - (stamina / 2), paddle_pos[1] - 5, stamina, 10)):
            v = [target_point[0] - paddle_pos[0], target_point[1] - paddle_pos[1]]
            mag_v = (v[0] ** 2 + v[1] ** 2) ** (1 / 2)
            unit_v = [v[0] / mag_v, v[1] / mag_v]
            print(unit_v)
            if unit_v[1] > 0:
                if unit_v[0] >= 0:
                    self.direction = [1, -1]
                if unit_v[0] <= 0:
                    self.direction = [-1, -1]
            else:
                self.direction = unit_v

        if self.position[0] <= 0:
            self.position[0] = 0
            self.direction = [-1 * self.direction[0], self.direction[1]]
        if self.position[0] + 10 >= self.win.get_width():
            self.position[0] = self.win.get_width() - 10
            self.direction = [-1 * self.direction[0], self.direction[1]]
        if self.position[1] <= 0:
            self.position[1] = 0
            self.direction = [self.direction[0], -1 * self.direction[1]]
        if self.position[1] + 10 >= self.win.get_height():
            self.position[1] = self.win.get_height() - 10
            self.direction = [self.direction[0], -1 * self.direction[1]]

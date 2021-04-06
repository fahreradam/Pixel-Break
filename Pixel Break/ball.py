import pygame
import vector

class Ball:
    def __init__(self, x, y, surf):
        self.position = [x, y]
        self.win = surf
        self.direction = [1, 1]
        self.img = pygame.image.load("images\\Ball.png")
        self.img_scale = pygame.transform.scale(self.img, (10, 10))
        self.speed = 250
        self.radius = 5
        self.is_attack = False
        # player life --
        # image
        self.life_img = pygame.image.load("images\\player life.png").convert()
        self.life1 = pygame.transform.scale(self.life_img, (20, 20))
        self.life2 = pygame.transform.scale(self.life_img, (20, 20))
        self.life3 = pygame.transform.scale(self.life_img, (20, 20))
        self.life_img_all = [self.life1, self.life2, self.life3]
        # count
        self.life_all = 3
        self.life_lost = 0
        # game over screen --
        self.game_over_img = pygame.image.load("images\\game over.png")

    def draw(self):
        self.win.blit(self.img_scale, self.position)
        # player lives
        if self.life_lost == 0:
            self.draw_lives_3()
        elif self.life_lost == 1:
            self.draw_lives_2()
        elif self.life_lost == 2:
            self.win.blit(self.life_img_all[2], (self.win.get_width() - 30, self.win.get_height() - 790))

    def move(self, dt):
        self.position = [(self.position[0] + self.direction[0] * dt * self.speed), (self.position[1] + self.direction[1]
                                                                                    * dt * self.speed)]

    def dot(self, v1, v2):
        """Preforming the dot product"""
        if v1.dim == v2.dim:
            i = 0
            sum = 0
            while i < v1.dim:
                d = v1[i] * v2[i]
                sum += d
                i += 1
            return sum

    def collision(self, paddle_pos, target_point, stamina):
        v = [target_point[0] - paddle_pos[0], target_point[1] - paddle_pos[1]]
        mag_v = (v[0] ** 2 + v[1] ** 2) ** (1 / 2)
        unit_v = [v[0] / mag_v, v[1] / mag_v]
        unit_perp = vector.Vector(-unit_v[1], unit_v[0])
        dir_to_ball = vector.Vector(self.position[0] - paddle_pos[0], self.position[1] - paddle_pos[1])
        d = self.dot(dir_to_ball, vector.Vector(unit_v[0], unit_v[1]))
        e = self.dot(dir_to_ball, unit_perp)

        if not pygame.key.get_pressed()[pygame.K_SPACE]:
            if pygame.Rect(self.position[0], self.position[1], 10, 10).colliderect(
                    pygame.Rect(paddle_pos[0] - (stamina / 2), paddle_pos[1] - 5, stamina, 10)):

                if not (abs(d) > 15 or abs(e) > int(stamina)):
                    print(stamina)
                    if unit_v[1] > 0:
                        if unit_v[0] >= 0:
                            self.direction = [1, -1]
                        if unit_v[0] <= 0:
                            self.direction = [-1, -1]
                    else:
                        self.direction = unit_v
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            if not (abs(d) > 15 or abs(e) > int(stamina)):
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
            #self.position[1] = self.win.get_height() - 10
            #self.direction = [self.direction[0], -1 * self.direction[1]]
            self.life_lost += 1
            self.position = paddle_pos

    def draw_lives_3(self):
        self.win.blit(self.life_img_all[2], (self.win.get_width() - 30, self.win.get_height() - 790))
        self.win.blit(self.life_img_all[1], (self.win.get_width() - 60, self.win.get_height() - 790))
        self.win.blit(self.life_img_all[0], (self.win.get_width() - 90, self.win.get_height() - 790))

    def draw_lives_2(self):
        self.win.blit(self.life_img_all[2], (self.win.get_width() - 30, self.win.get_height() - 790))
        self.win.blit(self.life_img_all[1], (self.win.get_width() - 60, self.win.get_height() - 790))

    def game_over(self):
        if self.life_lost == self.life_all:
            self.win.fill((0, 0, 0))
            self.win.blit(self.game_over_img, (0, 0))

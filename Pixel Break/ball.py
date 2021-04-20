import pygame
import vector


class Ball:
    def __init__(self, x, y, surf):
        self.position = [x, y]
        self.win = surf
        self.direction = [1, 1]
        self.img = pygame.image.load("images\\Ball.png")
        self.shadow_ball = pygame.image.load("images\\shadow ball.png")
        self.speed_img = pygame.image.load("images\\speed_power_up.png")
        self.heavy_img = pygame.image.load("images\\heavy_power_up.png")
        self.frame = pygame.image.load("images\\Power_up_frame.png")
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
        # game win screen --
        self.game_win_img = pygame.image.load("images\\Game Text - Win.png")

        self.end = False
        self.shadow_ball_pos = [x, y]
        self.shadow_dir = [1, 1]
        self.shadow_speed = 500
        self.stay = False
        self.powerup = None
        self.time = 0
        self.bounce = 0
        self.usable = []
        self.current_powerup = None
        self.brick_pos = None
        self.point = 0
        self.l_click = False
        self.r_click = False
        self.av_pos = []



    def draw(self):
        self.win.blit(self.img_scale, self.position)
        # player lives
        if self.life_lost == 0:
            self.draw_lives_3()
        elif self.life_lost == 1:
            self.draw_lives_2()
        elif self.life_lost == 2:
            self.win.blit(self.life_img_all[2], (self.win.get_width() - 30, self.win.get_height() - 790))
        # self.win.blit(self.shadow_ball, self.shadow_ball_pos)

    def move(self, dt):
        self.position = [(self.position[0] + self.direction[0] * dt * self.speed), (self.position[1] + self.direction[1]
                                                                                    * dt * self.speed)]

    def shadow(self, dt, paddle_pos):
        if not self.end:
            self.shadow_ball_pos = [(self.shadow_ball_pos[0] + self.shadow_dir[0] * dt * self.shadow_speed),
                                    (self.shadow_ball_pos[1] +
                                     self.shadow_dir[1] * dt * self.shadow_speed)]
        if self.shadow_ball_pos[1] >= paddle_pos[1]:
            self.end = True
            self.stay = True

        if self.stay:
            self.shadow_ball_pos = self.position
            self.shadow_dir = self.direction

        if self.shadow_ball_pos[0] <= 0:
            self.shadow_ball_pos[0] = 0
            self.shadow_dir = [-1 * self.shadow_dir[0], self.shadow_dir[1]]
        if self.shadow_ball_pos[0] + 10 >= self.win.get_width():
            self.shadow_ball_pos[0] = self.win.get_width() - 10
            self.shadow_dir = [-1 * self.shadow_dir[0], self.shadow_dir[1]]
        if self.shadow_ball_pos[1] <= 0:
            self.shadow_ball_pos[1] = 0
            self.shadow_dir = [self.shadow_dir[0], -1 * self.shadow_dir[1]]
        if self.shadow_ball_pos[1] + 10 >= self.win.get_height():
            self.shadow_ball_pos[1] = self.win.get_height() - 10
            self.shadow_dir = [self.shadow_dir[0], -1 * self.shadow_dir[1]]

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
            self.end = False
            self.stay = False
            if pygame.Rect(self.position[0], self.position[1], 10, 10).colliderect(
                    pygame.Rect(paddle_pos[0] - (stamina / 2), paddle_pos[1] - 5, stamina, 10)):

                if unit_v[1] > 0:
                    if unit_v[0] >= 0:
                        self.direction = [1, -1]
                    if unit_v[0] <= 0:
                        self.direction = [-1, -1]
                    if self.current_powerup == "Heavy":
                        self.bounce = self.bounce + 1
                else:
                    self.direction = unit_v
                    if self.current_powerup == "Heavy":
                        self.bounce = self.bounce + 1

        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            self.end = False
            self.stay = False
            if not (abs(d) > 15 or abs(e) > int(stamina)):
                if unit_v[1] > 0:
                    if unit_v[0] >= 0:
                        self.direction = [1, -1]
                    if unit_v[0] <= 0:
                        self.direction = [-1, -1]
                    if self.current_powerup == "Heavy":
                        self.bounce = self.bounce + 1
                else:
                    self.direction = unit_v
                    if self.current_powerup == "Heavy":
                        self.bounce = self.bounce + 1

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
            # self.position[1] = self.win.get_height() - 10
            # self.direction = [self.direction[0], -1 * self.direction[1]]
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
        if self.life_lost >= self.life_all:
            self.win.fill((0, 0, 0))
            self.win.blit(self.game_over_img, (0, 0))

    def game_win(self, health):
        if health <= 0:
            self.win.fill((0, 0, 0))
            self.win.blit(self.game_win_img, (self.win.get_width() / 2 -
                                              self.game_win_img.get_width() / 2, self.win.get_height() - 700))

    def power(self, dt, paddle_pos, stamina, mouse_click):
        for p in self.av_pos:
            if pygame.Rect(p.pos[0], p.pos[1], 10, 10).colliderect(
                    pygame.Rect(paddle_pos[0] - (stamina / 2), paddle_pos[1] - 5, stamina, 10)):
                if len(self.usable) <= 1:
                    self.usable.append(p.power_up)
                self.av_pos.remove(p)
            elif p.pos[1] >= self.win.get_height():
                self.av_pos.remove(p)
        if len(self.usable) >= 1:
            if mouse_click[0]:
                self.l_click = True
            if self.l_click:
                self.current_powerup = self.usable[0]
                if self.current_powerup == "Heavy":
                    self.heavy()
                if self.current_powerup == "Speed":
                    self.speedy_boy(dt)
        if len(self.usable) == 2:
            if mouse_click[2]:
                self.r_click = True
            if self.r_click:
                self.current_powerup = self.usable[1]
                if self.current_powerup == "Heavy":
                    self.heavy()
                if self.current_powerup == "Speed":
                    self.speedy_boy(dt)
        if len(self.usable) > 0:
            if self.usable[0] == "Heavy":
                self.win.blit(self.heavy_img, (500, 750))
            if self.usable[0] == "Speed":
                self.win.blit(self.speed_img, (500, 750))
            if len(self.usable) > 1:
                if self.usable[1] == "Heavy":
                    self.win.blit(self.heavy_img, (530, 750))
                if self.usable[1] == "Speed":
                    self.win.blit(self.speed_img, (530, 750))

        if self.current_powerup == None:
            self.r_click = False
            self.l_click = False

    def heavy(self):
        if self.position[0] <= 0:
            self.bounce = self.bounce + 1
        if self.position[0] + 10 >= self.win.get_width():
            self.bounce = self.bounce + 1
        if self.position[1] <= 0:
            self.bounce = self.bounce + 1
        if self.position[1] + 10 >= self.win.get_height():
            self.current_powerup = None
            self.usable.pop(0)
        if self.bounce >= 2:
            self.current_powerup = None
            self.usable.pop(0)
            self.bounce = 0

    def speedy_boy(self, dt):
        if self.time <= 2:
            self.speed = 500
            self.time += dt

        if self.time > 2:

            self.speed = 250
            self.time = 0
            self.usable.pop(0)
            self.current_powerup = None

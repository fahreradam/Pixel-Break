import pygame
import math
import copy
import power_ups

class Paddle:
    def __init__(self, win, x, y, ball):
        self.win = win
        self.speed = 200
        self.stamina = 100
        self.position = [x, y]
        self.orientation = 0  # In degrees
        self.actual_stamina = pygame.image.load("images\\stamina bar.png")
        self.full_stamina = pygame.image.load("images\\stamina bar back.png")
        self.radius = self.actual_stamina.get_width() / 2
        self.collide_type = 0
        self.dashing = False
        self.ball = ball
        self.score = 0
        self.av_power = []

    def draw(self):
        final_surf = pygame.transform.scale(self.actual_stamina, (int(self.stamina), 10))
        full_stamina = pygame.transform.scale(self.full_stamina, (100, 10))
        temp_surf = pygame.transform.rotate(final_surf, self.orientation)
        frame = pygame.transform.rotate(full_stamina, self.orientation)

        self.win.blit(temp_surf, (self.position[0] - temp_surf.get_width() / 2,
                                  self.position[1] - temp_surf.get_height() / 2))
        self.win.blit(frame, (self.position[0] - frame.get_width() / 2,
                              self.position[1] - frame.get_height() / 2))
        for p in self.av_power:
            p.draw()

    def move(self, direction, dt):
        dist = self.speed * direction * dt
        radians = math.radians(self.orientation)
        opposite = -dist * math.sin(radians)
        adjacent = dist * math.cos(radians)
        self.position[0] += adjacent
        self.position[1] += opposite



    def collide(self):
        if self.position[0] - 50 <= 0:
            self.position[0] = 50
        if self.position[0] + 50 >= self.win.get_width():
            self.position[0] = self.win.get_width() - 50

    def handle_input(self, dt, keys, event):
        if keys[pygame.K_d]:
            # self.move(1, dt)
            self.position[0] += self.speed * dt

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and self.stamina >= 10:
                    self.position[0] = 100 + self.position[0]
                    self.stamina -= 10
        if keys[pygame.K_a]:
            # self.move(-1, dt)
            self.position[0] -= self.speed * dt
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and self.stamina >= 10:
                    self.position[0] = self.position[0] - 100
                    self.stamina -= 10
                    self.dashing = True
            else:
                self.dashing = False
        if self.stamina <= 100:
            self.stamina += 5 * dt
        for p in self.av_power:
            p.move(dt)

    def point_towards(self, target_pt, keys, dt):
        if keys[pygame.K_SPACE]:
            adjacent = target_pt[0] - self.position[0]
            opposite = -(target_pt[1] - self.position[1])
            self.orientation = math.degrees(math.atan2(opposite, adjacent)) - 90
            self.stamina -= 6 * dt
        else:
            self.orientation = 0
            self.center = 0

    def collision(self, collide_list, dashing=False):

        sfactor = 0.8
        stamina_bar = pygame.Rect((self.position[0] - (self.stamina / 2), self.position[1], self.stamina, 10))

        for object in collide_list:

            if not object.is_attack:
                circle_box = pygame.Rect(int(object.position[0] - object.radius),
                                         int(object.position[1] - object.radius), object.radius * 2, object.radius * 2)
                if stamina_bar.colliderect(circle_box):
                    self.ball_bounce = True


            elif object.is_attack and dashing == False:

                if stamina_bar.colliderect(object.rect):
                    if self.stamina >= 1:
                        self.stamina -= sfactor

    def pixel_collision(self, pixel_list, ball_x, ball_y, ball_width, direction):

        for p in pixel_list:
            circle_box = pygame.Rect(int(ball_x - ball_width), int(ball_y - ball_width), 10, 10)
            if circle_box.colliderect(p.get_rect()):
                if self.ball.current_powerup == "Heavy":
                    if ball_x < p.right_point[0] and ball_x < p.top_point[0] and ball_x < p.bottom_point[0] and ball_x >= \
                            p.left_point[0]:
                        pixel_list.remove(p)
                    elif ball_x > p.left_point[0] and ball_x > p.top_point[0] and ball_x > p.bottom_point[0] and ball_x <= \
                            p.right_point[0]:
                        pixel_list.remove(p)
                    elif ball_y > p.left_point[1] and ball_y > p.top_point[1] and ball_y > p.right_point[1] and ball_y <= \
                            p.bottom_point[1]:
                        pixel_list.remove(p)
                    elif ball_y < p.left_point[1] and ball_y < p.top_point[1] and ball_y < p.right_point[1] and ball_y >= \
                            p.bottom_point[1]:
                        pixel_list.remove(p)
                else:
                    if ball_x < p.right_point[0] and ball_x < p.top_point[0] and ball_x < p.bottom_point[0] and ball_x >= \
                            p.left_point[0]:
                        direction[0] = direction[0] * -1  # LEFT
                        if p.toughness != 0:
                            p.toughness -= 1
                        else:
                            pixel_list.remove(p)
                    elif ball_x > p.left_point[0] and ball_x > p.top_point[0] and ball_x > p.bottom_point[0] and ball_x <= \
                            p.right_point[0]:
                        direction[0] = direction[0] * -1  # RIGHT
                        if p.toughness != 0:
                            p.toughness -= 1
                        else:
                            pixel_list.remove(p)
                    elif ball_y > p.left_point[1] and ball_y > p.top_point[1] and ball_y > p.right_point[1] and ball_y <= \
                            p.bottom_point[1]:
                        direction[1] = direction[1] * -1  # BOTTOM
                        if p.toughness != 0:
                            p.toughness -= 1
                        else:
                            pixel_list.remove(p)
                    elif ball_y < p.left_point[1] and ball_y < p.top_point[1] and ball_y < p.right_point[1] and ball_y >= \
                            p.bottom_point[1]:
                        direction[1] = direction[1] * -1  # TOP
                        if p.toughness != 0:
                            p.toughness -= 1
                        else:
                            pixel_list.remove(p)
                if p.powerup is not None:
                    self.av_power.append(power_ups.Power_ups(copy.deepcopy(p.pos), p.powerup, self.win))
                self.ball.av_pos = self.av_power
                self.score += 5


    def distance(self, x1, y1, x2, y2):
        space = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

        return space

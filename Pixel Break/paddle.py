import pygame
import math


class Paddle:
    def __init__(self, win, x, y):
        self.win = win
        self.speed = 100
        self.stamina = 100
        self.position = [x, y]
        self.orientation = 0  # In degrees
        self.actual_stamina = pygame.image.load("images\\stamina bar.png")
        self.full_stamina = pygame.image.load("images\\stamina bar back.png")

    def draw(self):
        final_surf = pygame.transform.scale(self.actual_stamina, (int(self.stamina), 10))
        full_stamina = pygame.transform.scale(self.full_stamina, (100, 10))
        temp_surf = pygame.transform.rotate(final_surf, self.orientation)
        frame = pygame.transform.rotate(full_stamina, self.orientation)

        self.win.blit(temp_surf, (self.position[0] - temp_surf.get_width() / 2,
                                  self.position[1] - temp_surf.get_height() / 2))
        self.win.blit(frame, (self.position[0] - frame.get_width() / 2,
                              self.position[1] - frame.get_height() / 2))

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
        if self.position[0] + self.stamina >= self.win.get_width():
            self.position[0] = self.win.get_width() - self.stamina

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
        if self.stamina <= 100:
            self.stamina += 5 * dt

    def point_towards(self, target_pt, keys, dt):
        if keys[pygame.K_SPACE]:
            adjacent = target_pt[0] - self.position[0]
            opposite = -(target_pt[1] - self.position[1])
            self.orientation = math.degrees(math.atan2(opposite, adjacent)) - 90
            self.stamina -= 6 * dt
        else:
            self.orientation = 0
            self.center = 0
import pygame






class Player:


    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.bar = img
        self.radius = self.bar.get_width() / 2
        self.collide_type = 0
    def collision(self, collide_list, dashing=False):
        sfactor = 0.2
        stamina_bar = pygame.Rect((self.x, self.y, int(self.bar.get_width()), int(self.bar.get_height())))

        for object in collide_list:

            if not object.is_attack:
                circle_box = pygame.Rect(int(object.x - object.radius), int(object.y - object.radius), object.radius * 2, object.radius * 2)
                if stamina_bar.colliderect(circle_box):
                    self.ball_bounce = True


            elif object.is_attack and dashing == False:

                if stamina_bar.colliderect(object):
                    self.bar = pygame.transform.scale(self.bar, (self.bar.get_width() - int(self.bar.get_width() * sfactor)))
    def pixel_collision(self, pixel_list, ball_x, ball_y, ball_width):

        for p in pixel_list:
            circle_box = pygame.Rect(int(ball_x - ball_width), int(ball_y - ball_width), ball_width * 2, ball_width * 2)
            if circle_box.colliderect(p.get_rect()):
                if ball_x + ball_width * 2 < p.right_point and ball_x + ball_width * 2 < p.top_point and ball_x + ball_width * 2 < p.bottom_point:
                    self.collide_type = 1 #LEFT SIDE COLLISION
                elif ball_x > p.left_point and ball_x > p.top_point and ball_x > p.bottom_point:
                    self.collide_type = 2 #RIGHT SIDE COLLISION
                elif ball_y > p.left_point and ball_y > p.top_point and ball_y > p.right_point:
                    self.collide_type = 3 #BOTTOM COLLISION
                else:
                    self.collide_type = 4 #TOP COLLISION

    def distance(self, x1, y1, x2, y2):
        space = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

        return space
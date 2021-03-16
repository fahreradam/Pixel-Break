import pygame
import math


class Paddle:
    def __init__(self, win, x, y):
        self.win = win
        self.speed = 100
        self.stamina = 100
        self.position = [x, y]
        self.orientation = 0  # In degrees
        self.center = 0
        self.rotation_rate = 90  # How fast does the ship rotate (in degrees / sec)
        self.img = pygame.image.load("images\\stamina bar.png")

    def draw(self):
        final_surf = pygame.transform.scale(self.img, (int(self.stamina), 10))
        temp_surf = pygame.transform.rotate(final_surf, self.orientation + self.center)

        self.win.blit(temp_surf, (self.position[0] - temp_surf.get_width() / 2,
                                  self.position[1] - temp_surf.get_height() / 2))
        self.win.blit(self.img, (self.position[0] - self.stamina / 2,
                                 self.position[1]))

    def move(self, direction, dt):
        dist = self.speed * direction * dt
        radians = math.radians(self.orientation)
        opposite = -dist * math.sin(radians)
        adjacent = dist * math.cos(radians)
        self.position[0] += adjacent
        self.position[1] += opposite

    def collide(self):
        if self.position[0] <= 0:
            self.position[0] = 0
        if self.position[0] + self.stamina >= self.win.get_width():
            self.position[0] = self.win.get_width() - self.stamina

    def rotate(self, direction, delta_time):
        """ direction should be (0 = no rotation, -1 = clockwise, +1 = counter_clockwise)
            delta_time is the time since the last frame
        """
        self.orientation += direction * self.rotation_rate * delta_time

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
            self.stamina += 2 * dt

    def point_towards(self, target_pt, keys):
        if keys[pygame.K_SPACE]:
            adjacent = target_pt[0] - self.position[0]
            opposite = -(target_pt[1] - self.position[1])
            self.orientation = math.degrees(math.atan2(opposite, adjacent)) + 90
            self.center = self.position[0] / 2
        else:
            self.orientation = 0
            self.center = 0

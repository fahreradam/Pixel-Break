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

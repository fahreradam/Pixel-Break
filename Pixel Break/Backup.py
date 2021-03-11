import pygame
import math


class Paddle:
    def __init__(self, win, x, y):
        self.win = win
        self.speed = 100
        self.stamina = 100
        self.position = [x, y]
        self.orientation = 180  # In degrees
        self.rotation_rate = 90  # How fast does the ship rotate (in degrees / sec)
        self.img = "images\\"

    def draw(self):
        pygame.draw.rect(self.win, (0, 100, 0), (self.position[0], self.position[1], 100, 10))
        pygame.draw.rect(self.win, (0, 255, 0), (self.position[0], self.position[1], self.stamina, 10))
        temp_surf = pygame.transform.rotate(self.img, self.orientation - 90)
        self.win.blit(temp_surf, (self.position[0], self.position[1]))

    def move(self, dt, direction):
        if keys[pygame.K_a]:
            self.position[0] -= self.speed * dt
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and self.stamina >= 1:
                    self.position[0] = self.position[0] - 50
                    self.stamina -= 10
        dist = self.speed * direction * dt
        radians = math.radians(self.orientation)
        opposite = -dist * math.sin(radians)
        adjacent = dist * math.cos(radians)
        self.position[0] += adjacent
        self.position[1] += opposite

        if keys[pygame.K_d]:
            self.position[0] += self.speed * dt
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and self.stamina >= 1:
                    self.position[0] = 50 + self.position[0]
                    self.stamina -= 10

        # Regen
        if self.stamina <= 100:
            self.stamina += 5 * dt

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

    def handle_input(self, delta_time, keys):
        if keys[pygame.K_d]:
            self.position[0] += self.speed * dt
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and self.stamina >= 1:
                    self.position[0] = 50 + self.position[0]
                    self.stamina -= 10
        if [0]:
            self.move(1, delta_time, event)

    def point_towards(self, target_pt, keys):
        if keys[pygame.K_SPACE]:
            adjacent = target_pt[0] - self.position[0]
            opposite = -(target_pt[1] - self.position[1])
            self.orientation = math.degrees(math.atan2(opposite, adjacent))

    class Player:
        """ A top-down player character sprite that can point and move in any direction """

        def __init__(self, x, y):
            self.position = [x, y]
            self.img = pygame.image.load("Image\\Spaceship_tut.png")
            self.orientation = 180  # In degrees
            self.rotation_rate = 90  # How fast does the ship rotate (in degrees / sec)
            self.move_rate = 150  # How fast does the ship move forwards (in pixels / sec)
            self.bounding_radius = 25

        def draw(self, surf):
            temp_surf = pygame.transform.rotate(self.img, self.orientation - 90)
            surf.blit(temp_surf, (self.position[0] - temp_surf.get_width() / 2,
                                  self.position[1] - temp_surf.get_height() / 2))

        def rotate(self, direction, delta_time):
            """ direction should be (0 = no rotation, -1 = clockwise, +1 = counter_clockwise)
                delta_time is the time since the last frame
            """
            self.orientation += direction * self.rotation_rate * delta_time

        def move(self, direction, delta_time):
            """ direction should be (0 = no movement, -1 = backwards, +1 = forwards)
                delta_time is the time since the last frame """
            dist = self.move_rate * direction * delta_time
            radians = math.radians(self.orientation)
            opposite = -dist * math.sin(radians)
            adjacent = dist * math.cos(radians)
            self.position[0] += adjacent
            self.position[1] += opposite

        def handle_input(self, delta_time):
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            self.point_towards(mouse_pos)
            if mouse_buttons[0]:
                self.move(1, delta_time)

        def point_towards(self, target_pt):
            adjacent = target_pt[0] - self.position[0]
            opposite = -(target_pt[1] - self.position[1])
            self.orientation = math.degrees(math.atan2(opposite, adjacent))

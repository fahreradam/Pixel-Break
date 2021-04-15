import pygame


class GameUI:
    """Game UI Manager"""

    def __init__(self, surf):
        self.win = surf
        # Screens --------------------------------------------------------------------------
        # title
        self.title_screen_img = pygame.image.load("images\\Game Title Screen.png").convert()
        # credits
        self.credits_scr = pygame.image.load("images\\Credits screen.png").convert()
        # leaderboard
        self.leaderboard_scr = pygame.image.load("images\\Leaderboard screen.png").convert()
        # buttons --------------------------------------------------------------------------
        # long
        self.button_w = 45
        self.button_h = 200
        self.button_size = [self.button_w, self.button_h]
        # short
        self.button_short_w = 45
        self.button_short_h = 140
        self.button_short_size = [self.button_short_w, self.button_short_h]
        # start
        self.start_img = pygame.image.load("images\\Button - Start.png").convert()
        self.start_img_hovered = pygame.image.load("images\\Button - Start (Hovered).png").convert()
        self.button_start = pygame.transform.scale(self.start_img, self.button_size)
        self.button_start_hovered = pygame.transform.scale(self.start_img_hovered, self.button_size)
        self.button_start_pos = [self.win.get_width() - 200 - self.button_w / 2,
                                 self.win.get_height() - 300 - self.button_h / 2]
        self.button_start_collider = pygame.Rect(self.button_start_pos, self.button_size)
        # leaderboard
        self.leaderboard_img = pygame.image.load("images\\Button - Leaderboard.png").convert()
        self.leaderboard_img_hovered = pygame.image.load("images\\Button - Leaderboard (Hovered).png").convert()
        self.button_leaderboard = pygame.transform.scale(self.leaderboard_img, self.button_size)
        self.button_leaderboard_hovered = pygame.transform.scale(self.leaderboard_img_hovered, self.button_size)
        self.button_leaderboard_pos = [self.win.get_width() - 400 - self.button_w / 2,
                                       self.win.get_height() - 300 - self.button_h / 2]
        self.button_leaderboard_collider = pygame.Rect(self.button_leaderboard_pos, self.button_size)
        # credits
        self.credits_img = pygame.image.load("images\\Button - Credits.png").convert()
        self.credits_img_hovered = pygame.image.load("images\\Button - Credits (Hovered).png").convert()
        self.button_credits = pygame.transform.scale(self.credits_img, self.button_short_size)
        self.button_credits_hovered = pygame.transform.scale(self.credits_img_hovered, self.button_short_size)
        self.button_credits_pos = [self.win.get_width() - 130 - self.button_w / 2,
                                   self.win.get_height() - 250 - self.button_h / 2]
        self.button_credits_collider = pygame.Rect(self.button_credits_pos, self.button_short_size)
        # quit
        self.quit_img = pygame.image.load("images\\Button - Exit.png").convert()
        self.quit_img_hovered = pygame.image.load("images\\Button - Exit (Hovered).png").convert()
        self.button_quit = pygame.transform.scale(self.quit_img, self.button_short_size)
        self.button_quit_hovered = pygame.transform.scale(self.quit_img_hovered, self.button_short_size)
        self.button_quit_pos = [self.win.get_width() - 470 - self.button_short_w / 2,
                                self.win.get_height() - 270 - self.button_short_h / 2]
        self.button_quit_collider = pygame.Rect(self.button_quit_pos, self.button_short_size)
        # return / back
        self.back_img = pygame.image.load("images\\Button - Back v2.png")
        self.back_img_hovered = pygame.image.load("images\\Button - Back v2 (Hovered).png")
        self.black_img = pygame.image.load("images\\black 100x100.png")
        self.button_back_pos = [20, 20]
        self.button_back_size = [30, 30]
        self.button_back = pygame.transform.scale(self.back_img, self.button_back_size)
        self.button_back_hovered = pygame.transform.scale(self.back_img_hovered, self.button_back_size)
        self.button_back_collider = pygame.Rect(self.button_back_pos, self.button_back_size)

    def draw(self):
        self.win.blit(self.title_screen_img, (0, 0))
        # start
        self.win.blit(self.button_start, self.button_start_pos)
        # leaderboard
        self.win.blit(self.button_leaderboard, self.button_leaderboard_pos)
        # credits
        self.win.blit(self.button_credits, self.button_credits_pos)
        # quit
        self.win.blit(self.button_quit, self.button_quit_pos)

    def draw_hovered(self):
        m_pos = pygame.mouse.get_pos()
        # start
        if self.button_start_collider.collidepoint(m_pos):
            self.win.blit(self.button_start_hovered, self.button_start_pos)
        # leaderboard
        elif self.button_leaderboard_collider.collidepoint(m_pos):
            self.win.blit(self.button_leaderboard_hovered, self.button_leaderboard_pos)
        # credits
        elif self.button_credits_collider.collidepoint(m_pos):
            self.win.blit(self.button_credits_hovered, self.button_credits_pos)
        # quit
        elif self.button_quit_collider.collidepoint(m_pos):
            self.win.blit(self.button_quit_hovered, self.button_quit_pos)
        else:
            self.win.fill((0, 0, 0))
            self.draw()

    def draw_return(self):
        self.win.blit(self.button_back, self.button_back_pos)

    def draw_return_hov(self):
        m_pos = pygame.mouse.get_pos()
        if self.button_back_collider.collidepoint(m_pos):
            self.win.blit(self.button_back_hovered, self.button_back_pos)
        else:
            self.win.blit(self.black_img, self.button_back_pos)
            self.win.blit(self.button_back, self.button_back_pos)

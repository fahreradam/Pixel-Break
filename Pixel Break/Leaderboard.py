import pygame


# starting pint from the top = 160
# hight of boxes = 24
# space between each box = 46

class Leaderboard:
    def __init__(self):
        self.file = "High_scores.txt"
        self.font = pygame.font.Font("font\\pixle_font\\Pixle_Font.ttf", 24)
        self.string_buff = ""
        self.typing = True

    def update(self, score, win, mode):

        event = pygame.event.poll()
        list = []
        new_score = score
        text = self.font.render("Please Type Your Name", True, (255, 255, 255))
        f = open(self.file, "r+")
        if self.typing:
            for line in f:
                list.append(line.strip())
            e = []
            for score in list:
                e.append(int(score.split(":")[1].strip()))

            t = -1
            for i in range(0, len(e)):
                if i == 13:
                    break
                if new_score > e[i]:
                    t = i
                    break
            if t != -1:
                win.blit(text, (((win.get_width() / 2) - (text.get_width() / 2)), 400))
                Shown_text = self.font.render(self.string_buff, True, (255, 255, 255))
                win.blit(Shown_text, ((win.get_width() / 2) - (Shown_text.get_width() / 2), 600))
                highschoreer = self.string_buff + ": " + str(new_score)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        list.insert(t, highschoreer)
                        self.typing = False
                    if event.key == pygame.K_BACKSPACE:
                        self.string_buff = self.string_buff[0: -1]
                    if event.key == pygame.K_SPACE:
                        self.string_buff += ""
                    elif event.key != pygame.K_SPACE and event.key != pygame.K_RETURN and event.key != pygame.K_ESCAPE \
                            and event.key != pygame.K_BACKSPACE and event.key != pygame.KMOD_SHIFT:
                        self.string_buff += pygame.key.name(event.key)
            if len(e) < 12 and t == -1:
                win.blit(text, (((win.get_width() / 2) - (text.get_width() / 2)), 400))
                Shown_text = self.font.render(self.string_buff, True, (255, 255, 255))
                win.blit(Shown_text, ((win.get_width() / 2) - (Shown_text.get_width() / 2), 600))
                highschoreer = self.string_buff + ": " + str(new_score)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        list.append(highschoreer)
                        self.typing = False
                    if event.key == pygame.K_BACKSPACE:
                        self.string_buff = self.string_buff[0: -1]
                    if event.key == pygame.K_SPACE:
                        self.string_buff += ""
                    elif event.key != pygame.K_SPACE and event.key != pygame.K_RETURN and event.key != pygame.K_ESCAPE \
                            and event.key != pygame.K_BACKSPACE and event.key != pygame.KMOD_SHIFT:
                        self.string_buff += pygame.key.name(event.key)

        if self.typing == False:
            f.close()
            f = open(self.file, "w")
            for i in list:
                f.write(i + "\n")

    def draw(self, win):
        f = open(self.file, "r")
        for r, l in zip(range(0, 11), f):
            text = self.font.render(l[:len(l) - 1], True, (0, 167, 93))
            win.blit(text, ((win.get_width() / 2) - (text.get_width() / 2), 160 + (46 * r)))

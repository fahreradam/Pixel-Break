import pygame
import paddle
import ball
import game_map
pygame.init()

win_w = 600
win_h = 800
win = pygame.display.set_mode((win_w, win_h))

clock = pygame.time.Clock()
ball = ball.Ball(400, 400, win)
paddle = paddle.Paddle(win, 400, 700)
cur_map = game_map.Map(starting_map)
done = False
while not done:
    dt = clock.tick() / 1000
    event = pygame.event.poll()
    keys = pygame.key.get_pressed()
    mPos = pygame.mouse.get_pos()
    mClick = pygame.mouse.get_pressed()

    # Drawing
    win.fill((0, 0, 0))
    paddle.draw()
    ball.draw()
    cur_map.render(game_surf, grid_color=None, debug=self.debug)

    pygame.display.flip()

    # Movement
    paddle.point_towards(mPos, keys, dt)
    paddle.handle_input(dt, keys, event)

    # Collision
    paddle.collide()

    # Exiting
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
    if event.type == pygame.QUIT:
        done = True

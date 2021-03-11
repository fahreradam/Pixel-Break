import pygame
import paddle
pygame.init()

win_w = 600
win_h = 800
win = pygame.display.set_mode((win_w, win_h))

clock = pygame.time.Clock()

paddle = paddle.Paddle(win, 400, 700)
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

    pygame.display.flip()

    # Movement
    paddle.point_towards(mPos, keys)
    paddle.handle_input(dt, keys, event)

    # Collision
    paddle.collide()

    # Exiting
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
    if event.type == pygame.QUIT:
        done = True

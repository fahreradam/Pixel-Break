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
cur_map = game_map.Map("BossMaps\\Litch.tmx")
done = False
collide_list = [ball]
while not done:
    dt = clock.tick() / 1000
    event = pygame.event.poll()
    keys = pygame.key.get_pressed()
    mPos = pygame.mouse.get_pos()
    mClick = pygame.mouse.get_pressed()

    # Movement
    paddle.point_towards(mPos, keys, dt)
    paddle.handle_input(dt, keys, event)

    # Collision
    paddle.collision(collide_list, paddle.dashing)
    paddle.pixel_collision(cur_map.bricks, ball.position[0], ball.position[1], 5, ball.direction)




    # Drawing
    win.fill((0, 0, 0))
    paddle.draw()
    ball.draw()
    ball.move(dt)
    ball.collision(paddle.position, mPos, paddle.stamina)
    cur_map.render(win, grid_color=None)

    pygame.display.flip()


    # Exiting
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
    if event.type == pygame.QUIT:
        done = True

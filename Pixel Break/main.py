import pygame
import paddle
import ball
import game_map
import Attacks
import random
pygame.init()

win_w = 600
win_h = 800
win = pygame.display.set_mode((win_w, win_h))
attk_exists = False
attk_timer = 2
attk_type = 0
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
    paddle.collide()
    if attk_exists == False:
        attk_timer -= 1 * dt
        attk_type = 0
    if attk_timer <= 0:
        attk_type = random.randint(1, 4)
        left_attk = Attacks.Attacks(attk_type, paddle.actual_stamina.get_height(), paddle.actual_stamina.get_width,
                                    600, 800, paddle.position[0])
        attk_exists = True






    # Drawing
    win.fill((0, 0, 0))
    paddle.draw()
    ball.draw()
    ball.move(dt)
    ball.collision(paddle.position, mPos, paddle.stamina)
    cur_map.render(win, grid_color=None)
    if attk_exists == True:
        left_attk.update(dt)
        if left_attk.direction != 0:

            left_attk.draw(win)

        else:
            attk_exists = False
        attk_timer = 2
    pygame.display.flip()


    # Exiting
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
    if event.type == pygame.QUIT:
        done = True

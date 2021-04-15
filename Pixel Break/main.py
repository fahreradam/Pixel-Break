import pygame
import gameui
import paddle
import ball
import game_map
import Attacks
import random
import bricks
pygame.init()

win_w = 600
win_h = 800
win = pygame.display.set_mode((win_w, win_h))
bachground = pygame.Surface((win_w, win_h))
boss_screen = pygame.Surface((win_w, win_h))
attk_exists = False
attk_timer = 2
attk_type = 0
clock = pygame.time.Clock()
game_ui = gameui.GameUI(win)
ball = ball.Ball(0, 0, win)
paddle = paddle.Paddle(win, 400, 700, ball)
cur_map = game_map.Map("BossMaps\\Litch.tmx")
background = pygame.image.load("images\\Background.png")
done = False
collide_list = [ball]
left_attk = None
# game state/mode
mode = "title"
while not done:
    dt = clock.tick() / 1000
    event = pygame.event.poll()
    keys = pygame.key.get_pressed()
    mPos = pygame.mouse.get_pos()
    mClick = pygame.mouse.get_pressed()
    health = len(cur_map.bricks)

    if mode == "game":
        # Movement
        paddle.point_towards(mPos, keys, dt)
        paddle.handle_input(dt, keys, event)
        # ball.shadow(dt, paddle.position)

        # Collision
        paddle.collision(collide_list, paddle.dashing)
        # paddle.pixel_collision(cur_map.bricks, ball.shadow_ball_pos[0], ball.shadow_ball_pos[1], 5, ball.shadow_dir)

        paddle.pixel_collision(cur_map.bricks, ball.position[0], ball.position[1], 5, ball.direction)

        paddle.collide()







    # Drawing

    win.blit(bachground, (0, 0))
    bachground.blit(background, (0, 0))
    paddle.draw()
    ball.draw()
    ball.move(dt)
    ball.collision(paddle.position, mPos, paddle.stamina)
    cur_map.render(win, grid_color=None)
    ball.power(dt)
    if attk_exists == False:

        attk_timer -= 1 * dt
        attk_type = 0
        if attk_timer <= 0:

            attk_type = random.randint(0, 10)

            left_attk = Attacks.Attacks(attk_type, paddle.position[1], paddle.actual_stamina.get_width(),
                                        600, 800, paddle.position[0], collide_list, paddle.position[1])

            collide_list.append(left_attk)

            attk_exists = True

    if attk_exists == True:

        left_attk.update(dt, win)

        if left_attk.direction != 0:

            left_attk.draw(win)
        else:
            if len(collide_list) >= 1 and left_attk.attack2 == None:
                collide_list.remove(left_attk)
                attk_exists = False
                attk_timer = 2
            if left_attk.attack3 != None:
                if left_attk.attack3.direction == 0:
                    collide_list.remove(left_attk.attack3)

                    attk_exists = False
                    attk_timer = 2
            if left_attk.attack2 != None:
                if left_attk.attack2.direction == 0:
                    collide_list.remove(left_attk.attack2)


    # title screen --
    if mode == "title":
        game_ui.draw()
        game_ui.draw_hovered()
    # menu buttons and game modes
    # start game
    if game_ui.button_start_collider.collidepoint(mPos) and mClick[0]:
        mode = "game"
    if mode == "game":
        win.fill((0, 0, 0))
        win.blit(bachground, (0, 0))
        bachground.blit(background, (0, 0))
        game_ui.draw_return()
        game_ui.draw_return_hov()
        paddle.draw()
        ball.draw()
        ball.move(dt)
        ball.collision(paddle.position, mPos, paddle.stamina)
        cur_map.render(win, grid_color=None)
        ball.power(dt, paddle.position, paddle.stamina, mClick)
        if attk_exists == False:

            attk_timer -= 1 * dt
            attk_type = 0
            if attk_timer <= 0:

                attk_type = 6


                left_attk = Attacks.Attacks(attk_type, paddle.position[1], paddle.actual_stamina.get_width(),
                                            600, 800, paddle.position[0], collide_list, paddle.position[1])

                collide_list.append(left_attk)

                attk_exists = True

        if attk_exists == True:

            left_attk.update(dt, win)

            if left_attk.direction != 0:

                left_attk.draw(win)
            else:
                if len(collide_list) >= 1 and left_attk.attack2 == None and left_attk.attack3 == None:
                    collide_list.remove(left_attk)

                    attk_exists = False
                    attk_timer = 2
                if left_attk.attack3 != None:
                    collide_list.remove(left_attk.attack3)
                if left_attk.attack2 != None:
                    if left_attk.attack2.direction == 0:
                        collide_list.remove(left_attk.attack2)

                        attk_exists = False
                        attk_timer = 2

    # quit game
    if game_ui.button_quit_collider.collidepoint(mPos) and mClick[0]:
        mode = "quit"
    if mode == "quit":
        done = True
    # credits
    if game_ui.button_credits_collider.collidepoint(mPos) and mClick[0]:
        mode = "credits"
    if mode == "credits":
        win.fill((0, 0, 0))
        win.blit(game_ui.credits_scr, (0, 0))
        game_ui.draw_return()
        game_ui.draw_return_hov()
    # leaderboard
    if game_ui.button_leaderboard_collider.collidepoint(mPos) and mClick[0]:
        mode = "leaderboard"
    if mode == "leaderboard":
        win.fill((0, 0, 0))
        win.blit(game_ui.leaderboard_scr, (0, 0))
        game_ui.draw_return()
        game_ui.draw_return_hov()
    # return to title screen / main menu
    if game_ui.button_back_collider.collidepoint(mPos) and mClick[0]:
        mode = "title"







    ball.game_win(health)

    ball.game_over()



    pygame.display.flip()

    # Exiting
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
    if event.type == pygame.QUIT:
        done = True






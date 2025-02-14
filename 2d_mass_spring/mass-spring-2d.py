"""
author: Faisal Z. Qureshi
email: faisal.qureshi@uoit.ca
website: http://www.vclab.ca
license: BSD
"""

import pygame, sys
import matplotlib.pyplot as plt
import numpy as np

# import sim_rk4 as Simulation
import sim as Simulation
import util


def main():
    # sim title
    title = 'Mass-Spring System'

    # initializing pygame
    pygame.init()

    # clock object that ensure that animation has the same
    # on all machines, regardless of the actual machine speed.
    clock = pygame.time.Clock()

    # fonts
    text = util.MyText(util.BLACK)

    # setting up a sprite group, which will be drawn on the
    # screen
    ball = util.MyRect(color=util.BLUE, width=32, height=32)
    center = util.MyRect(color=util.RED, width=4, height=4)
    x_axis = util.MyRect(color=util.BLACK, width=620, height=1)
    y_axis = util.MyRect(color=util.BLACK, width=1, height=460)
    my_group = pygame.sprite.Group([x_axis, y_axis, ball, center])

    # set up drawing canvas
    # top left corner is (0,0) top right (640,0) bottom left (0,480)
    # and bottom right is (640,480).
    win_width = 640
    win_height = 480
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption(title)

    # setting up simulation
    sim = Simulation.Simulation(title)
    # sim.init(state=np.array([200,200,0,0], dtype='float32'), mass=100., k=.01, l=200.) Try some other values
    sim.init(state=np.array([200,200,0,0], dtype='float32'), mass=10., k=10, l=200.)
    sim.set_time(0.0)
    sim.set_dt(0.1)

    print ('--------------------------------')
    print ('Usage:')
    print ('Press (r) to start/resume simulation')
    print ('Press (p) to pause simulation')
    print ('Press (q) to quit')
    print ('Press (space) to step forward simulation when paused')
    print ('Use mouse left button down to move mass around (only when simulation paused)')
    print ('--------------------------------')

    # Transformation to screen coordinates
    # Here 0,0 refers to simulation coordinates
    center.set_pos(util.to_screen(0, 0, win_width, win_height))
    x_axis.set_pos(util.to_screen(0, 0, win_width, win_height))
    y_axis.set_pos(util.to_screen(0, 0, win_width, win_height))


    while True:
        # 30 fps
        clock.tick(30)

        # update sprite x, y position using values
        # returned from the simulation
        ball.set_pos(util.to_screen(sim.state[0], sim.state[1], win_width, win_height))

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            sim.pause()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if not ball.picked:
                sim.resume()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # LEFT=1
            if sim.paused:
                if ball.rect.collidepoint(event.pos):
                    ball.picked = True
        elif event.type == pygame.MOUSEMOTION:
            if ball.picked:
                x, y = util.from_screen(event.pos[0], event.pos[1], win_width, win_height)
                sim.set_state(np.array([x, y, 0, 0], dtype='float32'))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if ball.picked:
                ball.picked = False
                sim.set_state(np.array([x, y, 0, 0], dtype='float32'))
        else:
            pass

        # clear the background, and draw the sprites
        screen.fill(util.WHITE)
        my_group.update()
        my_group.draw(screen)
        text.draw("Time = %f" % sim.cur_time, screen, (10,10))
        text.draw("x = %f" % sim.state[0], screen, (10,40))
        text.draw("y = %f" % sim.state[1], screen, (10,70))
        if ball.picked:
            text.draw("Picked. (Simulation disabled)", screen, (10,100))
        pygame.display.flip()

        # update simulation
        if not sim.paused:
            sim.step()
        elif not ball.picked and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sim.step()
        else:
            pass
    
    pygame.quit()
    sys.exit(0)

if __name__ == '__main__':
    main()
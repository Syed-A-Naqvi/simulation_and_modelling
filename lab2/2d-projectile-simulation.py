import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# clock object that ensure that animation has the same
# on all machines, regardless of the actual machine speed.
clock = pygame.time.Clock()

def load_image(name):
    image = pygame.image.load(name)
    return image

class MyCircle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, color, (width//2, height//2), min(width,height)//2)

    def update(self):
        pass

class Simulation:
    def __init__(self):
        
        self.x = 0
        self.vx = 0
        self.y = 0
        self.vy = 0
        self.mass = 1
        self.gamma = 0.0001
        self.gravity = 9.8
        self.dt = 0.033
        self.curr_time = 0
        
        self.paused = False # starting in paused mode

        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_f_params(self.gamma, self.gravity)

    def f(self, t, state, arg1, arg2):
        x, y, vx, vy = state
        gam, grav = arg1, arg2
        
        dx = vx
        dy = vy
        dvx = (-gam/self.mass)*vx
        dvy = (-gam/self.mass)*vy - grav
        
        return [dx, dy, dvx, dvy]
        
    def setup(self, speed, angle_degrees):
        
        self.vx = speed*np.cos(angle_degrees*(np.pi/180))
        self.vy = speed*np.sin(angle_degrees*(np.pi/180))
        self.solver.set_initial_value([self.x, self.y, self.vx, self.vy], self.curr_time)
    
        
        self.trace_x = [self.x]
        self.trace_y = [self.y]

    def step(self):
        self.curr_time += self.dt
        if(self.solver.successful()):
            self.solver.integrate(self.curr_time)
            self.x = self.solver.y[0]
            self.y = self.solver.y[1]
            self.vx = self.solver.y[2]
            self.vy = self.solver.y[3]
        else:
            print(f"Something went wrong during the integration at time {self.curr_time-self.dt}")

        self.trace_x.append(self.x)
        self.trace_y.append(self.y)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

def sim_to_screen(win_height, x, y):
    '''flipping y, since we want our y to increase as we move up'''
    x += 20
    y += 20

    return x, win_height - y

def main():

    # initializing pygame
    pygame.init()

    # top left corner is (0,0)
    win_width = 640
    win_height = 640
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('2D projectile motion')

    # setting up a sprite group, which will be drawn on the
    # screen
    my_sprite = MyCircle(RED, 10, 10)
    my_group = pygame.sprite.Group(my_sprite)

    print('--------------------------------')
    print('Usage:')
    print('Press (r) to start/resume simulation')
    print('Press (p) to pause simulation')
    print('Press (space) to step forward simulation when paused')
    print('Press (q) to exit simulation')
    print('--------------------------------')
    
    for angle in [15,30,45,60,75,90]:
        for speed in [50, 60, 70]:
            # setting up simulation
            sim = Simulation()
            sim.setup(speed, angle)

            while True:
                # 30 fps
                clock.tick(30)

                # update sprite x, y position using values
                # returned from the simulation
                my_sprite.rect.x, my_sprite.rect.y = sim_to_screen(win_height, sim.x, sim.y)

                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    sim.pause()
                    # print("x positions = ", sim.trace_x)
                    # print("y positions = ", sim.trace_y)
                    continue
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    sim.resume()
                    continue
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
                else:
                    pass

                # clear the background, and draw the sprites
                screen.fill(WHITE)
                my_group.update()
                my_group.draw(screen)
                pygame.display.flip()

                if sim.y < 0:
                    break

                # update simulation
                if not sim.paused:
                    sim.step()
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        sim.step()

            # plt.figure(1)
            # plt.plot(sim.trace_x, sim.trace_y)
            # plt.xlabel('x')
            # plt.ylabel('y')
            # plt.axis('equal')
            # plt.title('2D projectile trajectory')
            # plt.show()

            print(f"angle = {angle}, speed = {speed}, r = {sim.trace_x[-1]}")

    print()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
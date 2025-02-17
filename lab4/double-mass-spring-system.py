import sys
import math
import pygame
import numpy as np
from scipy.integrate import ode

# --------------------- Simulation Parameters ---------------------
WIDTH, HEIGHT = 800, 800
FPS = 60
MASS1 = 1.0
MASS2 = 10.0
K1 = 10.0
K2 = 50.0
C1 = 0.2
C2 = 0.2
REST_LENGTH1 = 10.0
REST_LENGTH2 = 10.0
GRAVITY = 9.81
DT = 0.02
SCALE = 10.0

# --------------------- Pygame Setup -----------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Mass-Spring Simulation")
clock = pygame.time.Clock()

# --------------------- Utility Function --------------------------
def screen_coords(x, y):
    screen_x = int(WIDTH / 2 + x * SCALE)
    screen_y = int(HEIGHT / 2 - y * SCALE)
    return (screen_x, screen_y)

# --------------------- Simulation Class --------------------------
class Simulation:

    def __init__(self, init_state):
        # State: [x1, y1, x2, y2, vx1, vy1, vx2, vy2]
        self.state = init_state[:]
        self.t = 0.0
        self.params = (MASS1, MASS2, K1, K2, C1, C2, REST_LENGTH1, REST_LENGTH2)
        self.solver = ode(self.f)
        self.solver.set_integrator("dop853")
        self.solver.set_initial_value(self.state, self.t)
        self.solver.set_f_params(self.params)

    def f(self, t, state, params):

        m1, m2, k1, k2, c1, c2, L1, L2 = params
        x1, y1, x2, y2, vx1, vy1, vx2, vy2 = state

        # --- Spring 1: Origin to Mass 1 ---
        dx1, dy1 = x1, y1
        r1 = math.sqrt(dx1**2 + dy1**2)  # avoid division by zero
        deform1 = r1 - L1
        # unit components in direction of spring1 forces
        ux1, uy1 = dx1 / r1, dy1 / r1 
        # Spring force and damping on mass1 from spring1:
        Fx1_spring = -k1 * deform1 * ux1
        Fy1_spring = -k1 * deform1 * uy1
        Fx1_damp = -c1 * vx1
        Fy1_damp = -c1 * vy1
        F1_origin_x = Fx1_spring + Fx1_damp
        F1_origin_y = Fy1_spring + Fy1_damp

        # --- Spring 2: Mass 1 to Mass 2 ---
        dx2 = x2 - x1
        dy2 = y2 - y1
        r2 = math.sqrt(dx2**2 + dy2**2)
        deform2 = r2 - L2
        # unit components in direction of spring2 forces
        ux2, uy2 = dx2 / r2, dy2 / r2 
        # relative velocity between mass 1 and 2
        rvx = vx2 - vx1
        rvy = vy2 - vy1
        Fx2_spring = -k2 * deform2 * ux2
        Fy2_spring = -k2 * deform2 * uy2
        Fx2_damp = -c2 * rvx
        Fy2_damp = -c2 * rvy
        F2_total_x = Fx2_spring + Fx2_damp
        F2_total_y = Fy2_spring + Fy2_damp

        # Force on mass1 from spring2 is the negative of that on mass2:
        F1_mass2_x = -F2_total_x
        F1_mass2_y = -F2_total_y

        # --- Net Forces on Mass 1 and Mass 2 ---
        Fx1_total = F1_origin_x + F1_mass2_x
        Fy1_total = F1_origin_y + F1_mass2_y
        Fx2_total = F2_total_x
        Fy2_total = F2_total_y

        # Add gravitational effects to both masses (positive-y is upwards)
        ay1_gravity = -GRAVITY
        ay2_gravity = -GRAVITY

        # Accelerations (F = m * a)
        ax1 = Fx1_total / m1
        ay1 = Fy1_total / m1 + ay1_gravity
        ax2 = Fx2_total / m2
        ay2 = Fy2_total / m2 + ay2_gravity

        return [vx1, vy1, vx2, vy2, ax1, ay1, ax2, ay2]


    def update(self, dt):
        if self.solver.successful():
            self.solver.integrate(self.solver.t + dt)
            self.state = self.solver.y
            self.t = self.solver.t

    def get_state(self):
        return self.state

# --------------------- Sprite for the Mass ------------------------
class MassSprite(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()

    def update_position(self, x, y):
        self.rect.center = screen_coords(x, y)

# --------------------- Main Function -----------------------------
def main():
    running = True
    clock = pygame.time.Clock()

    # Initial conditions for the two-mass system:
    init_state = [10.0, 10.0, 20.0, -2.0, 0.0, 0.0, 0.0, 0.0]
    sim = Simulation(init_state)

    # Create sprites for each mass
    mass1_sprite = MassSprite(color=(255, 0, 0), radius=10)
    mass2_sprite = MassSprite(color=(0, 200, 0), radius=10)
    all_sprites = pygame.sprite.Group(mass1_sprite, mass2_sprite)

    accumulator = 0.0
    while running:
    
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # calculating time in s since last frame
        dt_frame = clock.tick(FPS) / 1000.0
        # updating accumulated time, unaccounted for by sim updates
        accumulator += dt_frame
        # simulating multiple steps in case of residual time
        while accumulator >= DT:
            sim.update(DT)
            accumulator -= DT
        
        # Get the updated state
        state = sim.get_state()
        x1, y1, x2, y2, vx1, vy1, vx2, vy2 = state

        # Update sprites' positions
        mass1_sprite.update_position(x1, y1)
        mass2_sprite.update_position(x2, y2)

        # Draw background
        screen.fill("#525252")

        # Drawing Axes
        pygame.draw.line(screen, 'black', (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
        pygame.draw.line(screen, 'black', (0, HEIGHT//2), (WIDTH, HEIGHT//2), 2)

        # Origin hinge
        pygame.draw.circle(screen, (255, 255, 0), screen_coords(0, 0), 5)

        # Spring from origin to Mass 1
        pygame.draw.line(screen, "#d2d2d2", screen_coords(0, 0), screen_coords(x1, y1), 2)
        # Spring from Mass 1 to Mass 2
        pygame.draw.line(screen, "#d2d2d2", screen_coords(x1, y1), screen_coords(x2, y2), 2)

        # Draw mass sprites
        all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

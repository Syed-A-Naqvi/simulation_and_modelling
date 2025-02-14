"""
author: Faisal Qureshi
email: faisal.qureshi@uoit.ca
website: http://www.vclab.ca
license: BSD
"""

import numpy as np
from scipy.integrate import ode

class Simulation:
    def __init__(self, title):
        self.paused = True  # start in paused mode
        self.title = title
        self.cur_time = 0.0
        self.dt = 0.033    # time step in seconds (approx. 30 fps)
        self.state = None  # state will be an array: [x, y, vx, vy]
        self.mass = None   # mass of the object
        self.k = None      # spring constant
        self.l = None      # rest length of the spring
        self.ode_solver = None  # this will be our ode solver instance

    def f(self, t, st):
        
        x, y, vx, vy = st
        r = np.sqrt(x**2 + y**2)
        
        # The derivatives of position are just the velocities.
        dxdt = vx
        dydt = vy
        # Force: F = -k*(r - l) * (x/r, y/r), so acceleration = F/m.
        ax = -self.k * (r - self.l) * (x / r) / self.mass
        ay = -self.k * (r - self.l) * (y / r) / self.mass

        return [dxdt, dydt, ax, ay]

    def init(self, state, mass, k, l):
        self.state = np.array(state, dtype=np.float32)
        self.mass = mass
        self.k = k
        self.l = l
        self.cur_time = 0.0
        # Create the ODE solver object and set its initial conditions.
        self.ode_solver = ode(self.f)
        self.ode_solver.set_integrator('dop853')
        self.ode_solver.set_initial_value(self.state, self.cur_time)

    def set_state(self, state):
        self.state = np.array(state, dtype=np.float32)
        if self.ode_solver is not None:
            self.ode_solver.set_initial_value(self.state, self.cur_time)

    def set_time(self, cur_time=0.0):
        self.cur_time = cur_time
        if self.ode_solver is not None:
            self.ode_solver.set_initial_value(self.state, self.cur_time)

    def set_dt(self, dt=0.033):
        self.dt = dt

    def step(self):
        if self.ode_solver is not None and self.ode_solver.successful():
            self.ode_solver.integrate(self.cur_time + self.dt)
            self.state = self.ode_solver.y
            self.cur_time = self.ode_solver.t

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def save(self, filename):
        # Ignore this
        pass

    def load(self, filename):
        # Ignore this
        pass

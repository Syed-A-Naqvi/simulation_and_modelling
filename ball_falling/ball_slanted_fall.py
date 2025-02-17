"""
author: Faisal Qureshi
email: faisal.qureshi@ontariotechu.ca
website: http://www.vclab.ca
license: BSD
"""


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.integrate import ode


def rot(angle, v):
    # rotates vector v by some angle 
    # angle in radians
    return np.dot([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]], v)

# A little hack to set the floor at a slant of 10 degrees
floor_angle = np.deg2rad(10)
floor_normal = rot(floor_angle, np.array([0,1]))
floor_tangent = rot(floor_angle, -np.array([1,0]))
print ('floor_angle', np.rad2deg(floor_angle))
print ('floor_normal', floor_normal)

# Setup figure
fig = plt.figure(1)
ax = plt.axes(xlim=(0, 300), ylim=(-75, 110))
plt.grid()
line, = ax.plot([], [], '-')
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
frame_template = 'frame = %d'
frame_text = ax.text(0.05, 0.85, '', transform=ax.transAxes)
vx_template = 'Vx = %.1fm/s'
vx_text = ax.text(0.05, 0.80, '', transform=ax.transAxes)
vy_template = 'Vy = %.1fm/s'
vy_text = ax.text(0.05, 0.75, '', transform=ax.transAxes)
plt.title('xy location')
plt.xlabel('x')
plt.ylabel('y')

x0 = -300
y0 = x0 * np.sin(floor_angle)
x1 = 300
y1 = x1 * np.sin(floor_angle)
plt.plot([x0, x1], [y0, y1], 'g-')

# y0 + (x - x0) * (y1 - y0) / (x1 - x0) = y  

def collision_detection(x, y):
    # This function takes the current location of the
    # ball (x,y) and returns if the ball has collided
    # with the floor.  It returns the a boolean that is 
    # True if the collision has occured and False otherwise.
    # It also returns the y position of the collision.
    # Recall that the y location for the collision is 
    # different for different values of x, since the floor
    # is slanted.
    # 
    
    y_collision = y0 + (x - x0) * (y1 - y0) / (x1 - x0)
    
    if (y <= y_collision):
        return True, y_collision
    else:
        return False, y_collision

# Background for each function
def init():
    line.set_data([], [])
    time_text.set_text('')
    frame_text.set_text('')
    vx_text.set_text('')
    vy_text.set_text('')
    return line, time_text, frame_text,

# Called at each frame
def animate(i, ball):
    line.set_xdata(np.append(line.get_xdata(), ball.x))
    line.set_ydata(np.append(line.get_ydata(), ball.y))
    time_text.set_text(time_template % ball.t)
    frame_text.set_text(frame_template % i)
    vx_text.set_text(vx_template % ball.vx)
    vy_text.set_text(vy_template % ball.vy)
    
    ball.update()
    return line, time_text, frame_text, vx_text, vy_text

# Ball simulation - bouncing ball
class Ball:
    def __init__(self):
        self.y = 100
        self.x = 290
        self.vx = 0
        self.vy = 0
        self.g = -9.8
        self.dt = 0.01
        self.t = 0
        self.mass = 1
        self.friction = 0.001

        self.r = ode(self.f)
        self.r.set_integrator('dop853')
        self.r.set_initial_value([self.x, self.y, self.vx, self.vy], self.t)

    def f(self, t, y):
        # Function containing the derivatives of the state
        # variables to be used within the ODE solver.
        # Here variable y denotes the state variables.  Note that 
        # this y isn't the same as the y location of the ball!
        
        vx = y[2]
        vy = y[3]
        
        dxdt = vx
        dydt = vy
        dvxdt = (-self.friction / self.mass) * vx
        dvydt = self.g + (-self.friction / self.mass) * vy        

        return [dxdt, dydt, dvxdt, dvydt]

    def update(self):
        # Forwards the simulation by one step.
        # But in order to do so, you'll need to detect collision
        # and compute the collision response.
        #
        # TODO
        
        collision, y_ = collision_detection(self.x, self.y)
        if collision:
            print('Collision detected.')

            v = np.array([self.vx, self.vy])
            
            vn = (-np.dot(v, floor_normal)) * floor_normal
            vt = (np.dot(v, floor_tangent)) * floor_tangent
            
            v = vn + vt
            
            self.vx = v[0]
            self.vy = v[1]
            self.y = y_
            
            self.r.set_initial_value([self.x, self.y, self.vx, self.vy], self.t)

        # Call ode solver to move the simulation forward by
        # self.dt
        self.r.integrate(self.r.t + self.dt)
        
        # Copies values from the ode solver
        self.t = self.r.t
        self.x = self.r.y[0]
        self.y = self.r.y[1]
        self.vx = self.r.y[2]
        self.vy = self.r.y[3]
#        print('DBG', self.x, self.y, self.vx, self.vy, self.t)


ball = Ball()

# blit=True - only re-draw the parts that have changed.
# repeat=False - stops when frame count reaches 999
# fargs=(ball,) - a tuple that can be used to pass extra arguments to animate function
anim = animation.FuncAnimation(fig, animate, fargs=(ball,), init_func=init, frames=8000, interval=10, blit=True, repeat=False)
#plt.savefig('bouncing-ball-trace', format='png')

# Save the animation as an mp4.  For more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
# anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()#
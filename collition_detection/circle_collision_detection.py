import matplotlib.pyplot as plt
import numpy as np

def plot_circles(circle1, circle2, collision):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')

    # Draw circles
    circle1_patch = plt.Circle((circle1['x'], circle1['y']), circle1['radius'], color='red' if collision else 'green', alpha=0.5, label='Circle 1')
    circle2_patch = plt.Circle((circle2['x'], circle2['y']), circle2['radius'], color='red' if collision else 'green', alpha=0.5, label='Circle 2')

    ax.add_patch(circle1_patch)
    ax.add_patch(circle2_patch)

    # Draw center points
    ax.scatter([circle1['x'], circle2['x']], [circle1['y'], circle2['y']], color='black', marker='x', label='Centers')

    # Collision state text
    state_text = 'Collision!' if collision else 'No Collision'
    ax.set_title(state_text, fontsize=14, fontweight='bold', color='red' if collision else 'black')

    plt.legend()
    plt.grid(True)
    plt.show()

def check_circle_collision(circle1, circle2):
    dist = np.linalg.norm(np.array([np.abs((circle1['x']-circle2['x'])),np.abs(circle1['y']-circle2['y'])]))
    
    if (dist <= (circle1['radius'] + circle2['radius'])):
        return True
    else:
        return False

# Define circles for collision case
circle1_collision = {'x': 30, 'y': 50, 'radius': 20}
circle2_collision = {'x': 50, 'y': 50, 'radius': 20}
collision = check_circle_collision(circle1_collision, circle2_collision)
plot_circles(circle1_collision, circle2_collision, collision)

# Define circles for non-collision case
circle1_no_collision = {'x': 20, 'y': 50, 'radius': 15}
circle2_no_collision = {'x': 70, 'y': 50, 'radius': 15}
no_collision = check_circle_collision(circle1_no_collision, circle2_no_collision)
plot_circles(circle1_no_collision, circle2_no_collision, no_collision)
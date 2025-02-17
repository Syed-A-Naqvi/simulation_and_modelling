# Collision detection in polygons - 2D case
# Faisal Z. Qureshi
# faisal.qureshi@ontariotechu.ca
#
# Adapted from ChatGPT

import numpy as np
import matplotlib.pyplot as plt

class ConvexPolygon:
    
    def __init__(self, verticies):
        self.verticies = verticies
        self.edges = np.empty((0,2))
        self.separating_axes = np.empty((0,2))
        self.compute_edges()
        self.compute_axes()
    
    def compute_edges(self):
        vs = self.verticies
        for i in range(len(vs)):
            self.edges = np.vstack([self.edges, np.array([vs[(i+1) % len(vs)][0] - vs[(i)][0], vs[(i+1) % len(vs)][1] - vs[(i)][1]])])
        
    def compute_axes(self):
        es = self.edges
        axs = np.empty((0,2))
        
        R = np.array([[0, -1],
                      [1, 0]])
        for e in es:
            
            ax = np.linalg.matmul(R, e)
            ax = ax/np.linalg.norm(ax)
            
            colinear = False
            for a in axs:
                if(np.isclose(np.dot(ax, a) % 1, 0)):
                    colinear = True
            
            if not colinear:
                axs = np.vstack([axs, ax])
        self.separating_axes = axs
        

    def print(self):
        print(f"veticies: \n{self.verticies}")
        print(f"edges: \n{self.edges}")
        print(f"axes: \n{self.separating_axes}")


def polygons_collide(poly1, poly2):
    """Check for collision between two convex polygons using SAT."""
    
    poly1 = ConvexPolygon(poly1)
    poly2 = ConvexPolygon(poly2)
        
    axs = np.vstack([poly1.separating_axes, poly2.separating_axes])
    
    for a in axs:
        poly1_projections = np.sort(np.array([np.dot(a, v) for v in poly1.verticies]))
        poly2_projections = np.sort(np.array([np.dot(a, v) for v in poly2.verticies]))
        if not (poly1_projections[-1] > poly2_projections[0] and poly2_projections[-1] > poly1_projections[0]):
            return False
    
    return True

def plot_polygons(poly1, poly2, collision):
    """Visualize two polygons and indicate collision status."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')

    # Convert polygon arrays to lists for plotting
    poly1 = np.vstack([poly1, poly1[0]])  # Close the shape
    poly2 = np.vstack([poly2, poly2[0]])  # Close the shape

    # Draw polygons
    ax.plot(poly1[:, 0], poly1[:, 1], 'b-', linewidth=2, label="Polygon 1")
    ax.fill(poly1[:, 0], poly1[:, 1], 'blue', alpha=0.3)

    ax.plot(poly2[:, 0], poly2[:, 1], 'r-', linewidth=2, label="Polygon 2")
    ax.fill(poly2[:, 0], poly2[:, 1], 'red', alpha=0.3)
    

    # Collision state text
    state_text = "Collision!" if collision else "No Collision"
    ax.set_title(state_text, fontsize=14, fontweight="bold", color="green" if collision else "red")

    plt.legend()
    plt.grid(True)
    plt.show()

# Example polygons
polygon1 = np.array([[10, 10], [30, 10], [30, 30]]) #, [10, 30]])  # Square
polygon2 = np.array([[25, 25], [45, 25], [45, 45], [25, 45]])  # Overlapping Square
polygon3 = np.array([[50, 50], [70, 50], [70, 70], [50, 70]])  # Non-overlapping Square

# Check and plot collision case
collision1 = polygons_collide(polygon1, polygon2)
plot_polygons(polygon1, polygon2, collision1)

# Check and plot non-collision case
collision2 = polygons_collide(polygon1, polygon3)
plot_polygons(polygon1, polygon3, collision2)


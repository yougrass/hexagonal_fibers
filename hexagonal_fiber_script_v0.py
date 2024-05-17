import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

def generate_hexagonal_layer(a, radius):
    """
    Generate a hexagonal close-packed grid of points in the xy-plane,
    where each layer is itself shaped like a hexagon.
    
    Parameters:
    - a: float, distance between the centers of adjacent spheres.
    - radius: int, determines the number of hexagon layers from the center.
    
    Returns:
    - points: list of tuples, each representing the (x, y) coordinates of a sphere in the base layer.
    """
    points = []
    for i in range(-radius, radius + 1):
        for j in range(max(-radius, -i-radius), min(radius, -i+radius) + 1):
            x = a * (i + 0.5 * j)
            y = np.sqrt(3) * a / 2 * j
            points.append((x, y))
    return points


def rotate_point(point, angle):
    """
    Rotate a point around the origin by a given angle.
    
    Parameters:
    - point: tuple, the (x, y) coordinates of the point.
    - angle: float, the angle of rotation in radians.
    
    Returns:
    - rotated_point: tuple, the rotated (x, y) coordinates.
    """
    x, y = point
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    x_new = x * cos_theta - y * sin_theta
    y_new = x * sin_theta + y * cos_theta
    return (x_new, y_new)

def generate_twisted_hexagonal_fiber(a, layers, theta, radius):
    """
    Generate the coordinates for a twisted hexagonal fiber arrangement of spheres.
    
    Parameters:
    - a: float, distance between the centers of adjacent spheres.
    - layers: int, number of layers to generate.
    - theta: float, rotation angle between successive layers in radians.
    - radius: int, determines the extent of the hexagonal grid.
    
    Returns:
    - coordinates: list of tuples, each representing the (x, y, z) coordinates of a sphere.
    """
    coordinates = []
    base_layer = generate_hexagonal_layer(a, radius)
    
    for k in range(layers):
        z = k * a * np.sqrt(1)  # Adjust the z-spacing as needed
        angle = k * theta
        for point in base_layer:
            rotated_point = rotate_point(point, angle)
            coordinates.append((rotated_point[0], rotated_point[1], z))
    
    return coordinates

# Example usage
a = 3.2  # Distance between adjacent spheres
layers = 15  # Number of layers
theta = np.pi / 8 # Rotation angle in radians (30 degrees)
radius = 9  # Extent of the hexagonal grid

coords = generate_twisted_hexagonal_fiber(a, layers, theta, radius)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x_coords, y_coords, z_coords = zip(*coords)
ax.scatter(x_coords, y_coords, z_coords)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Default Fiber')

# Set the view angle to top-down
ax.view_init(elev=30, azim=0)
plt.show()


# Save coordinates to a CSV file
with open('test_coordinates.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['X', 'Y', 'Z'])  # Header row
    csvwriter.writerows(coords)
    
print(len(coords))


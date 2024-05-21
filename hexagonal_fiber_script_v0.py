import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
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

def generate_helical_hexagonal_fiber(a, layers, theta, radius, helix_radius, helix_pitch):
    """
    Generate the coordinates for a helical hexagonal fiber arrangement of spheres.
    
    Parameters:
    - a: float, distance between the centers of adjacent spheres.
    - layers: int, number of layers to generate.
    - theta: float, rotation angle between successive layers in radians.
    - radius: int, determines the extent of the hexagonal grid.
    - helix_radius: float, radius of the helical path.
    - helix_pitch: float, pitch of the helix (distance between turns along z-axis).
    
    Returns:
    - coordinates: list of tuples, each representing the (x, y, z) coordinates of a sphere.
    """
    coordinates = []
    base_layer = generate_hexagonal_layer(a, radius)
    
    for k in range(layers):
        z = k * helix_pitch  # z-spacing based on the helix pitch
        angle = k * theta
        helix_angle = k * (2 * np.pi / layers)  # angle for helical path
        helix_x = helix_radius * np.cos(helix_angle)
        helix_y = helix_radius * np.sin(helix_angle)
        for point in base_layer:
            rotated_point = rotate_point(point, angle)
            coordinates.append((rotated_point[0] + helix_x, rotated_point[1] + helix_y, z))
    
    return coordinates

# Example usage
a = 3.2  # Distance between adjacent spheres
layers = 15  # Number of layers
theta = np.pi / 20  # Rotation angle in radians (small twist)
radius = 9  # Number of hexagon layers from the center
helix_radius = 0  # Radius of the helical path
helix_pitch = 5  # Distance between turns along the z-axis

coords = generate_helical_hexagonal_fiber(a, layers, theta, radius, helix_radius, helix_pitch)

# Save coordinates to a CSV file
with open('nothelical_equalfiber.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['X', 'Y', 'Z'])  # Header row
    csvwriter.writerows(coords)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x_coords, y_coords, z_coords = zip(*coords)
# ax.scatter(x_coords, y_coords, z_coords)

# Plot with color variation using viridis colormap
colors = plt.cm.viridis(np.linspace(0, 1, layers))
for i in range(layers):
    layer_coords = coords[i * len(coords) // layers : (i + 1) * len(coords) // layers]
    x_layer, y_layer, z_layer = zip(*layer_coords)
    ax.scatter(x_layer, y_layer, z_layer, color=colors[i])


# Set the same scale for all axes
ax.set_box_aspect([np.ptp(x_coords), np.ptp(y_coords), np.ptp(z_coords)])  # Aspect ratio is 1:1:1


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Helical Equal Fiber')

# Set the view angle to top-down
ax.view_init(elev=22, azim=45)
plt.show()

print(len(coords))


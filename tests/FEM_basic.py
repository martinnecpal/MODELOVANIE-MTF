import numpy as np
import matplotlib.pyplot as plt

# Material properties (simplified nonlinear elastic model)
E = 210e3  # Young's modulus (MPa)
nu = 0.3   # Poisson's ratio
C1 = E / (2 * (1 + nu))  # Shear modulus

# Geometry and mesh
nodes = np.array([
    [0, 0],  # Node 1
    [1, 0],  # Node 2
    [1, 1],  # Node 3
    [0, 1],  # Node 4
    [2, 0],  # Node 5
    [2, 1],  # Node 6
])

elements = np.array([
    [0, 1, 2, 3],  # Element 1 (nodes 1, 2, 3, 4)
    [1, 4, 5, 2],  # Element 2 (nodes 2, 5, 6, 3)
])

# Applied displacement (large deformation)
applied_disp = 0.5  # Applied displacement in x-direction at node 5

# Boundary conditions (fixed at nodes 0 and 3)
fixed_nodes = [0, 3]

# Initialize displacements
num_nodes = len(nodes)
disp = np.zeros((num_nodes, 2))  # Displacement vector [u_x, u_y]

# Apply displacement at node 5
disp[4, 0] = applied_disp

# Compute deformed coordinates
deformed_nodes = nodes + disp

# Plot original and deformed mesh
def plot_mesh(nodes, elements, deformed_nodes=None):
    plt.figure(figsize=(10, 5))
    for element in elements:
        x = nodes[element, 0]
        y = nodes[element, 1]
        plt.fill(x, y, edgecolor='black', fill=False, label='Original')
        if deformed_nodes is not None:
            x_def = deformed_nodes[element, 0]
            y_def = deformed_nodes[element, 1]
            plt.fill(x_def, y_def, edgecolor='red', fill=False, label='Deformed')
    plt.legend()
    plt.title("Original and Deformed Mesh")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

# Plot the mesh
plot_mesh(nodes, elements, deformed_nodes)

# Stress calculation (simplified)
def compute_stress(disp, nodes, elements):
    stresses = []
    for element in elements:
        # Element nodes
        n1, n2, n3, n4 = element
        # Displacements at nodes
        u1 = disp[n1]
        u2 = disp[n2]
        u3 = disp[n3]
        u4 = disp[n4]
        # Strain calculation (simplified)
        strain_x = (u2[0] - u1[0]) / (nodes[n2, 0] - nodes[n1, 0])
        strain_y = (u4[1] - u1[1]) / (nodes[n4, 1] - nodes[n1, 1])
        # Stress calculation (simplified)
        stress_x = E * strain_x
        stress_y = E * strain_y
        stresses.append([stress_x, stress_y])
    return np.array(stresses)

# Compute stresses
stresses = compute_stress(disp, nodes, elements)
print("Stresses in each element:")
print(stresses)
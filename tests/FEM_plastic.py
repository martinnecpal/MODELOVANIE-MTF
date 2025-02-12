import numpy as np
import matplotlib.pyplot as plt

# Johnson-Cook material parameters
A = 200e6  # Yield stress (Pa)
B = 500e6  # Hardening modulus (Pa)
C = 0.01   # Strain rate dependency coefficient
n = 0.5    # Hardening exponent
m = 1.0    # Thermal softening exponent
eps0_dot = 1.0  # Reference strain rate (1/s)
Tm = 1000.0     # Melting temperature (K)
T0 = 300.0      # Room temperature (K)

# Elastic properties
E = 210e9  # Young's modulus (Pa)
nu = 0.3   # Poisson's ratio
G = E / (2 * (1 + nu))  # Shear modulus
K = E / (3 * (1 - 2 * nu))  # Bulk modulus

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

# Johnson-Cook stress calculation
def johnson_cook_stress(eps_p, eps_dot, T):
    T_star = (T - T0) / (Tm - T0) if Tm != T0 else 0
    return (A + B * eps_p**n) * (1 + C * np.log(eps_dot / eps0_dot)) * (1 - T_star**m)

# Plasticity algorithm
def compute_plastic_strain(eps_p_prev, eps_dot, T, stress, strain):
    # Trial stress
    stress_trial = E * strain
    # Yield condition
    yield_stress = johnson_cook_stress(eps_p_prev, eps_dot, T)
    if np.abs(stress_trial) <= yield_stress:
        return eps_p_prev, stress_trial  # Elastic deformation
    else:
        # Plastic deformation
        delta_eps_p = (np.abs(stress_trial) - yield_stress) / (E + (B * n * eps_p_prev**(n - 1)))
        eps_p = eps_p_prev + delta_eps_p
        stress = np.sign(stress_trial) * yield_stress
        return eps_p, stress

# Stress calculation for each element
def compute_stress(disp, nodes, elements):
    stresses = []
    plastic_strains = np.zeros(len(elements))  # Initialize plastic strains
    for i, element in enumerate(elements):
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
        strain = np.sqrt(strain_x**2 + strain_y**2)
        # Plastic strain and stress update
        eps_dot = 1.0  # Constant strain rate for simplicity
        T = T0  # Constant temperature for simplicity
        plastic_strains[i], stress = compute_plastic_strain(plastic_strains[i], eps_dot, T, 0, strain)
        stresses.append(stress)
    return np.array(stresses)

# Compute stresses
stresses = compute_stress(disp, nodes, elements)
print("Stresses in each element:")
print(stresses)

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
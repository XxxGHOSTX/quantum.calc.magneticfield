"""
Generalized Motion and Fluid Dynamics Integration
Combines electromagnetic forces, fluid dynamics, and quantum effects
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import List, Tuple, Callable


@dataclass
class PhysicalParameters:
    """Physical parameters for generalized motion."""
    mass: float = 1.0  # kg
    charge: float = 1.602e-19  # C (elementary charge)
    beta: float = 0.1  # Drag coefficient (N·s²/m²)
    gamma: float = 0.05  # Damping coefficient (N·s/m)
    
    # Electromagnetic parameters
    electric_field: np.ndarray = None
    magnetic_field: np.ndarray = None
    
    # Fluid parameters
    fluid_density: float = 1.225  # kg/m³ (air at sea level)
    viscosity: float = 1.81e-5  # Pa·s (air)


class GeneralizedMotionEquation:
    """
    Implementation of the generalized motion equation:
    
    F_net = m·a = Σ F_i - βv² - γ(dv/dt)
    
    Where:
    - F_net: Net force (N)
    - m: Mass (kg)
    - a: Acceleration (m/s²)
    - F_i: Individual forces
    - β: Drag coefficient
    - v: Velocity (m/s)
    - γ: Damping coefficient
    """
    
    def __init__(self, params: PhysicalParameters):
        """Initialize with physical parameters."""
        self.params = params
    
    def compute_lorentz_force(self, position, velocity, time):
        """
        Calculate Lorentz force: F = q(E + v × B)
        
        Args:
            position: Position vector (m)
            velocity: Velocity vector (m/s)
            time: Time (s)
        
        Returns:
            Lorentz force vector (N)
        """
        if self.params.electric_field is None:
            E = np.zeros(3)
        else:
            E = self.params.electric_field
        
        if self.params.magnetic_field is None:
            B = np.zeros(3)
        else:
            B = self.params.magnetic_field
        
        # F = q(E + v × B)
        lorentz = self.params.charge * (E + np.cross(velocity, B))
        return lorentz
    
    def compute_drag_force(self, velocity):
        """
        Calculate drag force: F_drag = -β|v|v
        
        Args:
            velocity: Velocity vector (m/s)
        
        Returns:
            Drag force vector (N)
        """
        v_magnitude = np.linalg.norm(velocity)
        if v_magnitude > 1e-10:
            drag = -self.params.beta * v_magnitude * velocity
        else:
            drag = np.zeros_like(velocity)
        return drag
    
    def compute_damping_force(self, acceleration):
        """
        Calculate damping force: F_damp = -γ(dv/dt)
        
        Args:
            acceleration: Acceleration vector (m/s²)
        
        Returns:
            Damping force vector (N)
        """
        return -self.params.gamma * acceleration
    
    def compute_net_force(self, position, velocity, time, external_forces=None):
        """
        Calculate net force on particle.
        
        Args:
            position: Position vector
            velocity: Velocity vector
            time: Time
            external_forces: List of additional force functions
        
        Returns:
            Net force vector
        """
        # Lorentz force
        F_lorentz = self.compute_lorentz_force(position, velocity, time)
        
        # Drag force
        F_drag = self.compute_drag_force(velocity)
        
        # External forces
        F_external = np.zeros(3)
        if external_forces is not None:
            for force_func in external_forces:
                F_external += force_func(position, velocity, time)
        
        # Total force (damping handled separately in equations of motion)
        F_net = F_lorentz + F_drag + F_external
        
        return F_net
    
    def equations_of_motion(self, state, time, external_forces=None):
        """
        Differential equations for particle motion.
        
        Args:
            state: [x, y, z, vx, vy, vz]
            time: Current time
            external_forces: List of force functions
        
        Returns:
            Derivatives [vx, vy, vz, ax, ay, az]
        """
        position = state[:3]
        velocity = state[3:]
        
        # Calculate net force
        F_net = self.compute_net_force(position, velocity, time, external_forces)
        
        # Calculate acceleration without damping
        a_nodamp = F_net / self.params.mass
        
        # Account for damping: m·a = F_net - γ·a
        # Solving: a = F_net / (m + γ)
        effective_mass = self.params.mass + self.params.gamma
        acceleration = a_nodamp * self.params.mass / effective_mass
        
        # Return derivatives
        derivatives = np.concatenate([velocity, acceleration])
        return derivatives
    
    def solve_trajectory(self, initial_position, initial_velocity, 
                        time_span, num_points=1000, external_forces=None):
        """
        Solve particle trajectory over time.
        
        Args:
            initial_position: Initial position [x, y, z]
            initial_velocity: Initial velocity [vx, vy, vz]
            time_span: (t_start, t_end)
            num_points: Number of time points
            external_forces: List of force functions
        
        Returns:
            times, positions, velocities
        """
        # Initial state
        initial_state = np.concatenate([initial_position, initial_velocity])
        
        # Time array
        times = np.linspace(time_span[0], time_span[1], num_points)
        
        # Solve ODE
        solution = odeint(self.equations_of_motion, initial_state, times, 
                         args=(external_forces,))
        
        positions = solution[:, :3]
        velocities = solution[:, 3:]
        
        return times, positions, velocities


class AdaptiveBasisElectromagnetic:
    """
    Implementation of Equation 1:
    F(t) = q[E(r,t) + v(t)×B(r,t)] + ∇·σ(r,t) + Σ aₙ(t)φₙ(r;λ) + ∮ A·dl
    """
    
    def __init__(self, charge, num_basis_functions=10):
        """
        Initialize electromagnetic force calculator.
        
        Args:
            charge: Particle charge (C)
            num_basis_functions: Number of basis functions in expansion
        """
        self.charge = charge
        self.num_basis = num_basis_functions
        self.basis_coefficients = np.zeros(num_basis_functions)
        self.lambda_params = np.ones(num_basis_functions)
    
    def basis_function(self, n, position, lambda_param):
        """
        Basis function φₙ(r; λ).
        Using spherical harmonics or localized Gaussians.
        
        Args:
            n: Basis function index
            position: Position vector
            lambda_param: Localization parameter
        
        Returns:
            Basis function value
        """
        r = np.linalg.norm(position)
        if r < 1e-10:
            return 0.0
        
        # Gaussian basis with different widths
        width = lambda_param * (n + 1)
        return np.exp(-r**2 / (2 * width**2)) * (r ** n)
    
    def compute_series_expansion(self, position, time):
        """
        Calculate Σ aₙ(t)φₙ(r;λ)
        
        Args:
            position: Position vector
            time: Time
        
        Returns:
            Force contribution from series expansion
        """
        force = np.zeros(3)
        
        for n in range(self.num_basis):
            # Time-dependent coefficient
            a_n = self.basis_coefficients[n] * np.cos(2 * np.pi * (n+1) * time)
            
            # Basis function
            phi_n = self.basis_function(n, position, self.lambda_params[n])
            
            # Gradient of basis function (numerical approximation)
            epsilon = 1e-6
            grad_phi = np.zeros(3)
            for i in range(3):
                pos_plus = position.copy()
                pos_plus[i] += epsilon
                phi_plus = self.basis_function(n, pos_plus, self.lambda_params[n])
                grad_phi[i] = (phi_plus - phi_n) / epsilon
            
            force += a_n * grad_phi
        
        return force
    
    def compute_stress_tensor_divergence(self, E_field, B_field, position):
        """
        Calculate ∇·σ(r,t) - electromagnetic stress tensor divergence.
        
        σ = ε₀(EE - ½|E|²I) + (1/μ₀)(BB - ½|B|²I)
        
        Args:
            E_field: Electric field at position
            B_field: Magnetic field at position
            position: Position vector
        
        Returns:
            Force from stress tensor divergence
        """
        epsilon_0 = 8.854187817e-12  # F/m
        mu_0 = 4 * np.pi * 1e-7  # H/m
        
        # Simplified: assume uniform fields for now
        # Full implementation would require field gradients
        E_mag_sq = np.dot(E_field, E_field)
        B_mag_sq = np.dot(B_field, B_field)
        
        # Approximate force (would need actual derivatives in full implementation)
        force = epsilon_0 * E_mag_sq * position / np.linalg.norm(position + 1e-10)**2
        
        return force
    
    def compute_total_force(self, position, velocity, E_field, B_field, time):
        """
        Calculate total electromagnetic force.
        
        Args:
            position: Position vector
            velocity: Velocity vector
            E_field: Electric field
            B_field: Magnetic field
            time: Time
        
        Returns:
            Total force vector
        """
        # Lorentz force
        F_lorentz = self.charge * (E_field + np.cross(velocity, B_field))
        
        # Stress tensor contribution
        F_stress = self.compute_stress_tensor_divergence(E_field, B_field, position)
        
        # Series expansion
        F_series = self.compute_series_expansion(position, time)
        
        # Vector potential line integral (simplified)
        # Full implementation would integrate around a closed path
        F_potential = np.zeros(3)  # Placeholder
        
        return F_lorentz + F_stress + F_series + F_potential


def demonstrate_generalized_motion():
    """Demonstrate generalized motion equations."""
    print("=" * 70)
    print("Generalized Motion and Fluid Dynamics Demonstration")
    print("=" * 70)
    
    # Set up physical parameters
    params = PhysicalParameters(
        mass=1e-10,  # Small particle (kg)
        charge=1.602e-19,  # Elementary charge
        beta=1e-8,  # Drag coefficient
        gamma=1e-9,  # Damping coefficient
    )
    
    # Set electromagnetic fields
    params.electric_field = np.array([1000.0, 0.0, 0.0])  # V/m
    params.magnetic_field = np.array([0.0, 0.0, 0.01])  # T
    
    # Create motion calculator
    motion = GeneralizedMotionEquation(params)
    
    # Initial conditions
    initial_pos = np.array([0.0, 0.0, 0.0])
    initial_vel = np.array([100.0, 0.0, 0.0])
    
    # Solve trajectory
    print("\nSolving particle trajectory...")
    times, positions, velocities = motion.solve_trajectory(
        initial_pos, initial_vel,
        time_span=(0, 1e-6),
        num_points=500
    )
    
    # Calculate energies
    kinetic_energy = 0.5 * params.mass * np.sum(velocities**2, axis=1)
    
    print(f"\nInitial kinetic energy: {kinetic_energy[0]:.6e} J")
    print(f"Final kinetic energy: {kinetic_energy[-1]:.6e} J")
    print(f"Energy dissipated: {(kinetic_energy[0] - kinetic_energy[-1]):.6e} J")
    
    # Visualize trajectory
    fig = plt.figure(figsize=(14, 10))
    
    # 3D trajectory
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', linewidth=2)
    ax1.scatter([initial_pos[0]], [initial_pos[1]], [initial_pos[2]], 
               c='g', s=100, marker='o', label='Start')
    ax1.scatter([positions[-1, 0]], [positions[-1, 1]], [positions[-1, 2]], 
               c='r', s=100, marker='x', label='End')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.set_title('3D Particle Trajectory')
    ax1.legend()
    
    # Velocity components
    ax2 = fig.add_subplot(222)
    ax2.plot(times * 1e6, velocities[:, 0], 'r-', label='vx', linewidth=2)
    ax2.plot(times * 1e6, velocities[:, 1], 'g-', label='vy', linewidth=2)
    ax2.plot(times * 1e6, velocities[:, 2], 'b-', label='vz', linewidth=2)
    ax2.set_xlabel('Time (μs)')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.set_title('Velocity Components')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Kinetic energy
    ax3 = fig.add_subplot(223)
    ax3.plot(times * 1e6, kinetic_energy, 'purple', linewidth=2)
    ax3.set_xlabel('Time (μs)')
    ax3.set_ylabel('Kinetic Energy (J)')
    ax3.set_title('Energy Dissipation')
    ax3.grid(True, alpha=0.3)
    
    # Speed
    ax4 = fig.add_subplot(224)
    speed = np.linalg.norm(velocities, axis=1)
    ax4.plot(times * 1e6, speed, 'orange', linewidth=2)
    ax4.set_xlabel('Time (μs)')
    ax4.set_ylabel('Speed (m/s)')
    ax4.set_title('Particle Speed')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('generalized_motion_trajectory.png', dpi=150, bbox_inches='tight')
    print("\nTrajectory visualization saved as 'generalized_motion_trajectory.png'")
    plt.close()
    
    # Demonstrate adaptive basis electromagnetic force
    print("\n" + "-" * 70)
    print("Adaptive Basis Electromagnetic Force Calculation")
    print("-" * 70)
    
    em_force = AdaptiveBasisElectromagnetic(charge=params.charge, num_basis_functions=5)
    em_force.basis_coefficients = np.array([1.0, 0.5, 0.25, 0.1, 0.05])
    em_force.lambda_params = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    
    test_position = np.array([1.0, 0.5, 0.0])
    test_velocity = np.array([10.0, 5.0, 0.0])
    test_time = 0.0
    
    F_total = em_force.compute_total_force(
        test_position, test_velocity,
        params.electric_field, params.magnetic_field,
        test_time
    )
    
    print(f"\nTest position: {test_position}")
    print(f"Test velocity: {test_velocity}")
    print(f"Total electromagnetic force: {F_total}")
    print(f"Force magnitude: {np.linalg.norm(F_total):.6e} N")
    
    print("\n" + "=" * 70)
    print("Demonstration Complete")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_generalized_motion()

"""
Mandelbrot Fractal Set Generator with Quantum Integration

Copyright (c) 2026 Tony Ray Macier III
Licensed under the MIT License - see LICENSE file for details

Author: Tony Ray Macier III
GitHub: @XxxGHOSTX
Project: Quantum Magnetic Field Calculator with Mandelbrot Fractal Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd


class MandelbrotSet:
    """
    Advanced Mandelbrot Set calculator with quantum and fractal applications.
    """

    def __init__(self, width=800, height=600, max_iter=256):
        """
        Initialize the Mandelbrot set calculator.

        Args:
            width: Image width in pixels
            height: Image height in pixels
            max_iter: Maximum number of iterations
        """
        self.width = width
        self.height = height
        self.max_iter = max_iter

    def mandelbrot_iteration(self, c, max_iter=None):
        """
        Calculate the number of iterations for a complex number c.

        Args:
            c: Complex number
            max_iter: Maximum iterations (uses self.max_iter if None)

        Returns:
            Number of iterations before divergence
        """
        if max_iter is None:
            max_iter = self.max_iter

        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter

    def generate_mandelbrot(self, xmin=-2.5, xmax=1.0, ymin=-1.25, ymax=1.25):
        """
        Generate the Mandelbrot set for a given region.

        Args:
            xmin, xmax: Real axis bounds
            ymin, ymax: Imaginary axis bounds

        Returns:
            2D array of iteration counts
        """
        x = np.linspace(xmin, xmax, self.width)
        y = np.linspace(ymin, ymax, self.height)
        mandelbrot_set = np.zeros((self.height, self.width))

        for i in range(self.height):
            for j in range(self.width):
                c = complex(x[j], y[i])
                mandelbrot_set[i, j] = self.mandelbrot_iteration(c)

        return mandelbrot_set

    def fractal_dimension(self, data):
        """
        Calculate the fractal dimension using box-counting method.

        Args:
            data: 2D array of Mandelbrot set

        Returns:
            Fractal dimension D
        """
        # Box-counting algorithm
        threshold = data < self.max_iter
        scales = np.logspace(0.1, 3, num=20, dtype=int)
        counts = []

        for scale in scales:
            if scale >= min(data.shape):
                break
            boxes = 0
            for i in range(0, data.shape[0], scale):
                for j in range(0, data.shape[1], scale):
                    if np.any(threshold[i:i+scale, j:j+scale]):
                        boxes += 1
            counts.append(boxes)

        # Calculate dimension from log-log plot
        valid_scales = scales[:len(counts)]
        if len(valid_scales) > 2:
            coeffs = np.polyfit(np.log(valid_scales), np.log(counts), 1)
            return -coeffs[0]
        return 1.0

    def quantum_coupling_strength(self, fractal_dim, mass_set=1e10, mass_universe=1e53):
        """
        Calculate quantum coupling strength in multiverse scenario.

        Equation: α_QCS = (ℏc/e²)(1 + M_set/M_universe)

        Args:
            fractal_dim: Fractal dimension from Mandelbrot set
            mass_set: Mass scale associated with Mandelbrot set
            mass_universe: Mass of the universe

        Returns:
            Quantum coupling strength
        """
        hbar = 1.054571817e-34  # Reduced Planck constant (J·s)
        c = 299792458  # Speed of light (m/s)
        e = 1.602176634e-19  # Elementary charge (C)

        alpha_base = (hbar * c) / (e ** 2)
        mass_ratio = mass_set / mass_universe
        alpha_qcs = alpha_base * (1 + fractal_dim * mass_ratio)

        return alpha_qcs

    def quantum_entanglement_strength(self, r, fractal_dim, mass_set=1e10, mass_universe=1e53):
        """
        Calculate quantum entanglement strength in multiverse.

        Equation: E_QES = (ℏc/r²)(1 + M_set/M_universe)

        Args:
            r: Separation between entangled particles (m)
            fractal_dim: Fractal dimension
            mass_set: Mass scale associated with Mandelbrot set
            mass_universe: Mass of the universe

        Returns:
            Quantum entanglement strength
        """
        hbar = 1.054571817e-34
        c = 299792458

        if r <= 0:
            r = 1e-10  # Avoid division by zero

        e_qes = (hbar * c / (r ** 2)) * (1 + fractal_dim * (mass_set / mass_universe))
        return e_qes

    def dark_matter_detection_probability(self, sigma_detect, sigma_total, delta, delta_max):
        """
        Calculate localized dark matter detection probability.

        Equation: P_detect = (σ_detect/σ_total)(1 + δ/δ_max)

        Args:
            sigma_detect: Detection cross-section
            sigma_total: Total interaction cross-section
            delta: Environmental factor
            delta_max: Maximum allowable environmental threshold

        Returns:
            Detection probability
        """
        if sigma_total == 0 or delta_max == 0:
            return 0

        p_detect = (sigma_detect / sigma_total) * (1 + delta / delta_max)
        return min(p_detect, 1.0)  # Probability cannot exceed 1

    def visualize_mandelbrot(self, data, save_path='mandelbrot_fractal.png'):
        """
        Visualize the Mandelbrot set with custom colormap.

        Args:
            data: 2D array of iteration counts
            save_path: Path to save the image
        """
        # Create custom colormap
        colors = ['#000033', '#000055', '#0E4C92', '#2E8BC0', '#19D3F3',
                  '#FFF33D', '#F39C12', '#E74C3C', '#000000']
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('mandelbrot', colors, N=n_bins)

        plt.figure(figsize=(12, 9))
        plt.imshow(data, extent=[-2.5, 1.0, -1.25, 1.25],
                   cmap=cmap, interpolation='bilinear', origin='lower')
        plt.colorbar(label='Iterations to divergence')
        plt.title('Mandelbrot Set Fractal Visualization', fontsize=16, fontweight='bold')
        plt.xlabel('Real Axis')
        plt.ylabel('Imaginary Axis')
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Mandelbrot visualization saved to {save_path}")
        plt.close()


def integrate_mandelbrot_xpoint(by_values, bz_values, theta_values, mandelbrot_set):
    """
    Integrate Mandelbrot fractal properties with magnetic x-point calculations.

    Args:
        by_values: By magnetic field components
        bz_values: Bz magnetic field components
        theta_values: Angle values
        mandelbrot_set: Instance of MandelbrotSet class

    Returns:
        DataFrame with integrated results
    """
    results = []

    # Generate Mandelbrot data
    fractal_data = mandelbrot_set.generate_mandelbrot()
    fractal_dim = mandelbrot_set.fractal_dimension(fractal_data)

    for i, (by, bz, theta) in enumerate(zip(by_values, bz_values, theta_values)):
        # Calculate x-point coordinate
        x_coord = np.sqrt(by**2 / (bz**2 + 1)) * np.cos(theta)

        # Map to complex plane point in Mandelbrot set
        c_real = (x_coord + 2.5) / 3.5 * 2.5 - 2.5  # Normalize to Mandelbrot range
        c_imag = theta / (2 * np.pi) * 2.5 - 1.25

        # Calculate Mandelbrot iterations for this point
        c = complex(c_real, c_imag)
        iterations = mandelbrot_set.mandelbrot_iteration(c)

        # Calculate quantum coupling strength
        coupling = mandelbrot_set.quantum_coupling_strength(fractal_dim)

        # Calculate entanglement strength (using x_coord as separation)
        entanglement = mandelbrot_set.quantum_entanglement_strength(
            abs(x_coord) if x_coord != 0 else 1e-10, fractal_dim
        )

        results.append({
            'data_point': i + 1,
            'By': by,
            'Bz': bz,
            'theta': theta,
            'x_coordinate': x_coord,
            'mandelbrot_iterations': iterations,
            'fractal_dimension': fractal_dim,
            'quantum_coupling': coupling,
            'entanglement_strength': entanglement
        })

    return pd.DataFrame(results)


def main():
    """
    Main function to demonstrate Mandelbrot set generation and analysis.
    """
    print("=" * 60)
    print("Mandelbrot Fractal Set - Quantum Integration")
    print("=" * 60)

    # Initialize Mandelbrot set
    mandelbrot = MandelbrotSet(width=1200, height=900, max_iter=256)

    # Generate Mandelbrot set
    print("\nGenerating Mandelbrot set...")
    fractal_data = mandelbrot.generate_mandelbrot()

    # Calculate fractal dimension
    print("Calculating fractal dimension...")
    fractal_dim = mandelbrot.fractal_dimension(fractal_data)
    print(f"Fractal Dimension: {fractal_dim:.4f}")

    # Visualize
    print("\nCreating visualization...")
    mandelbrot.visualize_mandelbrot(fractal_data)

    # Calculate quantum properties
    print("\nCalculating quantum properties...")
    coupling = mandelbrot.quantum_coupling_strength(fractal_dim)
    entanglement = mandelbrot.quantum_entanglement_strength(1e-9, fractal_dim)

    print(f"Quantum Coupling Strength: {coupling:.6e}")
    print(f"Quantum Entanglement Strength: {entanglement:.6e}")

    # Dark matter detection example
    print("\nDark Matter Detection Probability:")
    p_detect = mandelbrot.dark_matter_detection_probability(
        sigma_detect=1e-45,
        sigma_total=1e-40,
        delta=0.5,
        delta_max=1.0
    )
    print(f"Detection Probability: {p_detect:.6f}")

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

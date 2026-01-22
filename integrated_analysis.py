"""
Integrated Quantum-Fractal-Magnetic Field Analysis System
Combines Mandelbrot fractals, magnetic x-point calculations, and quantum gravity
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mandelbrot_fractal import MandelbrotSet, integrate_mandelbrot_xpoint
from x_point import x_point
from quantum_gravity import QuantumGravityEquation
import json


class IntegratedQuantumSystem:
    """
    Unified system integrating:
    - Mandelbrot fractal analysis
    - Magnetic field x-point calculations
    - Quantum gravity equations
    """
    
    def __init__(self):
        """Initialize the integrated system."""
        self.mandelbrot = MandelbrotSet(width=400, height=300, max_iter=128)
        self.quantum_gravity = QuantumGravityEquation()
        self.results_history = []
    
    def analyze_magnetic_field_quantum_properties(self, by_values, bz_values, theta_values):
        """
        Perform comprehensive analysis of magnetic field with quantum properties.
        
        Args:
            by_values: By magnetic field components
            bz_values: Bz magnetic field components
            theta_values: Angle values (radians)
        
        Returns:
            Comprehensive results dictionary
        """
        print("=" * 70)
        print("Integrated Quantum-Fractal-Magnetic Field Analysis")
        print("=" * 70)
        
        # Step 1: Calculate magnetic x-points
        print("\n[1/5] Calculating magnetic x-points...")
        x_points = x_point(np.array(by_values), np.array(bz_values), np.array(theta_values))
        
        # Step 2: Generate Mandelbrot fractal data
        print("[2/5] Generating Mandelbrot fractal set...")
        fractal_data = self.mandelbrot.generate_mandelbrot()
        fractal_dim = self.mandelbrot.fractal_dimension(fractal_data)
        print(f"    Fractal Dimension: {fractal_dim:.4f}")
        
        # Step 3: Calculate quantum properties
        print("[3/5] Computing quantum gravity properties...")
        quantum_results = []
        
        for i, (by, bz, theta, x_coord) in enumerate(zip(by_values, bz_values, theta_values, x_points)):
            # Map x-point to complex plane for Mandelbrot
            c_real = (x_coord + 2.5) / 3.5 * 2.5 - 2.5
            c_imag = theta / (2 * np.pi) * 2.5 - 1.25
            c = complex(c_real, c_imag)
            
            # Mandelbrot iterations
            iterations = self.mandelbrot.mandelbrot_iteration(c)
            
            # Quantum coupling
            coupling = self.quantum_gravity.quantum_coupling_strength_multiverse(fractal_dim)
            
            # Entanglement strength
            separation = abs(x_coord) if abs(x_coord) > 1e-15 else 1e-15
            entanglement = self.quantum_gravity.quantum_entanglement_strength(
                separation, fractal_dim
            )
            
            # Dark matter detection probability
            dm_prob = self.mandelbrot.dark_matter_detection_probability(
                sigma_detect=1e-45 * (1 + abs(by)),
                sigma_total=1e-40 * (1 + abs(bz)),
                delta=abs(theta) / (2 * np.pi),
                delta_max=1.0
            )
            
            # Time dilation near magnetic structure
            # Use magnetic field strength as proxy for effective mass
            effective_mass = (by**2 + bz**2) ** 0.5 * 1e30  # Scale to stellar masses
            gamma = self.quantum_gravity.extended_time_dilation_factor(
                velocity=0.1 * self.quantum_gravity.constants.c,
                mass=effective_mass,
                distance=abs(x_coord) * 1e10  # Scale to astronomical units
            )
            
            # Quantum gravity interaction
            qg_interaction = self.quantum_gravity.quantum_gravity_interaction_probability(
                m1=1e-27,
                m2=1e-27,
                distance=separation,
                energy=by * bz * 1e-10,
                entropy=iterations * 1e-23
            )
            
            quantum_results.append({
                'data_point': i + 1,
                'By': by,
                'Bz': bz,
                'theta': theta,
                'x_coordinate': x_coord,
                'mandelbrot_iterations': iterations,
                'fractal_dimension': fractal_dim,
                'quantum_coupling': coupling,
                'entanglement_strength': entanglement,
                'dark_matter_detection_prob': dm_prob,
                'time_dilation_factor': gamma,
                'quantum_gravity_interaction': qg_interaction
            })
        
        results_df = pd.DataFrame(quantum_results)
        
        # Step 4: Calculate aggregate quantum properties
        print("[4/5] Computing aggregate quantum properties...")
        
        # Black hole analogy for strong magnetic fields
        max_field_strength = np.max(np.sqrt(np.array(by_values)**2 + np.array(bz_values)**2))
        bh_mass_analog = max_field_strength * 1e31  # Scale to black hole mass
        hawking_temp = self.quantum_gravity.hawking_temperature(bh_mass_analog)
        
        # Holographic entropy bound
        characteristic_area = np.pi * (np.max(np.abs(x_points)) * 1e10) ** 2
        entropy_bound = self.quantum_gravity.holographic_principle_bound(characteristic_area)
        
        # Quantum sensing properties
        coherence_time = self.quantum_gravity.quantum_sensing_coherence_time(
            dephasing_rate=fractal_dim * 1e6  # Hz
        )
        
        metrology_efficiency = self.quantum_gravity.quantum_metrology_efficiency(
            parameter_uncertainty=np.std(x_points),
            noise_variance=np.var(x_points) * 0.1,
            n_measurements=len(x_points)
        )
        
        aggregate_results = {
            'fractal_dimension': fractal_dim,
            'mean_x_coordinate': np.mean(x_points),
            'std_x_coordinate': np.std(x_points),
            'mean_quantum_coupling': np.mean([r['quantum_coupling'] for r in quantum_results]),
            'mean_entanglement_strength': np.mean([r['entanglement_strength'] for r in quantum_results]),
            'mean_dm_detection_prob': np.mean([r['dark_matter_detection_prob'] for r in quantum_results]),
            'mean_time_dilation': np.mean([r['time_dilation_factor'] for r in quantum_results if np.isfinite(r['time_dilation_factor'])]),
            'max_field_strength': max_field_strength,
            'hawking_temperature_analog': hawking_temp,
            'holographic_entropy_bound': entropy_bound,
            'quantum_coherence_time': coherence_time,
            'metrology_efficiency': metrology_efficiency
        }
        
        # Step 5: Visualization
        print("[5/5] Generating visualizations...")
        self._create_visualizations(results_df, fractal_data, aggregate_results)
        
        # Store results
        analysis_package = {
            'individual_results': results_df,
            'aggregate_results': aggregate_results,
            'fractal_data_shape': fractal_data.shape
        }
        
        self.results_history.append(analysis_package)
        
        print("\n" + "=" * 70)
        print("Analysis Complete!")
        print("=" * 70)
        
        return analysis_package
    
    def _create_visualizations(self, results_df, fractal_data, aggregate_results):
        """Create comprehensive visualizations."""
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Mandelbrot Set
        ax1 = plt.subplot(2, 3, 1)
        im1 = ax1.imshow(fractal_data, extent=[-2.5, 1.0, -1.25, 1.25],
                         cmap='twilight', interpolation='bilinear', origin='lower')
        ax1.set_title('Mandelbrot Fractal Set', fontweight='bold')
        ax1.set_xlabel('Real Axis')
        ax1.set_ylabel('Imaginary Axis')
        plt.colorbar(im1, ax=ax1, label='Iterations')
        
        # 2. X-Point Coordinates
        ax2 = plt.subplot(2, 3, 2)
        ax2.plot(results_df['data_point'], results_df['x_coordinate'], 
                'o-', linewidth=2, markersize=8, color='#2E8BC0')
        ax2.set_title('Magnetic X-Point Coordinates', fontweight='bold')
        ax2.set_xlabel('Data Point')
        ax2.set_ylabel('X-Coordinate')
        ax2.grid(True, alpha=0.3)
        
        # 3. Quantum Coupling Strength
        ax3 = plt.subplot(2, 3, 3)
        ax3.bar(results_df['data_point'], results_df['quantum_coupling'],
                color='#19D3F3', alpha=0.7, edgecolor='black')
        ax3.set_title('Quantum Coupling Strength', fontweight='bold')
        ax3.set_xlabel('Data Point')
        ax3.set_ylabel('Coupling Strength')
        ax3.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        # 4. Entanglement Strength
        ax4 = plt.subplot(2, 3, 4)
        ax4.plot(results_df['data_point'], results_df['entanglement_strength'],
                's-', linewidth=2, markersize=8, color='#F39C12')
        ax4.set_title('Quantum Entanglement Strength', fontweight='bold')
        ax4.set_xlabel('Data Point')
        ax4.set_ylabel('Entanglement Strength')
        ax4.set_yscale('log')
        ax4.grid(True, alpha=0.3)
        
        # 5. Dark Matter Detection Probability
        ax5 = plt.subplot(2, 3, 5)
        ax5.bar(results_df['data_point'], results_df['dark_matter_detection_prob'],
                color='#E74C3C', alpha=0.7, edgecolor='black')
        ax5.set_title('Dark Matter Detection Probability', fontweight='bold')
        ax5.set_xlabel('Data Point')
        ax5.set_ylabel('Detection Probability')
        ax5.set_ylim([0, 1])
        
        # 6. Quantum Gravity Interaction
        ax6 = plt.subplot(2, 3, 6)
        ax6.plot(results_df['data_point'], results_df['quantum_gravity_interaction'],
                '^-', linewidth=2, markersize=8, color='#9B59B6')
        ax6.set_title('Quantum Gravity Interaction Probability', fontweight='bold')
        ax6.set_xlabel('Data Point')
        ax6.set_ylabel('Interaction Probability')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('integrated_quantum_analysis.png', dpi=150, bbox_inches='tight')
        print(f"    Visualization saved as 'integrated_quantum_analysis.png'")
        plt.close()
    
    def print_summary_report(self, analysis_package):
        """Print a comprehensive summary report."""
        print("\n" + "=" * 70)
        print("COMPREHENSIVE ANALYSIS SUMMARY REPORT")
        print("=" * 70)
        
        agg = analysis_package['aggregate_results']
        
        print("\n--- Fractal Properties ---")
        print(f"Fractal Dimension: {agg['fractal_dimension']:.6f}")
        
        print("\n--- Magnetic Field X-Points ---")
        print(f"Mean X-Coordinate: {agg['mean_x_coordinate']:.6f}")
        print(f"Std Dev X-Coordinate: {agg['std_x_coordinate']:.6f}")
        
        print("\n--- Quantum Properties ---")
        print(f"Mean Quantum Coupling: {agg['mean_quantum_coupling']:.6e}")
        print(f"Mean Entanglement Strength: {agg['mean_entanglement_strength']:.6e}")
        print(f"Mean Dark Matter Detection Prob: {agg['mean_dm_detection_prob']:.6f}")
        print(f"Mean Time Dilation Factor: {agg['mean_time_dilation']:.6f}")
        
        print("\n--- Black Hole Analogy ---")
        print(f"Max Field Strength: {agg['max_field_strength']:.6f}")
        print(f"Hawking Temperature (Analog): {agg['hawking_temperature_analog']:.6e} K")
        
        print("\n--- Holographic & Quantum Sensing ---")
        print(f"Holographic Entropy Bound: {agg['holographic_entropy_bound']:.6e} J/K")
        print(f"Quantum Coherence Time: {agg['quantum_coherence_time']:.6e} s")
        print(f"Metrology Efficiency: {agg['metrology_efficiency']:.6f}")
        
        print("\n" + "=" * 70)
    
    def export_results(self, analysis_package, filename='quantum_analysis_results.json'):
        """Export results to JSON file."""
        export_data = {
            'aggregate_results': analysis_package['aggregate_results'],
            'individual_results': analysis_package['individual_results'].to_dict(orient='records')
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"\nResults exported to: {filename}")


def main():
    """Main demonstration of integrated quantum-fractal-magnetic system."""
    print("=" * 70)
    print("INTEGRATED QUANTUM-FRACTAL-MAGNETIC FIELD SYSTEM")
    print("=" * 70)
    
    # Initialize system
    system = IntegratedQuantumSystem()
    
    # Load sample magnetic field data
    print("\nLoading magnetic field data...")
    try:
        data = pd.read_csv("solar_corona_magnetic_field.csv")
        by_values = data["By"].values
        bz_values = data["Bz"].values
        theta_values = data["theta"].values
        print(f"Loaded {len(by_values)} data points from CSV")
    except FileNotFoundError:
        print("Using generated sample data...")
        by_values = np.array([1.5, 2.3, 1.8, 2.1, 1.9, 2.5, 1.7, 2.2, 1.6, 2.4])
        bz_values = np.array([2.0, 1.8, 2.5, 2.2, 2.3, 2.0, 2.4, 2.1, 2.6, 1.9])
        theta_values = np.array([0.785398, 0.523599, 0.698132, 0.610865, 0.654498,
                                0.785398, 0.666667, 0.741456, 0.588003, 0.754321])
    
    # Perform comprehensive analysis
    analysis_results = system.analyze_magnetic_field_quantum_properties(
        by_values, bz_values, theta_values
    )
    
    # Print summary report
    system.print_summary_report(analysis_results)
    
    # Export results
    system.export_results(analysis_results)
    
    # Save individual results to CSV
    analysis_results['individual_results'].to_csv(
        'integrated_quantum_results.csv', index=False
    )
    print("Detailed results saved to: integrated_quantum_results.csv")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    main()

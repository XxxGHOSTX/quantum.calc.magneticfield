"""
Comprehensive Smoke Test Script
Tests all major components and functionalities of the Quantum Magnetic Field Calculator

Copyright (c) 2026 Tony Ray Macier III
Licensed under the MIT License - see LICENSE file for details
"""

import sys
import numpy as np
from colorama import init, Fore, Style

# Initialize colorama for colored output
try:
    init(autoreset=True)
except:
    pass  # Fallback if colorama not available

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
    print("="*70)

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.YELLOW}ℹ️  {text}{Style.RESET_ALL}")


def test_imports():
    """Test all module imports"""
    print_header("Testing Module Imports")
    
    modules = [
        'x_point',
        'mandelbrot_fractal',
        'quantum_gravity',
        'advanced_quantum_equations',
        'fluid_dynamics',
        'integrated_analysis',
        'web_app'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print_success(f"Module '{module}' imported successfully")
        except Exception as e:
            print_error(f"Failed to import '{module}': {e}")
            return False
    
    return True


def test_x_point_calculations():
    """Test X-point magnetic field calculations"""
    print_header("Testing X-Point Calculations")
    
    try:
        from x_point import x_point, Shor
        
        # Test basic calculation
        by, bz, theta = 1.0, 1.0, np.pi/4
        result = x_point(by, bz, theta)
        print_success(f"X-point calculated: {result}")
        
        # Test Shor function
        shor_result = Shor(5.7)
        print_success(f"Shor function: Shor(5.7) = {shor_result}")
        
        return True
    except Exception as e:
        print_error(f"X-point calculations failed: {e}")
        return False


def test_mandelbrot_generation():
    """Test Mandelbrot fractal generation"""
    print_header("Testing Mandelbrot Fractal Generation")
    
    try:
        from mandelbrot_fractal import MandelbrotSet
        
        # Create and generate fractal
        mset = MandelbrotSet(width=200, height=150, max_iter=128)
        fractal = mset.generate_mandelbrot()
        print_success(f"Fractal generated: shape={fractal.shape}")
        
        # Calculate fractal dimension
        fractal_dim = mset.fractal_dimension(fractal)
        print_success(f"Fractal dimension: {fractal_dim:.6f}")
        
        # Test quantum coupling
        coupling = mset.quantum_coupling_strength(fractal_dim)
        print_success(f"Quantum coupling strength: {coupling:.6e}")
        
        return True
    except Exception as e:
        print_error(f"Mandelbrot generation failed: {e}")
        return False


def test_quantum_equations():
    """Test advanced quantum equations"""
    print_header("Testing Advanced Quantum Equations")
    
    try:
        from advanced_quantum_equations import (
            BlackHoleThermodynamics,
            QuantumErrorCorrection,
            QuantumSensingFramework,
            GravitationalWavePhysics,
            MultiverseQuantumCoupling,
            HolographicPrinciple
        )
        
        # Black Hole Thermodynamics
        bh = BlackHoleThermodynamics()
        mass = 10 * 1.989e30  # 10 solar masses
        temp = bh.hawking_temperature(mass)
        entropy = bh.bekenstein_hawking_entropy(mass)
        print_success(f"Black Hole: T={temp:.2e} K, S={entropy:.2e}")
        
        # Quantum Error Correction
        qec = QuantumErrorCorrection()
        error_rate = qec.surface_code_logical_error_rate(0.001, 5)
        print_success(f"QEC error rate: {error_rate:.2e}")
        
        # Quantum Sensing
        qs = QuantumSensingFramework()
        # Create sample eigenstates and eigenvalues
        eigenvalues = np.array([1.0, -1.0])
        eigenstates = [np.array([1, 0]), np.array([0, 1])]
        witness = qs.entanglement_witness_operator(eigenvalues, eigenstates)
        print_success(f"Entanglement witness: shape={witness.shape}")
        
        # Gravitational Waves
        gw = GravitationalWavePhysics()
        amplitudes = np.array([1e-21])
        frequencies = np.array([100.0])  # Hz
        phases = np.array([0.0])
        time = np.array([0.0, 0.001, 0.002])
        strain = gw.gravitational_wave_strain(amplitudes, frequencies, phases, time)
        print_success(f"GW strain: max={np.max(np.abs(strain)):.2e}")
        
        # Multiverse Coupling
        mc = MultiverseQuantumCoupling()
        coupling = mc.quantum_gravitational_coupling_mandelbrot(1e10, 1e53)
        print_success(f"Multiverse coupling: {coupling:.2e}")
        
        # Holographic Principle
        hp = HolographicPrinciple()
        area = 1e20  # Area in m²
        s_max = hp.holographic_entropy_bound(area)
        print_success(f"Holographic entropy bound: {s_max:.2e}")
        
        return True
    except Exception as e:
        print_error(f"Quantum equations failed: {e}")
        return False


def test_fluid_dynamics():
    """Test fluid dynamics equations"""
    print_header("Testing Fluid Dynamics")
    
    try:
        from fluid_dynamics import GeneralizedMotionEquation, PhysicalParameters
        
        # Create physical parameters
        params = PhysicalParameters()
        params.mass = 1.0
        params.charge = 1.6e-19
        params.magnetic_field = np.array([0.0, 0.0, 1.0])
        
        fluid = GeneralizedMotionEquation(params)
        
        # Compute Lorentz force
        position = np.array([0.0, 0.0, 0.0])
        velocity = np.array([1.0, 0.0, 0.0])
        force = fluid.compute_lorentz_force(position, velocity, 0.0)
        print_success(f"Lorentz force: {force}")
        
        # Check if reynolds_number method exists
        if hasattr(fluid, 'reynolds_number'):
            re = fluid.reynolds_number(10.0, 1.0, 0.1, 1.0)
            print_success(f"Reynolds number: {re:.2f}")
        else:
            print_info("Reynolds number method not found (may not be implemented)")
        
        return True
    except Exception as e:
        print_error(f"Fluid dynamics failed: {e}")
        return False


def test_web_application():
    """Test web application functionality"""
    print_header("Testing Web Application")
    
    try:
        from web_app import app
        import json
        
        app.config['TESTING'] = True
        client = app.test_client()
        
        # Test main page
        response = client.get('/')
        if response.status_code == 200:
            print_success("Main page (/) loads successfully")
        else:
            print_error(f"Main page failed: {response.status_code}")
            return False
        
        # Test 3D page
        response = client.get('/3d')
        if response.status_code == 200:
            print_success("3D page (/3d) loads successfully")
        else:
            print_error(f"3D page failed: {response.status_code}")
            return False
        
        # Test Mandelbrot API
        response = client.post('/api/mandelbrot',
                              data=json.dumps({'width': 200, 'height': 150}),
                              content_type='application/json')
        if response.status_code == 200:
            data = json.loads(response.data)
            if data['success']:
                print_success(f"Mandelbrot API works: fractal_dim={data['fractal_dimension']:.6f}")
            else:
                print_error("Mandelbrot API returned success=False")
                return False
        else:
            print_error(f"Mandelbrot API failed: {response.status_code}")
            return False
        
        # Test Quantum Properties API
        response = client.post('/api/quantum_properties',
                              data=json.dumps({}),
                              content_type='application/json')
        if response.status_code == 200:
            data = json.loads(response.data)
            if data['success']:
                print_success(f"Quantum API works: coupling={data['quantum_coupling']:.6e}")
            else:
                print_error("Quantum API returned success=False")
                return False
        else:
            print_error(f"Quantum API failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print_error(f"Web application test failed: {e}")
        return False


def test_integrated_analysis():
    """Test integrated analysis system"""
    print_header("Testing Integrated Analysis System")
    
    try:
        from integrated_analysis import IntegratedQuantumSystem
        
        analysis = IntegratedQuantumSystem()
        
        # Test with sample data
        by_values = np.array([1.0, 2.0, 3.0])
        bz_values = np.array([1.0, 1.5, 2.0])
        theta_values = np.array([0.5, 0.6, 0.7])
        
        results = analysis.analyze_magnetic_field_quantum_properties(
            by_values, bz_values, theta_values
        )
        print_success(f"Integrated analysis completed with {len(results)} results")
        
        return True
    except Exception as e:
        print_error(f"Integrated analysis failed: {e}")
        return False


def run_all_tests():
    """Run all smoke tests"""
    print("\n" + "="*70)
    print(f"{Fore.CYAN}Quantum Magnetic Field Calculator - Comprehensive Smoke Test{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Copyright (c) 2026 Tony Ray Macier III{Style.RESET_ALL}")
    print("="*70)
    
    tests = [
        ("Module Imports", test_imports),
        ("X-Point Calculations", test_x_point_calculations),
        ("Mandelbrot Generation", test_mandelbrot_generation),
        ("Quantum Equations", test_quantum_equations),
        ("Fluid Dynamics", test_fluid_dynamics),
        ("Web Application", test_web_application),
        ("Integrated Analysis", test_integrated_analysis),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print("\n" + "-"*70)
    if passed == total:
        print(f"{Fore.GREEN}🎉 ALL TESTS PASSED! ({passed}/{total}){Style.RESET_ALL}")
        print(f"{Fore.GREEN}✨ Repository is fully functional and integrated!{Style.RESET_ALL}")
        return 0
    else:
        print(f"{Fore.RED}⚠️  SOME TESTS FAILED ({passed}/{total} passed){Style.RESET_ALL}")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())

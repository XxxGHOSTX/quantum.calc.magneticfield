"""
Interactive Web Application for Mandelbrot Fractal and Magnetic Field Visualization
Integrates quantum mechanics, fractal geometry, and magnetic field calculations

Copyright (c) 2026 Tony Ray Macier III
Licensed under the MIT License - see LICENSE file for details

Author: Tony Ray Macier III
GitHub: @XxxGHOSTX
Project: Quantum Magnetic Field Calculator with Mandelbrot Fractal Analysis
"""

from flask import Flask, render_template, jsonify, request, redirect
import numpy as np
import json
from mandelbrot_fractal import MandelbrotSet, integrate_mandelbrot_xpoint
from x_point import x_point
from advanced_quantum_equations import (
    BlackHoleThermodynamics, QuantumErrorCorrection, 
    QuantumSensingFramework, MultiverseQuantumCoupling
)

app = Flask(__name__)


@app.route('/')
def index():
    """Main page route - 2D visualization"""
    return render_template('index.html')


@app.route('/3d')
def advanced_3d():
    """Advanced 3D visualization with Three.js"""
    return render_template('advanced_3d.html')


@app.route('/api/mandelbrot', methods=['POST'])
def generate_mandelbrot():
    """
    API endpoint to generate Mandelbrot set data
    """
    try:
        data = request.get_json()
        
        width = data.get('width', 800)
        height = data.get('height', 600)
        max_iter = data.get('max_iter', 256)
        xmin = data.get('xmin', -2.5)
        xmax = data.get('xmax', 1.0)
        ymin = data.get('ymin', -1.25)
        ymax = data.get('ymax', 1.25)
        
        mandelbrot = MandelbrotSet(width=width, height=height, max_iter=max_iter)
        fractal_data = mandelbrot.generate_mandelbrot(xmin, xmax, ymin, ymax)
        fractal_dim = mandelbrot.fractal_dimension(fractal_data)
        
        # Convert to list for JSON serialization
        fractal_list = fractal_data.tolist()
        
        return jsonify({
            'success': True,
            'data': fractal_list,
            'fractal_dimension': fractal_dim,
            'width': width,
            'height': height,
            'bounds': {
                'xmin': xmin,
                'xmax': xmax,
                'ymin': ymin,
                'ymax': ymax
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/xpoint', methods=['POST'])
def calculate_xpoint():
    """
    API endpoint to calculate magnetic x-points
    """
    try:
        data = request.get_json()
        
        by = np.array(data.get('by', []))
        bz = np.array(data.get('bz', []))
        theta = np.array(data.get('theta', []))
        
        if len(by) == 0 or len(bz) == 0 or len(theta) == 0:
            return jsonify({'success': False, 'error': 'Missing input data'}), 400
        
        # Calculate x-points
        x_points = x_point(by, bz, theta)
        
        return jsonify({
            'success': True,
            'x_points': x_points.tolist(),
            'count': len(x_points)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/integrate', methods=['POST'])
def integrate_calculations():
    """
    API endpoint to integrate Mandelbrot and x-point calculations
    """
    try:
        data = request.get_json()
        
        by = np.array(data.get('by', []))
        bz = np.array(data.get('bz', []))
        theta = np.array(data.get('theta', []))
        
        width = data.get('width', 400)
        height = data.get('height', 300)
        max_iter = data.get('max_iter', 128)
        
        mandelbrot = MandelbrotSet(width=width, height=height, max_iter=max_iter)
        results_df = integrate_mandelbrot_xpoint(by, bz, theta, mandelbrot)
        
        return jsonify({
            'success': True,
            'results': results_df.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/quantum_properties', methods=['POST'])
def quantum_properties():
    """
    API endpoint to calculate quantum properties
    """
    try:
        data = request.get_json()
        
        fractal_dim = data.get('fractal_dim', 1.5)
        separation = data.get('separation', 1e-9)
        mass_set = data.get('mass_set', 1e10)
        mass_universe = data.get('mass_universe', 1e53)
        
        mandelbrot = MandelbrotSet()
        
        coupling = mandelbrot.quantum_coupling_strength(fractal_dim, mass_set, mass_universe)
        entanglement = mandelbrot.quantum_entanglement_strength(separation, fractal_dim, mass_set, mass_universe)
        
        return jsonify({
            'success': True,
            'quantum_coupling': coupling,
            'entanglement_strength': entanglement,
            'fractal_dimension': fractal_dim
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/dark_matter', methods=['POST'])
def dark_matter_detection():
    """
    API endpoint to calculate dark matter detection probability
    """
    try:
        data = request.get_json()
        
        sigma_detect = data.get('sigma_detect', 1e-45)
        sigma_total = data.get('sigma_total', 1e-40)
        delta = data.get('delta', 0.5)
        delta_max = data.get('delta_max', 1.0)
        
        mandelbrot = MandelbrotSet()
        p_detect = mandelbrot.dark_matter_detection_probability(
            sigma_detect, sigma_total, delta, delta_max
        )
        
        return jsonify({
            'success': True,
            'detection_probability': p_detect,
            'parameters': {
                'sigma_detect': sigma_detect,
                'sigma_total': sigma_total,
                'delta': delta,
                'delta_max': delta_max
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    print("=" * 60)
    print("Starting Quantum Magnetic Field Fractal Web Application")
    print("=" * 60)
    print("\nAvailable Routes:")
    print("  - 2D Visualization: http://127.0.0.1:5000")
    print("  - 3D Advanced View: http://127.0.0.1:5000/3d")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

# Usage Examples
## Quantum Magnetic Field Calculator with Mandelbrot Fractal Analysis

**Copyright © 2026 Tony Ray Macier III** | Licensed under MIT License

---

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Command Line Examples](#command-line-examples)
4. [Web Application Examples](#web-application-examples)
5. [Python API Examples](#python-api-examples)
6. [Advanced Examples](#advanced-examples)

---

## Installation

### Using pip
```bash
# Clone repository
git clone https://github.com/XxxGHOSTX/quantum.calc.magneticfield.git
cd quantum.calc.magneticfield

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

### Using conda
```bash
# Clone repository
git clone https://github.com/XxxGHOSTX/quantum.calc.magneticfield.git
cd quantum.calc.magneticfield

# Create conda environment
conda env create -f environment.yml
conda activate quantum-magnetic-field
```

### Verify Installation
```bash
# Run tests
python -m pytest test_x_point.py -v
python -m pytest test_integration.py -v

# Run smoke test
python smoke_test.py
```

---

## Quick Start

### Start Web Application
```bash
python web_app.py
```

Then open in your browser:
- **2D Interface**: http://localhost:5000
- **3D Interface**: http://localhost:5000/3d

---

## Command Line Examples

### Example 1: Calculate Magnetic X-Points
```bash
python x_point.py
```

This reads data from `solar_corona_magnetic_field.csv` and calculates x-points for solar corona magnetic fields.

### Example 2: Generate Mandelbrot Fractal
```python
# Create file: generate_fractal.py
from mandelbrot_fractal import MandelbrotSet

# Generate fractal
mset = MandelbrotSet(width=800, height=600, max_iter=256)
fractal = mset.generate_mandelbrot()

# Visualize and save
mset.visualize_mandelbrot(fractal, save_path='my_fractal.png')
print(f"Fractal saved to my_fractal.png")
```

Run with:
```bash
python generate_fractal.py
```

### Example 3: Integrated Analysis
```python
# Create file: analyze_system.py
from integrated_analysis import IntegratedQuantumSystem
import numpy as np

# Create system
system = IntegratedQuantumSystem()

# Magnetic field data
by = np.array([1.0, 1.5, 2.0, 2.5, 3.0])
bz = np.array([1.0, 1.2, 1.4, 1.6, 1.8])
theta = np.array([0.5, 0.6, 0.7, 0.8, 0.9])

# Analyze
results = system.analyze_magnetic_field_quantum_properties(by, bz, theta)
print(f"Analysis complete! {len(results)} data points processed")
```

Run with:
```bash
python analyze_system.py
```

---

## Web Application Examples

### Example 1: Generate Fractal via API
```python
import requests
import json

url = "http://localhost:5000/api/mandelbrot"
params = {
    "width": 800,
    "height": 600,
    "max_iter": 256,
    "xmin": -2.5,
    "xmax": 1.0,
    "ymin": -1.25,
    "ymax": 1.25
}

response = requests.post(url, json=params)
data = response.json()

if data['success']:
    print(f"Fractal dimension: {data['fractal_dimension']:.6f}")
    print(f"Data shape: {len(data['data'])} x {len(data['data'][0])}")
else:
    print(f"Error: {data['error']}")
```

### Example 2: Zoom Into Interesting Region
```python
import requests

# Zoom into the "Seahorse Valley" region
url = "http://localhost:5000/api/mandelbrot"
params = {
    "width": 1200,
    "height": 900,
    "max_iter": 512,
    "xmin": -0.75,
    "xmax": -0.74,
    "ymin": 0.11,
    "ymax": 0.12
}

response = requests.post(url, json=params)
data = response.json()
print(f"High-detail fractal generated: {data['fractal_dimension']:.6f}")
```

### Example 3: Calculate Quantum Properties
```python
import requests

# Get fractal dimension first
fractal_response = requests.post(
    "http://localhost:5000/api/mandelbrot",
    json={"width": 400, "height": 300}
)
fractal_data = fractal_response.json()
fractal_dim = fractal_data['fractal_dimension']

# Calculate quantum properties
quantum_response = requests.post(
    "http://localhost:5000/api/quantum_properties",
    json={
        "fractal_dim": fractal_dim,
        "separation": 1e-10,
        "mass_set": 1e11,
        "mass_universe": 1e54
    }
)
quantum_data = quantum_response.json()

print(f"Quantum Coupling: {quantum_data['quantum_coupling']:.6e}")
print(f"Entanglement Strength: {quantum_data['entanglement_strength']:.6e}")
```

---

## Python API Examples

### Example 1: Black Hole Properties
```python
from advanced_quantum_equations import BlackHoleThermodynamics

# Create black hole calculator
bh = BlackHoleThermodynamics()

# Calculate properties for different mass black holes
masses = [1, 5, 10, 50, 100]  # Solar masses

print("Black Hole Properties")
print("=" * 60)
for m_solar in masses:
    mass = m_solar * 1.989e30  # Convert to kg
    temp = bh.hawking_temperature(mass)
    entropy = bh.bekenstein_hawking_entropy(mass)
    radius = bh.schwarzschild_radius(mass)
    
    print(f"\n{m_solar} M☉:")
    print(f"  Schwarzschild radius: {radius:.2e} m")
    print(f"  Hawking temperature: {temp:.2e} K")
    print(f"  Entropy: {entropy:.2e} J/K")
```

### Example 2: Quantum Error Correction Analysis
```python
from advanced_quantum_equations import QuantumErrorCorrection
import numpy as np
import matplotlib.pyplot as plt

qec = QuantumErrorCorrection()

# Analyze error rates for different code distances
physical_error = 0.001  # 0.1% physical error rate
code_distances = range(3, 16, 2)
logical_errors = []

for d in code_distances:
    logical_error = qec.surface_code_logical_error_rate(physical_error, d)
    logical_errors.append(logical_error)
    print(f"Code distance {d}: {logical_error:.2e}")

# Plot results
plt.figure(figsize=(10, 6))
plt.semilogy(code_distances, logical_errors, 'o-', linewidth=2)
plt.xlabel('Code Distance')
plt.ylabel('Logical Error Rate')
plt.title('QEC Performance vs Code Distance')
plt.grid(True, alpha=0.3)
plt.savefig('qec_analysis.png', dpi=150)
print("\nPlot saved as qec_analysis.png")
```

### Example 3: Fractal Dimension vs Quantum Coupling
```python
from mandelbrot_fractal import MandelbrotSet
import numpy as np

# Generate fractals at different zoom levels
zoom_levels = [1.0, 10.0, 100.0, 1000.0]
results = []

for zoom in zoom_levels:
    # Adjust bounds for zoom
    center_x, center_y = -0.75, 0.1
    width = 3.5 / zoom
    
    mset = MandelbrotSet(width=400, height=300, max_iter=int(128 + zoom))
    fractal = mset.generate_mandelbrot(
        xmin=center_x - width/2,
        xmax=center_x + width/2,
        ymin=center_y - width/2,
        ymax=center_y + width/2
    )
    
    fractal_dim = mset.fractal_dimension(fractal)
    coupling = mset.quantum_coupling_strength(fractal_dim)
    
    results.append({
        'zoom': zoom,
        'fractal_dim': fractal_dim,
        'coupling': coupling
    })
    
    print(f"Zoom {zoom:>7.1f}x: D={fractal_dim:.6f}, Coupling={coupling:.6e}")

print("\nFractal dimension changes with zoom level!")
```

### Example 4: Gravitational Wave Detection
```python
from advanced_quantum_equations import GravitationalWavePhysics
import numpy as np
import matplotlib.pyplot as plt

gw = GravitationalWavePhysics()

# Simulate LIGO-like detection
time = np.linspace(0, 1.0, 10000)  # 1 second of data at 10kHz

# Two black holes merging (simplified)
amplitudes = np.array([1e-21, 5e-22])
frequencies = np.array([100.0, 250.0])  # Hz
phases = np.array([0.0, np.pi/4])

strain = gw.gravitational_wave_strain(amplitudes, frequencies, phases, time)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(time * 1000, strain, linewidth=0.5)
plt.xlabel('Time (ms)')
plt.ylabel('Strain')
plt.title('Gravitational Wave Signal')
plt.grid(True, alpha=0.3)
plt.savefig('gw_signal.png', dpi=150)
print(f"Max strain: {np.max(np.abs(strain)):.2e}")
print("Plot saved as gw_signal.png")
```

### Example 5: Dark Matter Detection Probability
```python
from mandelbrot_fractal import MandelbrotSet
import numpy as np

mset = MandelbrotSet()

# Vary quantum fluctuation parameters
deltas = np.linspace(0.1, 1.0, 10)
probabilities = []

for delta in deltas:
    prob = mset.dark_matter_detection_probability(
        sigma_detect=1e-45,
        sigma_total=1e-40,
        delta=delta,
        delta_max=1.0
    )
    probabilities.append(prob)
    print(f"δ = {delta:.2f}: P_detect = {prob:.6f}")

print(f"\nDetection probability varies from {min(probabilities):.6f} to {max(probabilities):.6f}")
```

---

## Advanced Examples

### Example 1: Complete System Analysis
```python
from integrated_analysis import IntegratedQuantumSystem
import numpy as np
import pandas as pd

# Initialize system
system = IntegratedQuantumSystem()

# Generate synthetic magnetic field data
n_points = 50
by = 1.0 + 0.5 * np.sin(np.linspace(0, 2*np.pi, n_points))
bz = 1.0 + 0.3 * np.cos(np.linspace(0, 2*np.pi, n_points))
theta = np.linspace(0.3, 1.0, n_points)

# Perform comprehensive analysis
print("Starting comprehensive analysis...")
results = system.analyze_magnetic_field_quantum_properties(by, bz, theta)

# Convert to DataFrame for easy analysis
df = pd.DataFrame(results)

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Save results
df.to_csv('comprehensive_analysis_results.csv', index=False)
print("\nResults saved to comprehensive_analysis_results.csv")
```

### Example 2: Batch Processing Multiple Regions
```python
from mandelbrot_fractal import MandelbrotSet
import json

# Define interesting regions
regions = {
    "main_set": {"xmin": -2.5, "xmax": 1.0, "ymin": -1.25, "ymax": 1.25},
    "seahorse": {"xmin": -0.75, "xmax": -0.74, "ymin": 0.11, "ymax": 0.12},
    "elephant": {"xmin": -0.16, "xmax": -0.15, "ymin": 1.03, "ymax": 1.04},
    "spiral": {"xmin": -0.76, "xmax": -0.74, "ymin": 0.08, "ymax": 0.10}
}

results = {}

for name, bounds in regions.items():
    print(f"\nProcessing {name}...")
    mset = MandelbrotSet(width=800, height=600, max_iter=512)
    fractal = mset.generate_mandelbrot(**bounds)
    fractal_dim = mset.fractal_dimension(fractal)
    
    results[name] = {
        "fractal_dimension": fractal_dim,
        "bounds": bounds
    }
    
    # Save image
    mset.visualize_mandelbrot(fractal, save_path=f'fractal_{name}.png')
    print(f"  Dimension: {fractal_dim:.6f}")
    print(f"  Image saved: fractal_{name}.png")

# Save metadata
with open('batch_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nMetadata saved to batch_results.json")
```

### Example 3: Real-time Monitoring System
```python
from web_app import app
import threading
import time
import requests

def monitor_system():
    """Monitor system performance"""
    base_url = "http://localhost:5000"
    
    while True:
        try:
            # Test API responsiveness
            start = time.time()
            response = requests.post(
                f"{base_url}/api/mandelbrot",
                json={"width": 200, "height": 150},
                timeout=10
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API healthy - Response time: {duration:.3f}s - "
                      f"Fractal dim: {data['fractal_dimension']:.6f}")
            else:
                print(f"⚠️  API issue - Status code: {response.status_code}")
        
        except Exception as e:
            print(f"❌ API error: {e}")
        
        time.sleep(30)  # Check every 30 seconds

if __name__ == '__main__':
    # Start monitoring in background thread
    monitor_thread = threading.Thread(target=monitor_system, daemon=True)
    monitor_thread.start()
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)
```

### Example 4: Performance Benchmark
```python
import time
import numpy as np
from mandelbrot_fractal import MandelbrotSet

# Benchmark different resolutions
resolutions = [
    (200, 150),
    (400, 300),
    (800, 600),
    (1200, 900),
    (1600, 1200)
]

print("Mandelbrot Generation Performance Benchmark")
print("=" * 60)

for width, height in resolutions:
    mset = MandelbrotSet(width=width, height=height, max_iter=256)
    
    start = time.time()
    fractal = mset.generate_mandelbrot()
    duration = time.time() - start
    
    pixels = width * height
    pixels_per_second = pixels / duration
    
    print(f"{width}x{height:>4} ({pixels:>8} px): "
          f"{duration:>6.3f}s ({pixels_per_second:>10,.0f} px/s)")

print("=" * 60)
```

---

## Tips and Best Practices

### 1. Memory Management
For large fractals, use lower resolutions or increase system memory:
```python
# Good for memory-constrained systems
mset = MandelbrotSet(width=400, height=300, max_iter=128)

# High quality but memory intensive
mset = MandelbrotSet(width=1920, height=1080, max_iter=1024)
```

### 2. Iteration Optimization
Adjust iterations based on zoom level:
```python
def optimal_iterations(zoom_level):
    """Calculate optimal iterations for zoom level"""
    return min(1024, int(256 + zoom_level * 10))

zoom = 100
max_iter = optimal_iterations(zoom)
mset = MandelbrotSet(max_iter=max_iter)
```

### 3. Error Handling
Always wrap API calls in try-except:
```python
try:
    response = requests.post(url, json=params, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
```

### 4. Batch Processing
Process multiple items efficiently:
```python
from concurrent.futures import ThreadPoolExecutor

def process_point(params):
    by, bz, theta = params
    return x_point(by, bz, theta)

# Parallel processing
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_point, data_points))
```

---

## Troubleshooting

### Issue: Import Errors
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: Web App Won't Start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Use different port
python web_app.py --port 5001
```

### Issue: Slow Fractal Generation
```python
# Use lower resolution
mset = MandelbrotSet(width=400, height=300, max_iter=128)

# Or enable parallel processing (if available)
# mset = MandelbrotSet(width=800, height=600, parallel=True)
```

---

## Additional Resources

- **API Documentation**: See `API_DOCUMENTATION.md`
- **Complete System Guide**: See `COMPLETE_SYSTEM_GUIDE.md`
- **Publication Documentation**: See `PUBLICATION_DOCUMENTATION.md`
- **GitHub Repository**: https://github.com/XxxGHOSTX/quantum.calc.magneticfield

---

**Copyright © 2026 Tony Ray Macier III | MIT License | Attribution Required**

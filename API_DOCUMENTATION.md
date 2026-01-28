# API Documentation
## Quantum Magnetic Field Calculator with Mandelbrot Fractal Analysis

**Copyright © 2026 Tony Ray Macier III** | Licensed under MIT License

---

## Table of Contents
1. [Web Routes](#web-routes)
2. [API Endpoints](#api-endpoints)
3. [Python API](#python-api)
4. [Data Formats](#data-formats)
5. [Error Handling](#error-handling)

---

## Web Routes

### GET `/`
**2D Mandelbrot Fractal Visualization**

Returns the main HTML interface with interactive Mandelbrot fractal explorer.

**Features:**
- Infinite zoom animation
- Real-time fractal generation
- Quantum properties calculator
- Magnetic field visualization

**Response:** HTML page

---

### GET `/3d`
**3D Advanced Quantum Visualization**

Returns the 3D visualization interface built with Three.js.

**Features:**
- Black hole with Hawking radiation
- Fractal spacetime landscapes
- Quantum error correction lattice
- Interactive Bloch sphere

**Response:** HTML page

---

## API Endpoints

All API endpoints accept and return JSON data.

### POST `/api/mandelbrot`
**Generate Mandelbrot Fractal Set**

Generates a Mandelbrot fractal with specified parameters.

**Request Body:**
```json
{
  "width": 800,           // Image width in pixels (default: 800)
  "height": 600,          // Image height in pixels (default: 600)
  "max_iter": 256,        // Maximum iterations (default: 256)
  "xmin": -2.5,          // Minimum real coordinate
  "xmax": 1.0,           // Maximum real coordinate
  "ymin": -1.25,         // Minimum imaginary coordinate
  "ymax": 1.25           // Maximum imaginary coordinate
}
```

**Response:**
```json
{
  "success": true,
  "data": [[...]],               // 2D array of iteration counts
  "fractal_dimension": 1.85,     // Calculated fractal dimension
  "width": 800,
  "height": 600,
  "bounds": {
    "xmin": -2.5,
    "xmax": 1.0,
    "ymin": -1.25,
    "ymax": 1.25
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message"
}
```

---

### POST `/api/xpoint`
**Calculate Magnetic X-Points**

Calculates magnetic field x-points using quantum qubits.

**Request Body:**
```json
{
  "by": [1.0, 2.0, 3.0],        // By magnetic field components
  "bz": [1.0, 1.5, 2.0],        // Bz magnetic field components
  "theta": [0.5, 0.6, 0.7]      // Angle values in radians
}
```

**Response:**
```json
{
  "success": true,
  "x_points": [0.5, 0.6, 0.7],  // Calculated x-points
  "count": 3
}
```

---

### POST `/api/integrate`
**Integrated Mandelbrot and X-Point Calculation**

Performs integrated analysis combining Mandelbrot fractals and x-point calculations.

**Request Body:**
```json
{
  "by": [1.0, 2.0],
  "bz": [1.0, 1.5],
  "theta": [0.5, 0.6],
  "width": 400,
  "height": 300,
  "max_iter": 128
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "by": 1.0,
      "bz": 1.0,
      "theta": 0.5,
      "x_point": 0.5,
      "fractal_dimension": 1.85,
      ...
    },
    ...
  ]
}
```

---

### POST `/api/quantum_properties`
**Calculate Quantum Properties**

Calculates quantum coupling and entanglement strength based on fractal dimensions.

**Request Body:**
```json
{
  "fractal_dim": 1.5,           // Fractal dimension (default: 1.5)
  "separation": 1e-9,           // Separation distance in meters
  "mass_set": 1e10,             // Mass scale from set (kg)
  "mass_universe": 1e53         // Universe mass scale (kg)
}
```

**Response:**
```json
{
  "success": true,
  "quantum_coupling": 1.23e12,
  "entanglement_strength": 5.67e-20,
  "fractal_dimension": 1.5
}
```

---

### POST `/api/dark_matter`
**Dark Matter Detection Probability**

Calculates dark matter detection probability using quantum fluctuations in fractal spacetime.

**Request Body:**
```json
{
  "sigma_detect": 1e-45,        // Detection cross-section (m²)
  "sigma_total": 1e-40,         // Total cross-section (m²)
  "delta": 0.5,                 // Quantum fluctuation parameter
  "delta_max": 1.0              // Maximum fluctuation
}
```

**Response:**
```json
{
  "success": true,
  "detection_probability": 0.123,
  "parameters": {
    "sigma_detect": 1e-45,
    "sigma_total": 1e-40,
    "delta": 0.5,
    "delta_max": 1.0
  }
}
```

---

## Python API

### Core Modules

#### X-Point Calculations
```python
from x_point import x_point, Shor
import numpy as np

# Calculate x-points
by = np.array([1.0, 2.0, 3.0])
bz = np.array([1.0, 1.5, 2.0])
theta = np.array([0.5, 0.6, 0.7])

x_points = x_point(by, bz, theta)
print(f"X-points: {x_points}")
```

#### Mandelbrot Fractal Generation
```python
from mandelbrot_fractal import MandelbrotSet

# Create and generate fractal
mset = MandelbrotSet(width=800, height=600, max_iter=256)
fractal = mset.generate_mandelbrot(xmin=-2.5, xmax=1.0, ymin=-1.25, ymax=1.25)

# Calculate fractal dimension
fractal_dim = mset.fractal_dimension(fractal)
print(f"Fractal dimension: {fractal_dim:.6f}")

# Calculate quantum coupling
coupling = mset.quantum_coupling_strength(fractal_dim)
print(f"Quantum coupling: {coupling:.6e}")
```

#### Black Hole Thermodynamics
```python
from advanced_quantum_equations import BlackHoleThermodynamics

bh = BlackHoleThermodynamics()

# Calculate for a 10 solar mass black hole
mass = 10 * 1.989e30  # kg
temp = bh.hawking_temperature(mass)
entropy = bh.bekenstein_hawking_entropy(mass)

print(f"Hawking Temperature: {temp:.2e} K")
print(f"Bekenstein-Hawking Entropy: {entropy:.2e} J/K")
```

#### Quantum Error Correction
```python
from advanced_quantum_equations import QuantumErrorCorrection

qec = QuantumErrorCorrection()

# Surface code logical error rate
physical_error = 0.001  # 0.1% physical error rate
code_distance = 5
logical_error = qec.surface_code_logical_error_rate(physical_error, code_distance)

print(f"Logical error rate: {logical_error:.2e}")
```

#### Quantum Sensing Framework
```python
from advanced_quantum_equations import QuantumSensingFramework
import numpy as np

qs = QuantumSensingFramework()

# Entanglement witness operator
eigenvalues = np.array([1.0, -1.0])
eigenstates = [np.array([1, 0]), np.array([0, 1])]
witness = qs.entanglement_witness_operator(eigenvalues, eigenstates)

print(f"Witness operator shape: {witness.shape}")
```

#### Gravitational Wave Physics
```python
from advanced_quantum_equations import GravitationalWavePhysics
import numpy as np

gw = GravitationalWavePhysics()

# Calculate gravitational wave strain
amplitudes = np.array([1e-21, 2e-21])
frequencies = np.array([100.0, 200.0])  # Hz
phases = np.array([0.0, np.pi/4])
time = np.linspace(0, 0.1, 1000)

strain = gw.gravitational_wave_strain(amplitudes, frequencies, phases, time)
print(f"Max strain: {np.max(np.abs(strain)):.2e}")
```

#### Fluid Dynamics
```python
from fluid_dynamics import GeneralizedMotionEquation, PhysicalParameters
import numpy as np

# Create physical parameters
params = PhysicalParameters()
params.mass = 1.0
params.charge = 1.6e-19
params.magnetic_field = np.array([0.0, 0.0, 1.0])

# Create motion equation
fluid = GeneralizedMotionEquation(params)

# Calculate Lorentz force
position = np.array([0.0, 0.0, 0.0])
velocity = np.array([1.0, 0.0, 0.0])
force = fluid.compute_lorentz_force(position, velocity, 0.0)

print(f"Lorentz force: {force}")
```

#### Integrated Analysis
```python
from integrated_analysis import IntegratedQuantumSystem
import numpy as np

# Create integrated system
system = IntegratedQuantumSystem()

# Analyze magnetic field with quantum properties
by_values = np.array([1.0, 2.0, 3.0])
bz_values = np.array([1.0, 1.5, 2.0])
theta_values = np.array([0.5, 0.6, 0.7])

results = system.analyze_magnetic_field_quantum_properties(
    by_values, bz_values, theta_values
)

print(f"Analysis complete: {len(results)} results")
```

---

## Data Formats

### Mandelbrot Fractal Data
2D numpy array where each element represents the iteration count for that pixel coordinate.

### X-Point Results
1D numpy array of x-coordinate values for magnetic field null points.

### Quantum Properties
Dictionary containing:
- `quantum_coupling`: Gravitational-quantum coupling strength
- `entanglement_strength`: Quantum entanglement measure
- `fractal_dimension`: Calculated fractal dimension

---

## Error Handling

All API endpoints return consistent error format:

```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

HTTP Status Codes:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `500`: Internal Server Error

---

## Rate Limiting

No rate limiting is currently implemented. For production deployment, consider adding rate limiting middleware.

---

## CORS

CORS is not currently enabled. To enable CORS for cross-origin requests:

```python
from flask_cors import CORS
CORS(app)
```

---

## Authentication

No authentication is currently implemented. This is suitable for local development. For production deployment, implement authentication middleware.

---

## Example Usage

### Complete Workflow
```python
import requests
import json

# Base URL
base_url = "http://localhost:5000"

# 1. Generate Mandelbrot fractal
response = requests.post(f"{base_url}/api/mandelbrot", 
                        json={"width": 400, "height": 300})
data = response.json()
fractal_dim = data['fractal_dimension']
print(f"Fractal dimension: {fractal_dim}")

# 2. Calculate quantum properties
response = requests.post(f"{base_url}/api/quantum_properties",
                        json={"fractal_dim": fractal_dim})
data = response.json()
print(f"Quantum coupling: {data['quantum_coupling']}")

# 3. Calculate x-points
response = requests.post(f"{base_url}/api/xpoint",
                        json={
                            "by": [1.0, 2.0],
                            "bz": [1.0, 1.5],
                            "theta": [0.5, 0.6]
                        })
data = response.json()
print(f"X-points: {data['x_points']}")
```

---

## Support

For issues, questions, or contributions:
- **GitHub**: [@XxxGHOSTX](https://github.com/XxxGHOSTX)
- **Repository**: https://github.com/XxxGHOSTX/quantum.calc.magneticfield

---

**Copyright © 2026 Tony Ray Macier III | MIT License | Attribution Required**

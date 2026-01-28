"""
Integration Test Suite for Quantum Magnetic Field Calculator
Tests web application API endpoints and full system integration

Copyright (c) 2026 Tony Ray Macier III
Licensed under the MIT License - see LICENSE file for details
"""

import pytest
import json
import numpy as np
from web_app import app


@pytest.fixture
def client():
    """Create test client for Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestWebRoutes:
    """Test basic web routes"""
    
    def test_index_route(self, client):
        """Test main index page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'html' in response.data.lower()
    
    def test_3d_route(self, client):
        """Test 3D visualization page loads"""
        response = client.get('/3d')
        assert response.status_code == 200
        assert b'html' in response.data.lower()


class TestMandelbrotAPI:
    """Test Mandelbrot fractal API endpoints"""
    
    def test_mandelbrot_generation_default(self, client):
        """Test Mandelbrot generation with default parameters"""
        response = client.post('/api/mandelbrot',
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert 'fractal_dimension' in data
        assert isinstance(data['fractal_dimension'], float)
    
    def test_mandelbrot_generation_custom(self, client):
        """Test Mandelbrot generation with custom parameters"""
        params = {
            'width': 400,
            'height': 300,
            'max_iter': 128,
            'xmin': -2.0,
            'xmax': 1.0,
            'ymin': -1.0,
            'ymax': 1.0
        }
        response = client.post('/api/mandelbrot',
                               data=json.dumps(params),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['width'] == 400
        assert data['height'] == 300
        assert len(data['data']) == 300
        assert len(data['data'][0]) == 400
    
    def test_mandelbrot_generation_invalid(self, client):
        """Test Mandelbrot generation with invalid parameters"""
        params = {
            'width': -100,  # Invalid
            'height': 300
        }
        response = client.post('/api/mandelbrot',
                               data=json.dumps(params),
                               content_type='application/json')
        # Should either handle gracefully or return error
        assert response.status_code in [200, 400]


class TestXPointAPI:
    """Test X-Point calculation API endpoints"""
    
    def test_xpoint_calculation_simple(self, client):
        """Test X-point calculation with simple data"""
        params = {
            'by': [1.0, 2.0, 3.0],
            'bz': [1.0, 1.5, 2.0],
            'theta': [0.5, 0.6, 0.7]
        }
        response = client.post('/api/xpoint',
                               data=json.dumps(params),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'x_points' in data
        assert 'count' in data
    
    def test_xpoint_missing_data(self, client):
        """Test X-point calculation with missing data"""
        params = {
            'by': [],
            'bz': [],
            'theta': []
        }
        response = client.post('/api/xpoint',
                               data=json.dumps(params),
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False


class TestIntegrationAPI:
    """Test integrated calculations API"""
    
    def test_integrate_calculations(self, client):
        """Test integration of Mandelbrot and X-point calculations"""
        params = {
            'by': [1.0, 2.0],
            'bz': [1.0, 1.5],
            'theta': [0.5, 0.6],
            'width': 200,
            'height': 150,
            'max_iter': 64
        }
        response = client.post('/api/integrate',
                               data=json.dumps(params),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'results' in data


class TestQuantumAPI:
    """Test quantum properties API endpoints"""
    
    def test_quantum_properties_default(self, client):
        """Test quantum properties calculation with defaults"""
        response = client.post('/api/quantum_properties',
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'quantum_coupling' in data
        assert 'entanglement_strength' in data
        assert 'fractal_dimension' in data
    
    def test_quantum_properties_custom(self, client):
        """Test quantum properties with custom parameters"""
        params = {
            'fractal_dim': 1.8,
            'separation': 1e-10,
            'mass_set': 1e11,
            'mass_universe': 1e54
        }
        response = client.post('/api/quantum_properties',
                               data=json.dumps(params),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['fractal_dimension'] == 1.8
    
    def test_dark_matter_detection_default(self, client):
        """Test dark matter detection probability with defaults"""
        response = client.post('/api/dark_matter',
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'detection_probability' in data
        assert 'parameters' in data
    
    def test_dark_matter_detection_custom(self, client):
        """Test dark matter detection with custom parameters"""
        params = {
            'sigma_detect': 1e-46,
            'sigma_total': 1e-41,
            'delta': 0.3,
            'delta_max': 0.9
        }
        response = client.post('/api/dark_matter',
                               data=json.dumps(params),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['detection_probability'], float)


class TestFullIntegration:
    """Test full system integration"""
    
    def test_complete_workflow(self, client):
        """Test complete workflow: generate fractal, calculate properties"""
        # Step 1: Generate Mandelbrot fractal
        mandelbrot_response = client.post('/api/mandelbrot',
                                          data=json.dumps({'width': 200, 'height': 150}),
                                          content_type='application/json')
        assert mandelbrot_response.status_code == 200
        mandelbrot_data = json.loads(mandelbrot_response.data)
        fractal_dim = mandelbrot_data['fractal_dimension']
        
        # Step 2: Calculate quantum properties using fractal dimension
        quantum_response = client.post('/api/quantum_properties',
                                       data=json.dumps({'fractal_dim': fractal_dim}),
                                       content_type='application/json')
        assert quantum_response.status_code == 200
        quantum_data = json.loads(quantum_response.data)
        assert quantum_data['success'] is True
        
        # Step 3: Calculate dark matter detection
        dm_response = client.post('/api/dark_matter',
                                  data=json.dumps({}),
                                  content_type='application/json')
        assert dm_response.status_code == 200
        dm_data = json.loads(dm_response.data)
        assert dm_data['success'] is True
        
        print("✅ Complete workflow test passed!")
        print(f"   Fractal Dimension: {fractal_dim}")
        print(f"   Quantum Coupling: {quantum_data['quantum_coupling']}")
        print(f"   Dark Matter P_detect: {dm_data['detection_probability']}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

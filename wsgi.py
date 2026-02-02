"""
WSGI Entry Point for Production Deployment
Quantum Magnetic Field Calculator with Mandelbrot Fractal Analysis

Copyright (c) 2026 Tony Ray Macier III
Licensed under the MIT License - see LICENSE file for details

Author: Tony Ray Macier III
GitHub: @XxxGHOSTX
Project: Quantum Magnetic Field Calculator with Mandelbrot Fractal Analysis

Usage:
    gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 wsgi:app
"""

from web_app import app

if __name__ == "__main__":
    app.run()

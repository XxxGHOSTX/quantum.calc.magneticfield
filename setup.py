"""
Setup script for Quantum Magnetic Field Calculator

Copyright (c) 2026 Tony Ray Macier III
Licensed under the MIT License - see LICENSE file for details

Author: Tony Ray Macier III
GitHub: @XxxGHOSTX
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="quantum-calc-magneticfield",
    version="1.0.0",
    author="Tony Ray Macier III",
    author_email="",
    description="Quantum Magnetic Field Calculator with Mandelbrot Fractal Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XxxGHOSTX/quantum.calc.magneticfield",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=7.0.0", "pytest-cov>=3.0.0", "flake8>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "quantum-calc=web_app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

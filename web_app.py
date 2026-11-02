"""
Interactive Web Application for Mandelbrot Fractal and Magnetic Field Visualization.
The HTTP interface is a local development tool. Numerical requests are bounded
before reaching computational routines to prevent accidental or hostile resource
exhaustion.
"""
from flask import Flask, render_template, jsonify, request, redirect
import ipaddress
import math
import os
import numpy as np
from mandelbrot_fractal import MandelbrotSet, integrate_mandelbrot_xpoint
from x_point import x_point
from advanced_quantum_equations import (
    BlackHoleThermodynamics, QuantumErrorCorrection,
    QuantumSensingFramework, MultiverseQuantumCoupling
)

HOST = os.getenv("QUANTUM_WEB_HOST", "127.0.0.1").strip() or "127.0.0.1"
PORT = int(os.getenv("QUANTUM_WEB_PORT", "5000"))
_ALLOWED_HOSTS = {"127.0.0.1", "localhost", "::1", f"127.0.0.1:{PORT}", f"localhost:{PORT}", f"[::1]:{PORT}"}
_ALLOWED_ORIGINS = {f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}", f"http://[::1]:{PORT}"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 256 * 1024


@app.before_request
def restrict_api_to_local_clients():
    """Keep calculator APIs local even when an accidental non-local bind is configured."""
    try:
        if not ipaddress.ip_address(request.remote_addr or "").is_loopback:
            return jsonify({"success": False, "error": "API access is restricted to local clients."}), 403
    except ValueError:
        return jsonify({"success": False, "error": "API access is restricted to local clients."}), 403

    if request.host.lower() not in _ALLOWED_HOSTS:
        return jsonify({"success": False, "error": "Untrusted local Host header."}), 403

    origin = request.headers.get("Origin")
    if origin and origin.rstrip("/") not in _ALLOWED_ORIGINS:
        return jsonify({"success": False, "error": "Untrusted browser Origin."}), 403

    return None


def _json_object():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("A JSON object request body is required.")
    return data


def _bounded_int(data, key, default, minimum, maximum):
    value = data.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer.")
    if not minimum <= value <= maximum:
        raise ValueError(f"{key} must be between {minimum} and {maximum}.")
    return value


def _finite_number(data, key, default, minimum=None, maximum=None):
    value = data.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{key} must be a finite number.")
    value = float(value)
    if minimum is not None and value < minimum:
        raise ValueError(f"{key} must be at least {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"{key} must be at most {maximum}.")
    return value


def _finite_array(data, key, maximum_length=4096):
    values = data.get(key, [])
    if not isinstance(values, list) or not values:
        raise ValueError(f"{key} must be a non-empty JSON array.")
    if len(values) > maximum_length:
        raise ValueError(f"{key} may contain at most {maximum_length} values.")
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for value in values
    ):
        raise ValueError(f"{key} must contain only finite numbers.")
    return np.asarray(values, dtype=float)


def _validate_fractal_budget(width, height, max_iter):
    if width * height * max_iter > 150_000_000:
        raise ValueError("Requested fractal workload exceeds the 150-million pixel-iteration limit.")


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
    """Generate bounded Mandelbrot set data."""
    try:
        data = _json_object()
        width = _bounded_int(data, "width", 800, 16, 1024)
        height = _bounded_int(data, "height", 600, 16, 1024)
        max_iter = _bounded_int(data, "max_iter", 256, 8, 4096)
        _validate_fractal_budget(width, height, max_iter)

        xmin = _finite_number(data, "xmin", -2.5, -4.0, 4.0)
        xmax = _finite_number(data, "xmax", 1.0, -4.0, 4.0)
        ymin = _finite_number(data, "ymin", -1.25, -4.0, 4.0)
        ymax = _finite_number(data, "ymax", 1.25, -4.0, 4.0)
        if xmin >= xmax or ymin >= ymax:
            raise ValueError("Fractal bounds must be increasing (min less than max).")

        mandelbrot = MandelbrotSet(width=width, height=height, max_iter=max_iter)
        fractal_data = mandelbrot.generate_mandelbrot(xmin, xmax, ymin, ymax)
        fractal_dim = mandelbrot.fractal_dimension(fractal_data)

        return jsonify({
            "success": True,
            "data": fractal_data.tolist(),
            "fractal_dimension": fractal_dim,
            "width": width,
            "height": height,
            "bounds": {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax},
        })
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception("Mandelbrot generation failed.")
        return jsonify({"success": False, "error": "Mandelbrot calculation failed."}), 500


@app.route('/api/xpoint', methods=['POST'])
def calculate_xpoint():
    """Calculate magnetic x-points from bounded finite arrays."""
    try:
        data = _json_object()
        by = _finite_array(data, "by")
        bz = _finite_array(data, "bz")
        theta = _finite_array(data, "theta")
        if not (len(by) == len(bz) == len(theta)):
            raise ValueError("by, bz, and theta arrays must have equal lengths.")

        x_points = x_point(by, bz, theta)
        return jsonify({"success": True, "x_points": x_points.tolist(), "count": len(x_points)})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception("X-point calculation failed.")
        return jsonify({"success": False, "error": "X-point calculation failed."}), 500


@app.route('/api/integrate', methods=['POST'])
def integrate_calculations():
    """Integrate bounded Mandelbrot and x-point calculations."""
    try:
        data = _json_object()
        by = _finite_array(data, "by")
        bz = _finite_array(data, "bz")
        theta = _finite_array(data, "theta")
        if not (len(by) == len(bz) == len(theta)):
            raise ValueError("by, bz, and theta arrays must have equal lengths.")

        width = _bounded_int(data, "width", 400, 16, 1024)
        height = _bounded_int(data, "height", 300, 16, 1024)
        max_iter = _bounded_int(data, "max_iter", 128, 8, 4096)
        _validate_fractal_budget(width, height, max_iter)

        mandelbrot = MandelbrotSet(width=width, height=height, max_iter=max_iter)
        results_df = integrate_mandelbrot_xpoint(by, bz, theta, mandelbrot)
        return jsonify({"success": True, "results": results_df.to_dict(orient="records")})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception("Integrated calculation failed.")
        return jsonify({"success": False, "error": "Integrated calculation failed."}), 500


@app.route('/api/quantum_properties', methods=['POST'])
def quantum_properties():
    """Calculate finite, bounded quantum-property estimates."""
    try:
        data = _json_object()
        fractal_dim = _finite_number(data, "fractal_dim", 1.5, 0.0, 3.0)
        separation = _finite_number(data, "separation", 1e-9, 0.0, 1e100)
        if separation == 0:
            raise ValueError("separation must be greater than zero.")
        mass_set = _finite_number(data, "mass_set", 1e10, 0.0, 1e100)
        mass_universe = _finite_number(data, "mass_universe", 1e53, 0.0, 1e100)
        if mass_set == 0 or mass_universe == 0:
            raise ValueError("mass_set and mass_universe must be greater than zero.")

        mandelbrot = MandelbrotSet()
        coupling = mandelbrot.quantum_coupling_strength(fractal_dim, mass_set, mass_universe)
        entanglement = mandelbrot.quantum_entanglement_strength(separation, fractal_dim, mass_set, mass_universe)
        return jsonify({
            "success": True,
            "quantum_coupling": coupling,
            "entanglement_strength": entanglement,
            "fractal_dimension": fractal_dim,
        })
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception("Quantum-property calculation failed.")
        return jsonify({"success": False, "error": "Quantum-property calculation failed."}), 500


@app.route('/api/dark_matter', methods=['POST'])
def dark_matter_detection():
    """Calculate bounded dark-matter detection probability parameters."""
    try:
        data = _json_object()
        sigma_detect = _finite_number(data, "sigma_detect", 1e-45, 0.0, 1e100)
        sigma_total = _finite_number(data, "sigma_total", 1e-40, 0.0, 1e100)
        delta = _finite_number(data, "delta", 0.5, 0.0, 1e100)
        delta_max = _finite_number(data, "delta_max", 1.0, 0.0, 1e100)
        if sigma_total == 0 or delta_max == 0:
            raise ValueError("sigma_total and delta_max must be greater than zero.")
        if delta > delta_max:
            raise ValueError("delta must not exceed delta_max.")

        mandelbrot = MandelbrotSet()
        p_detect = mandelbrot.dark_matter_detection_probability(
            sigma_detect, sigma_total, delta, delta_max
        )
        return jsonify({
            "success": True,
            "detection_probability": p_detect,
            "parameters": {
                "sigma_detect": sigma_detect,
                "sigma_total": sigma_total,
                "delta": delta,
                "delta_max": delta_max,
            },
        })
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception("Dark-matter estimate failed.")
        return jsonify({"success": False, "error": "Dark-matter estimate failed."}), 500


if __name__ == '__main__':
    try:
        bind_ip = ipaddress.ip_address(HOST)
    except ValueError as exc:
        raise SystemExit("QUANTUM_WEB_HOST must be a literal loopback IP address.") from exc
    if not bind_ip.is_loopback:
        raise SystemExit("The quantum web application is local-only and cannot bind to a non-loopback address.")

    print("=" * 60)
    print("Starting Quantum Magnetic Field Fractal Web Application")
    print("=" * 60)
    print(f"2D Visualization: http://{HOST}:{PORT}")
    print(f"3D Advanced View: http://{HOST}:{PORT}/3d")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=False, host=HOST, port=PORT)

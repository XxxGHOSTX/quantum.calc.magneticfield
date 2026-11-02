import unittest

import web_app


class QuantumWebSecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = web_app.app.test_client()

    def test_api_rejects_non_loopback_clients(self):
        response = self.client.post(
            "/api/quantum_properties",
            json={},
            environ_overrides={"REMOTE_ADDR": "203.0.113.10"},
        )
        self.assertEqual(response.status_code, 403)

    def test_api_rejects_dns_rebinding_host(self):
        response = self.client.post(
            "/api/quantum_properties",
            json={},
            base_url="http://attacker.example",
            headers={"Origin": "http://attacker.example"},
        )
        self.assertEqual(response.status_code, 403)

    def test_api_rejects_untrusted_origin(self):
        response = self.client.post(
            "/api/quantum_properties",
            json={},
            headers={"Origin": "https://attacker.example"},
        )
        self.assertEqual(response.status_code, 403)

    def test_mandelbrot_rejects_oversized_dimensions(self):
        response = self.client.post(
            "/api/mandelbrot",
            json={"width": 100000, "height": 600, "max_iter": 256},
        )
        self.assertEqual(response.status_code, 400)

    def test_mandelbrot_rejects_excessive_iteration_budget(self):
        response = self.client.post(
            "/api/mandelbrot",
            json={"width": 1024, "height": 1024, "max_iter": 4096},
        )
        self.assertEqual(response.status_code, 400)

    def test_mandelbrot_rejects_non_finite_bounds(self):
        response = self.client.post(
            "/api/mandelbrot",
            json={"xmin": float("nan")},
        )
        self.assertEqual(response.status_code, 400)

    def test_xpoint_rejects_mismatched_array_lengths(self):
        response = self.client.post(
            "/api/xpoint",
            json={"by": [1, 2], "bz": [1], "theta": [0, 1]},
        )
        self.assertEqual(response.status_code, 400)

    def test_integrate_rejects_oversized_arrays(self):
        data = {"by": [0.1] * 4097, "bz": [0.2] * 4097, "theta": [0.3] * 4097}
        response = self.client.post("/api/integrate", json=data)
        self.assertEqual(response.status_code, 400)

    def test_quantum_properties_rejects_zero_separation(self):
        response = self.client.post(
            "/api/quantum_properties",
            json={"separation": 0},
        )
        self.assertEqual(response.status_code, 400)

    def test_dark_matter_rejects_delta_above_maximum(self):
        response = self.client.post(
            "/api/dark_matter",
            json={"delta": 2, "delta_max": 1},
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()

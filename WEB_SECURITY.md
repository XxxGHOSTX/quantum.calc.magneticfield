# Web Application Security

The Flask visualization app is a local development interface. It binds to a literal loopback IP address only and refuses to start on a non-loopback address. Flask debug mode is disabled.

Every `/api/*` route checks the source IP, exact local Host, and optional Origin. Requests from remote clients, unapproved Host headers, and foreign Origins are rejected. JSON request bodies are capped at 256 KiB.

Numerical requests are bounded before computation: Mandelbrot dimensions and iteration counts are capped, pixel-iteration work has a hard budget, numeric values must be finite and within defined limits, and input arrays have equal-length and 4,096-element limits. Invalid inputs return HTTP 400; unexpected calculation errors are logged server-side and return a generic HTTP 500.

Run tests with:

```bash
python -m unittest discover -s tests -p 'test_web_security.py' -v
```

This is a local-only development server, not a remote or production API. A remote deployment would require a separately reviewed authenticated gateway, TLS, resource quotas, monitoring, and network policy.

# Deployment Guide
## Quantum Magnetic Field Calculator with Mandelbrot Fractal Analysis

**Copyright © 2026 Tony Ray Macier III** | Licensed under MIT License

---

## Table of Contents
1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Configuration](#configuration)
6. [Security](#security)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Local Development

### Requirements
- Python 3.7 or higher
- pip or conda package manager
- 4GB RAM minimum (8GB recommended)
- 1GB free disk space

### Setup
```bash
# Clone repository
git clone https://github.com/XxxGHOSTX/quantum.calc.magneticfield.git
cd quantum.calc.magneticfield

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest -v
python smoke_test.py

# Start development server
python web_app.py
```

Access at: http://localhost:5000

### Development Mode
The Flask app runs in debug mode by default for development:
```python
# web_app.py (current configuration)
app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## Production Deployment

### Using Gunicorn (Recommended)

#### 1. Install Gunicorn
```bash
pip install gunicorn
```

#### 2. Create WSGI Entry Point
Create `wsgi.py`:
```python
"""
WSGI entry point for production deployment
"""
from web_app import app

if __name__ == "__main__":
    app.run()
```

#### 3. Run with Gunicorn
```bash
# Basic usage
gunicorn --bind 0.0.0.0:5000 wsgi:app

# Production configuration
gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    --access-logfile /var/log/quantum_calc/access.log \
    --error-logfile /var/log/quantum_calc/error.log \
    wsgi:app
```

#### 4. Create Systemd Service
Create `/etc/systemd/system/quantum-calc.service`:
```ini
[Unit]
Description=Quantum Magnetic Field Calculator
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/quantum.calc.magneticfield
Environment="PATH=/opt/quantum.calc.magneticfield/venv/bin"
ExecStart=/opt/quantum.calc.magneticfield/venv/bin/gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    wsgi:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable quantum-calc
sudo systemctl start quantum-calc
sudo systemctl status quantum-calc
```

### Using uWSGI

#### 1. Install uWSGI
```bash
pip install uwsgi
```

#### 2. Create uWSGI Configuration
Create `uwsgi.ini`:
```ini
[uwsgi]
module = wsgi:app
master = true
processes = 4
threads = 2
socket = /tmp/quantum-calc.sock
chmod-socket = 660
vacuum = true
die-on-term = true
```

#### 3. Run uWSGI
```bash
uwsgi --ini uwsgi.ini
```

### Nginx Reverse Proxy

#### 1. Install Nginx
```bash
sudo apt update
sudo apt install nginx
```

#### 2. Configure Nginx
Create `/etc/nginx/sites-available/quantum-calc`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Increase timeout for fractal generation
    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (if needed)
    location /static {
        alias /opt/quantum.calc.magneticfield/static;
        expires 30d;
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/quantum-calc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 3. SSL/TLS with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Docker Deployment

### Create Dockerfile
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application files
COPY . .

# Create non-root user
RUN useradd -m -u 1000 quantum && chown -R quantum:quantum /app
USER quantum

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]
```

### Create docker-compose.yml
```yaml
version: '3.8'

services:
  quantum-calc:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Build and Run
```bash
# Build image
docker build -t quantum-calc .

# Run container
docker run -d -p 5000:5000 --name quantum-calc quantum-calc

# Or use docker-compose
docker-compose up -d

# View logs
docker logs -f quantum-calc

# Stop
docker stop quantum-calc
```

---

## Cloud Deployment

### AWS Elastic Beanstalk

#### 1. Install EB CLI
```bash
pip install awsebcli
```

#### 2. Initialize EB
```bash
eb init -p python-3.10 quantum-calc
```

#### 3. Create `.ebextensions/python.config`
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: wsgi:app
  aws:elasticbeanstalk:environment:proxy:
    ProxyServer: nginx
```

#### 4. Deploy
```bash
eb create quantum-calc-env
eb open
```

### Heroku

#### 1. Create Procfile
```
web: gunicorn wsgi:app
```

#### 2. Create runtime.txt
```
python-3.10.8
```

#### 3. Deploy
```bash
heroku create quantum-calc-app
git push heroku main
heroku open
```

### Google Cloud Run

#### 1. Create Dockerfile (see Docker section above)

#### 2. Build and Push
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/quantum-calc
```

#### 3. Deploy
```bash
gcloud run deploy quantum-calc \
  --image gcr.io/PROJECT_ID/quantum-calc \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300
```

### DigitalOcean App Platform

#### 1. Create .do/app.yaml
```yaml
name: quantum-calc
services:
- name: web
  github:
    repo: XxxGHOSTX/quantum.calc.magneticfield
    branch: main
  run_command: gunicorn --bind :8080 wsgi:app
  http_port: 8080
  instance_count: 1
  instance_size_slug: basic-xxs
```

#### 2. Deploy via UI
- Connect GitHub repository
- Configure settings
- Deploy

---

## Configuration

### Environment Variables
Create `.env` file:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=104857600  # 100MB
REQUEST_TIMEOUT=300  # 5 minutes
```

### Load in Application
```python
# web_app.py
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 104857600))
```

### Production Settings
```python
# config.py
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Performance
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
```

---

## Security

### 1. Enable HTTPS
Always use HTTPS in production:
```bash
# Let's Encrypt (recommended)
sudo certbot --nginx

# Or use your SSL certificate
```

### 2. Add Security Headers
Update Nginx configuration:
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

### 3. Rate Limiting
Install Flask-Limiter:
```bash
pip install Flask-Limiter
```

Add to web_app.py:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/mandelbrot', methods=['POST'])
@limiter.limit("10 per minute")
def generate_mandelbrot():
    # ...
```

### 4. CORS (if needed)
```bash
pip install flask-cors
```

```python
from flask_cors import CORS

CORS(app, origins=["https://your-frontend-domain.com"])
```

### 5. Input Validation
Always validate user input:
```python
from flask import request, abort

@app.route('/api/mandelbrot', methods=['POST'])
def generate_mandelbrot():
    data = request.get_json()
    
    # Validate width and height
    width = data.get('width', 800)
    height = data.get('height', 600)
    
    if not (100 <= width <= 2000) or not (100 <= height <= 2000):
        abort(400, "Invalid dimensions")
    
    # ...
```

---

## Monitoring

### 1. Application Logging
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/quantum_calc.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Quantum Calculator startup')
```

### 2. Performance Monitoring
Use monitoring services:
- **New Relic**: Application performance monitoring
- **Datadog**: Infrastructure and application monitoring
- **Sentry**: Error tracking and monitoring

Example with Sentry:
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### 3. Health Check Endpoint
Add to web_app.py:
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })
```

---

## Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
python web_app.py --port 5001
```

### Issue: Out of Memory
```bash
# Increase worker timeout
gunicorn --timeout 300 wsgi:app

# Reduce max iterations
# In web_app.py, add validation:
max_iter = min(data.get('max_iter', 256), 512)
```

### Issue: Slow Response Times
```bash
# Add caching
pip install Flask-Caching

# Configure Redis cache
CACHE_TYPE = "RedisCache"
CACHE_REDIS_HOST = "localhost"
CACHE_REDIS_PORT = 6379
```

### Issue: Database Connection Errors
Not applicable (application doesn't use database)

### Issue: SSL Certificate Errors
```bash
# Renew Let's Encrypt certificate
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

---

## Maintenance

### Backup
```bash
# Backup data files
tar -czf backup-$(date +%Y%m%d).tar.gz \
    solar_corona_magnetic_field.csv \
    integrated_quantum_results.csv \
    quantum_analysis_results.json

# Upload to S3 (example)
aws s3 cp backup-$(date +%Y%m%d).tar.gz s3://your-bucket/backups/
```

### Updates
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests
python -m pytest -v

# Restart service
sudo systemctl restart quantum-calc
```

### Database (Future Enhancement)
If adding database support:
```bash
# Install PostgreSQL
pip install psycopg2-binary

# Run migrations
flask db upgrade
```

---

## Performance Optimization

### 1. Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/mandelbrot', methods=['POST'])
@cache.cached(timeout=3600, query_string=True)
def generate_mandelbrot():
    # ...
```

### 2. Async Processing
For long-running tasks:
```bash
pip install celery redis
```

### 3. CDN for Static Files
Use CDN for templates and static assets:
- CloudFlare
- AWS CloudFront
- Google Cloud CDN

---

## Support

For deployment issues:
- **GitHub Issues**: https://github.com/XxxGHOSTX/quantum.calc.magneticfield/issues
- **Documentation**: See README.md and API_DOCUMENTATION.md

---

**Copyright © 2026 Tony Ray Macier III | MIT License | Attribution Required**

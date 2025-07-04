# 📊 Observability in Python with Prometheus and Grafana

This project demonstrates how to add **observability** to a Python application using **Prometheus** and **Grafana**. You'll learn how to expose metrics in a Flask app, collect them with Prometheus, and visualize them in Grafana dashboards.

---

## 🔧 Requirements

- Python 3.7+
- pip
- Prometheus (installed locally)
- Grafana (installed locally)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/python-observability-example.git
cd python-observability-example
```

### 2. Install Dependencies

```bash
pip install flask prometheus_client
```

### 3. Run the Flask App

```bash
python app.py
```

This starts your Flask app on:

- `http://localhost:5000` → base route
- `http://localhost:5000/metrics` → metrics endpoint (used by Prometheus)

---

### 4. Configure Prometheus

Create a file named `prometheus.yml` and include the following configuration:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'python_app'
    static_configs:
      - targets: ['localhost:5000']
```

Run Prometheus using the downloaded binary:

```bash
prometheus --config.file=prometheus.yml
```

Then open Prometheus UI in your browser:

```
http://localhost:9090
```

---

### 5. Set Up Grafana

1. Download and install Grafana from the [official website](https://grafana.com/grafana/download).
2. Launch Grafana and open in your browser:  
   `http://localhost:3000`
3. Log in (default user: `admin`, password: `admin`).
4. Add **Prometheus** as a new data source (Settings → Data Sources → Add).
5. Create a new dashboard:
   - **Panel 1:** visualize `http_requests_total` metric
   - **Panel 2:** visualize `http_request_duration_seconds` metric

These panels will show real-time request count and response latency.

---

## 🐍 Sample Flask App (`app.py`)

```python
from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'Request latency',
    ['method', 'endpoint']
)

@app.route('/')
def home():
    start_time = time.time()
    time.sleep(0.2)  # Simulate work
    latency = time.time() - start_time
    status_code = 200

    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=status_code).inc()
    REQUEST_LATENCY.labels(method='GET', endpoint='/').observe(latency)

    return "Hello from Flask!", status_code

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 📈 Metrics Tracked

- `http_requests_total`: Number of HTTP requests received.
- `http_request_duration_seconds`: Latency of each request.

---

## ✅ Result

With everything running, you'll have a live dashboard showing:

- Request rate and total count
- Request latency in seconds
- Insights into how your Python app behaves over time

---

## 📂 File Structure

```
.
├── app.py
├── prometheus.yml
└── README.md
```

---

## 📌 License

MIT License

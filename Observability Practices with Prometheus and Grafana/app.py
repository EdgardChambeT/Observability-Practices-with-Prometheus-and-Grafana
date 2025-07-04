from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Definir métricas
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total de peticiones HTTP',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'Duración de las peticiones HTTP',
    ['method', 'endpoint']
)

@app.route('/')
def home():
    start_time = time.time()
    
    # Simular carga
    time.sleep(0.2)
    
    latency = time.time() - start_time
    status_code = 200

    # Actualizar métricas
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=status_code).inc()
    REQUEST_LATENCY.labels(method='GET', endpoint='/').observe(latency)

    return "¡Hola desde Flask!", status_code

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

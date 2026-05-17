from flask import Flask, jsonify, request
import time
import random
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# --- Prometheus метрики ---
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Всего запросов',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Задержка запросов',
    ['endpoint']
)

ACTIVE_USERS = Gauge(
    'app_active_users',
    'Количество активных пользователей'
)

# Простая "база данных" в памяти
tasks = []
task_id_counter = 1


@app.before_request
def before_request():
    request.start_time = time.time()
    ACTIVE_USERS.set(random.randint(1, 50))  # симуляция пользователей


@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    return response


# --- API эндпоинты ---

@app.route('/')
def index():
    return jsonify({
        "app": "DevOps Practice App",
        "version": "1.0.0",
        "endpoints": ["/tasks", "/health", "/metrics"]
    })


@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200


@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks, "count": len(tasks)})


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Поле 'title' обязательно"}), 400

    task = {
        "id": task_id_counter,
        "title": data["title"],
        "done": False
    }
    tasks.append(task)
    task_id_counter += 1
    return jsonify(task), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Задача не найдена"}), 404
    task["done"] = True
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Удалено"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
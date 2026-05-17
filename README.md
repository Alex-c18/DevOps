[README.md](https://github.com/user-attachments/files/27804332/README.md)
<div align="center">

# 🚀 DevOps Practice Project

**Учебный проект для практики DevOps-инструментов**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-minikube-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![Prometheus](https://img.shields.io/badge/Prometheus-metrics-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)](https://prometheus.io)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://terraform.io)

<br/>

> Простое Flask REST API (список задач) с полным DevOps-стеком:
> контейнеризация, оркестрация, мониторинг и инфраструктура как код.

</div>

---

## 📋 Содержание

- [Стек](#-стек)
- [Структура проекта](#-структура-проекта)
- [Быстрый старт](#-быстрый-старт)
- [API](#-api)
- [Docker](#-docker)
- [Kubernetes](#-kubernetes)
- [Мониторинг](#-мониторинг)
- [Terraform IaC](#-terraform-iac)

---

## 🛠 Стек

| Слой | Инструмент | Версия |
|:---|:---|:---:|
| 🐍 Приложение | Python + Flask | 3.12 / 3.0 |
| 🐳 Контейнеры | Docker + Compose | latest |
| ☸️ Оркестрация | Kubernetes (minikube) | latest |
| 📈 Метрики | Prometheus | latest |
| 📊 Мониторинг | Netdata | latest |
| 🏗 IaC | Terraform | ~1.x |

---

## 📁 Структура проекта

```
devops-practice/
├── 🐍 app.py                # Flask-приложение (REST API)
├── 📦 requirements.txt      # Python-зависимости
├── 🐳 Dockerfile            # Образ приложения
├── 🗂  docker-compose.yml   # Стек: app + Prometheus + Netdata
├── ⚙️  prometheus.yml       # Конфиг скрейпинга Prometheus
├── ☸️  k8s-manifests.yaml   # Kubernetes: Deployment + Service
├── 🏗  main.tf              # Terraform IaC конфигурация
└── 📖 README.md
```

---

## ⚡ Быстрый старт

### Вариант 1 — Локально

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Вариант 2 — Docker Compose ✅ рекомендуется

```bash
docker compose up -d
```

После запуска доступны:

| Сервис | URL | Описание |
|:---|:---|:---|
| 🐍 Приложение | http://localhost:5000 | REST API |
| 📈 Prometheus | http://localhost:9090 | Метрики |
| 📊 Netdata | http://localhost:19999 | Мониторинг |

---

## 🔌 API

### Эндпоинты

| Метод | Путь | Описание |
|:---:|:---|:---|
| `GET` | `/` | Информация о приложении |
| `GET` | `/health` | Healthcheck |
| `GET` | `/metrics` | Метрики Prometheus |
| `GET` | `/tasks` | Список задач |
| `POST` | `/tasks` | Создать задачу |
| `PUT` | `/tasks/:id` | Отметить выполненной |
| `DELETE` | `/tasks/:id` | Удалить задачу |

### Примеры

```bash
# ➕ Создать задачу
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Изучить Docker"}'

# 📋 Список всех задач
curl http://localhost:5000/tasks

# ✅ Отметить выполненной
curl -X PUT http://localhost:5000/tasks/1

# 🗑 Удалить задачу
curl -X DELETE http://localhost:5000/tasks/1
```

<details>
<summary>📄 Пример ответа</summary>

```json
{
  "tasks": [
    { "id": 1, "title": "Изучить Docker", "done": true },
    { "id": 2, "title": "Настроить Kubernetes", "done": false }
  ],
  "count": 2
}
```

</details>

---

## 🐳 Docker

### Собрать и запустить образ

```bash
# Сборка
docker build -t devops-app:latest .

# Запуск
docker run -p 5000:5000 devops-app:latest
```

### Полезные команды

```bash
docker compose up -d          # Запустить весь стек в фоне
docker compose ps             # Статус сервисов
docker compose logs -f app    # Логи приложения в реальном времени
docker compose down           # Остановить (данные сохраняются)
docker compose down -v        # Остановить + удалить volumes
```

> **⚠️ Важно:** данные хранятся в памяти и сбрасываются при перезапуске контейнера.
> Это нормально для учебного проекта — в продакшене используют БД + volumes.

---

## ☸️ Kubernetes

> Требуется [minikube](https://minikube.sigs.k8s.io/docs/start/)

```bash
# 1. Запустить кластер
minikube start

# 2. Переключиться на Docker-демон внутри minikube
eval $(minikube docker-env)

# 3. Собрать образ внутри minikube
docker build -t devops-app:latest .

# 4. Задеплоить
kubectl apply -f k8s-manifests.yaml

# 5. Получить URL
minikube service devops-app-service --url
```

### Управление

```bash
kubectl get pods                                      # Список подов
kubectl describe pod <pod-name>                       # Детали пода
kubectl logs <pod-name>                               # Логи
kubectl scale deployment devops-app --replicas=4      # Масштабирование
kubectl rollout status deployment/devops-app          # Статус деплоя
kubectl rollout undo deployment/devops-app            # Откат
```

### Архитектура

```
┌─────────────────────────────────────┐
│           Kubernetes Cluster        │
│                                     │
│  ┌──────────┐    ┌──────────┐       │
│  │  Pod 1   │    │  Pod 2   │  ...  │
│  │ devops   │    │ devops   │       │
│  │  app     │    │  app     │       │
│  └────┬─────┘    └────┬─────┘       │
│       └───────┬────────┘            │
│         ┌─────┴──────┐              │
│         │  Service   │              │
│         │  NodePort  │              │
│         └─────┬──────┘              │
└───────────────┼─────────────────────┘
                │ :80 → :5000
              Клиент
```

---

## 📊 Мониторинг

### Метрики приложения

Приложение экспортирует метрики на `/metrics` в формате Prometheus:

| Метрика | Тип | Описание |
|:---|:---:|:---|
| `app_requests_total` | Counter | Всего запросов (по методу, пути, статусу) |
| `app_request_latency_seconds` | Histogram | Задержка запросов |
| `app_active_users` | Gauge | Активные пользователи |

### PromQL — полезные запросы

```promql
# Запросов в секунду
rate(app_requests_total[1m])

# 95-й перцентиль задержки
histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[5m]))

# Процент ошибок (4xx + 5xx)
sum(rate(app_requests_total{status=~"4..|5.."}[5m]))
  / sum(rate(app_requests_total[5m])) * 100

# Активные пользователи
app_active_users
```

### Генерация нагрузки для проверки метрик

```bash
for i in {1..50}; do
  curl -s http://localhost:5000/tasks > /dev/null
  curl -s -X POST http://localhost:5000/tasks \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Task $i\"}" > /dev/null
done
```

---

## 🏗 Terraform IaC

```bash
terraform init          # Инициализация (скачать провайдеры)
terraform plan          # Посмотреть что будет создано
terraform apply         # Применить конфигурацию
terraform show          # Текущее состояние
terraform destroy       # Удалить созданные ресурсы
```

### Переменные

```bash
# Переопределить без редактирования файла
terraform apply -var="replicas=3" -var="port=8080"
```

---

<div align="center">

Сделано для практики DevOps 🛠

</div>

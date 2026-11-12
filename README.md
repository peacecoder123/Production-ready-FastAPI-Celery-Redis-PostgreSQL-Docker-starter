# FastAPI + Celery + Docker Production Starter

> **Developer:** Radhe Wankhade · [@RadheWankhade01](https://x.com/RadheWankhade01) on X

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python) ![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-009688?logo=fastapi) ![Celery](https://img.shields.io/badge/Celery-5.4-37814A?logo=celery) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

A clean, production-ready backend starter combining **FastAPI (async)**, **Celery distributed workers**, **Redis broker**, **PostgreSQL database**, and **Docker Compose** with health checks, database seeding, and async testing out of the box.

---

## Architecture Overview

```
                      ┌──────────────────────┐
                      │    Client / UI       │
                      └──────────┬───────────┘
                                 │ HTTP requests
                                 ▼
                      ┌──────────────────────┐
                      │   FastAPI (api)      │
                      │  - REST Endpoints    │
                      │  - SQLAlchemy Async  │
                      └────┬────────────┬────┘
                           │            │
            Dispatches task│            │ Queries / Writes
                           ▼            ▼
         ┌───────────────────┐        ┌──────────────────────┐
         │   Redis (redis)   │        │ PostgreSQL (postgres)│
         │ - Message Broker  │        │ - Persistent Storage │
         └─────────┬─────────┘        └──────────────────────┘
                   │
                   ▼ Consumes tasks
         ┌───────────────────┐
         │ Celery (worker)   │
         │ - Long-running    │
         │   background jobs │
         └───────────────────┘
```

---

## Features

- **Asynchronous Architecture:** Full `async`/`await` support with SQLAlchemy 2.0 and `asyncpg`.
- **Distributed Tasks:** Celery workers backed by Redis for offloading heavy workloads.
- **Docker Compose Setup:** Multi-container stack (`api`, `worker`, `beat`, `postgres`, `redis`) with dependent health checks.
- **Database Migrations & Seeding:** Seed script (`scripts/seed.py`) runs both inside Docker and locally.
- **Zero-Docker Testing:** Uses in-memory SQLite (`sqlite+aiosqlite`) so test suites run in seconds without starting containers.
- **Agent Skill Ready:** Drop into `.agents/skills/fastapi-celery-docker-starter` for AI coding assistants.

---

## Quick Start

### 1. Run with Docker Compose

```bash
# Copy environment configuration
cp .env.example .env

# Build and start all 5 containers
docker compose up -d --build

# Run database seed inside the running API container
docker compose exec api python -m scripts.seed
```

Check the services:
- **Interactive API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check:** `curl http://localhost:8000/health`
- **System Status:** `curl http://localhost:8000/status`

---

### 2. Local Development (without Docker)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database seeding locally (creates local SQLite test.db)
python -m scripts.seed

# 3. Start FastAPI dev server
uvicorn app.main:app --reload --port 8000
```

---

## Service Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Liveness check (always returns `{"status": "ok"}`) |
| `GET` | `/status` | Subsystem status overview (`api`, `db`, `worker`) |
| `GET` | `/ready` | Readiness check verifying active database connection |
| `POST` | `/api/v1/items` | Create new item (`{"name": "...", "description": "..."}`) |
| `GET` | `/api/v1/items` | List items with pagination |
| `GET` | `/api/v1/items/{id}` | Get item details by ID |

---

## Celery Worker Usage

To queue a task from Python code:

```python
from app.workers.tasks import process_item

# Queues asynchronously in Redis
task = process_item.delay(42, {"priority": "high"})
print(f"Task ID: {task.id}")
```

Run the example trigger script:
```bash
python examples/trigger_task.py
```

---

## Running Tests

Tests run completely in-memory using `sqlite+aiosqlite` and `httpx`:

```bash
pytest -v
```

Expected output:
```
tests/test_health.py::test_health_check PASSED
tests/test_health.py::test_status_endpoint PASSED
tests/test_health.py::test_items_crud PASSED
```

---

## Project Structure

```
fastapi-celery-docker-starter/
├── app/
│   ├── api/v1/items.py         ← REST API endpoints
│   ├── models/item.py          ← SQLAlchemy declarative model
│   ├── schemas/item.py         ← Pydantic validation schemas
│   ├── workers/                ← Celery app & background tasks
│   │   ├── celery_app.py
│   │   └── tasks.py
│   ├── config.py               ← App settings & env loading
│   ├── database.py             ← Async engine & session management
│   └── main.py                 ← FastAPI entrypoint
├── scripts/
│   └── seed.py                 ← DB seeding script
├── tests/
│   ├── conftest.py             ← Pytest fixtures & SQLite mock engine
│   └── test_health.py          ← API endpoint unit & integration tests
├── examples/
│   └── trigger_task.py         ← Celery dispatch example
├── docker-compose.yml          ← 5-container orchestrated environment
├── Dockerfile                  ← Multi-stage lightweight image
├── requirements.txt            ← Pinned dependencies
├── SKILL.md                    ← Agent skill manifest
├── README.md                   ← Project documentation
└── LICENSE                     ← MIT
```

---

## 🔗 Connected Skills Ecosystem

This tool is part of a modular **Open-Source Content & Intelligence Pipeline**. Each tool works 100% standalone, or combines seamlessly with the others:

```
┌──────────────────────────────────────┐       ┌──────────────────────────────────────┐
│     Safe RSS News Ingestor           │       │       Trading Chart Exporter         │
│  (SSRF-safe news & feeds)            │       │   (High-res headless chart capture)  │
└──────────────────┬───────────────────┘       └──────────────────┬───────────────────┘
                   │                                              │
                   ▼                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          QC Tweet & Thread Composer                                 │
│         (Deterministic numeric grounding & anti-hallucination verification)         │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         Publishing Eligibility Gate                                 │
│            (DRAFT ➔ PENDING_REVIEW ➔ APPROVED ➔ PUBLISHED state machine)            │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            Zero-Cost X Publisher                                    │
│             (Web Intent + OS Clipboard PNG Ctrl+V @ $0 API cost)                    │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                           ▲
                                           │ Orchestrated by
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    FastAPI + Celery + Docker Starter                                │
│             (Production async backend, Redis task queue & PostgreSQL)               │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

| Pipeline Stage | Repository | Purpose |
|---|---|---|
| **1. News Ingestion** | [📰 safe-rss-news-ingestor](https://github.com/peacecoder123/A-production-safe-RSS-Atom-news-aggregator) | Hardened RSS/Atom aggregator that prevents SSRF attacks and strips junk HTML |
| **2. Chart Visuals** | [📊 trading-chart-exporter](https://github.com/peacecoder123/Trading-chart-exporter-Trading-view-alternative-Skill-) | Headless Playwright exporter for TradingView charts & financial visuals |
| **3. AI Content QC** | [✍️ qc-tweet-composer](https://github.com/peacecoder123/Quality-Control-gate-for-AI-drafted-tweets-threads-Ai-Skill-) | Fact-checks AI post drafts against sources, catches fake metrics & splits threads |
| **4. Editorial Gate** | [🚦 publishing-eligibility-gate](https://github.com/peacecoder123/publishing-eligibility-gate) | Content review state machine with audit history preventing unapproved releases |
| **5. $0 Distribution** | [🚀 zero-cost-x-publisher](https://github.com/peacecoder123/zero-cost-X-Twitter-publisher) | Publishes text + image to X at $0 cost via web intent + clipboard Ctrl+V |
| **6. Backend Engine** | [⚡ fastapi-celery-docker-starter](https://github.com/peacecoder123/Production-ready-FastAPI-Celery-Redis-PostgreSQL-Docker-starter) *(This repo)* | Production async backend stack with Celery workers, Redis, and PostgreSQL |

---

## License

MIT — Created by [Radhe Wankhade](https://x.com/RadheWankhade01).


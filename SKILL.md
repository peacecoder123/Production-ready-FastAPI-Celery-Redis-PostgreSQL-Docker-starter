---
name: fastapi-celery-docker-starter
description: >-
  Production-grade template for building scalable backend applications using FastAPI, Celery,
  Redis, PostgreSQL, and Docker Compose with health checks, database seeding, and async testing.
author: "Radhe Wankhade (@RadheWankhade01)"
x_profile: "https://x.com/RadheWankhade01"
---

# FastAPI + Celery + Docker Production Starter

A modern, production-hardened template for asynchronous web applications and distributed background job processing.

## Architecture

- **FastAPI**: High performance async REST API with automatic Swagger docs.
- **Celery**: Distributed task queue handling long-running background tasks.
- **Redis**: In-memory message broker and task result backend.
- **PostgreSQL**: Robust relational database using SQLAlchemy 2.0 async engine.
- **Docker Compose**: Containerized multi-service setup with dependency health checks.

## When to Use This Skill
- You need to scaffold a new backend service that requires both synchronous API endpoints and asynchronous background workers.
- You want clean Docker Compose orchestration with PostgreSQL and Redis health checks already wired.
- You want an established pattern for DB seeding and in-memory test isolation.

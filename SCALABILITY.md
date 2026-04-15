# Technical Scalability Note

This document outlines how the current Notes API can be scaled to support millions of users and high request volumes.

## 1. Architectural Scaling (Microservices)
Currently built as a monolith for simplicity, the application can be decomposed into microservices:
- **Auth Service**: Handles registration, login, and token validation.
- **Notes Service**: Handles CRUD operations for notes.
- **User Service**: Manages user profiles and permissions.
Benefit: Services can be scaled independently based on load (e.g., scaling the Notes service during peak activity while keeping Auth service smaller).

## 2. Database Scalability
- **Read/Write Splitting**: Use a Primary database for writes and multiple Read Replicas for high-volume GET requests.
- **Indexing**: Optimized indexes on `owner_id` and `id` ensure sub-millisecond query times.
- **Sharding**: Partitioning the `notes` table by `owner_id` across multiple database instances as the volume grows beyond the capacity of a single instance.

## 3. Caching (Redis)
- **Session Caching**: Store active JWT tokens and user metadata in Redis to avoid hitting the database on every authorized request.
- **Query Caching**: Cache frequently accessed lists of notes with an appropriate TTL (Time to Live) and invalidation on update/delete.

## 4. Load Balancing & Concurrency
- **Vertical Scaling**: Increasing CPU/RAM on a single server (limited ceiling).
- **Horizontal Scaling**: Deploying multiple instances of the FastAPI app behind a Load Balancer (Nginx/HAProxy) or an Orchestrator (Kubernetes).
- **Asynchronous Processing**: Using Task Queues (Celery/RabbitMQ) for non-blocking tasks like sending registration emails.

## 5. Deployment & Orchestration
- **Docker**: Ensures environment consistency across dev, staging, and production.
- **Kubernetes (K8s)**: Automatically manages scaling, health checks, and rollbacks.
- **CD/CI**: Automated pipelines to run tests and deploy to the cloud (AWS/GCP/Azure) upon every commit.

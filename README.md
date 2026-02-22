# 🏗️ Project Aether-SRE

**Objective:** Build a self-healing, local-first SRE agent that monitors, diagnoses, and repairs a Docker-based microservice cluster using a local LLM (Ollama).

## 🚀 Modules

### Module 1: The "Target & Trigger" (Infrastructure)
- **Chaos Service:** A Python app designed to fail (Memory Leaks, Crashes).
- **Prometheus:** Metrics collection.
- **Alertmanager:** Alert routing.
- **Docker Compose:** Orchestration.

## 🛠️ Setup

1. Ensure Docker Desktop is running.
2. Run the stack:
   ```bash
   docker-compose up --build -d
   ```
3. Trigger a failure:
   ```bash
   curl -X POST http://localhost:8080/stress
   ```
# 🏗️ Project Aether-SRE

**Objective:** A self-healing, local-first SRE agent that monitors, diagnoses, and repairs a Docker-based microservice cluster using an autonomous reasoning engine.

## 🚀 System Architecture

### 1. Monitoring Stack (The Eyes)
- **Prometheus:** Scrapes real-time metrics from services.
- **Alertmanager:** Routes firing alerts to the Agent Service.
- **Context Enrichment:** The agent automatically fetches container logs and resource metrics to provide deep diagnostic context.

### 2. Autonomous Agent (The Brain)
- **FastAPI Webhook:** Receives and validates incoming alerts.
- **Reasoning Engine:** Uses a ReAct (Reason + Act) loop to autonomously decide which tools to use for diagnosis.
- **LLM Integration:** Powered by Ollama (local-first) to analyze symptoms and recommend actions.

### 3. Self-Healing (The Hands)
- **Repair Engine:** Directly interacts with the Docker daemon to perform remediation.
- **Automated Actions:** Capable of autonomously restarting services, clearing caches, or resetting environments based on diagnostic findings.

## 🛠️ Setup & Usage

1.  **Prerequisites:**
    *   Docker Desktop
    *   Ollama (running `qwen2.5-coder:7b` or similar)

2.  **Spin up the Stack:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Trigger a Failure (Stress Test):**
    ```bash
    curl -X POST http://localhost:8080/stress
    ```

4.  **Monitor the Agent:**
    Watch the agent reason and repair the system in real-time:
    ```bash
    docker logs -f agent-service
    ```

## 📊 Outputs

For detailed examples of the agent's reasoning chains and JSON diagnoses, see [outputs.md](./outputs.md).

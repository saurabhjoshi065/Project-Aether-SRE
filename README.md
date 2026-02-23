# 🏗️ Project Aether-SRE

**Objective:** Build a self-healing, local-first SRE agent that monitors, diagnoses, and repairs a Docker-based microservice cluster using a local LLM (Ollama).

## 🚀 Modules

### Module 1: The "Target & Trigger" (Infrastructure)
- **Chaos Service:** A Python app designed to fail (Memory Leaks, Crashes).
- **Prometheus:** Metrics collection.
- **Alertmanager:** Alert routing.
- **Docker Compose:** Orchestration.

### Module 2: The "Ear" (Agent Service)
- **FastAPI Webhook:** Receives alerts from Alertmanager.
- **Pydantic Validation:** Ensures alert data integrity.
- **Structured Logging:** Prepares alert context for the LLM.

### Module 3: The "Brain" (Agent Service)
- **LangChain & Ollama:** Integrates with a local LLM for diagnosis.
- **Prompt Engineering:** Uses a system prompt to get structured JSON diagnoses.
- **Async & Fallback:** Ensures non-blocking operation and graceful degradation.

## 🛠️ Setup

1.  **Prerequisites:**
    *   Docker Desktop
    *   Python 3.11+
    *   Ollama running with a model (e.g., `llama2`)

2.  **Installation:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the service:**
    ```bash
    uvicorn main:app --reload
    ```
    The service will be available at `http://localhost:8000`.

4.  **Run the infrastructure stack:**
    ```bash
    docker-compose up --build -d
    ```

5.  **Trigger a failure:**
    ```bash
    curl -X POST http://localhost:8080/stress
    ```

## 📝 Usage

To send a test alert to the service, you can use `curl`:

```bash
curl -X POST http://localhost:8000/v1/alerts -H "Content-Type: application/json" -d @- << EOF
{
  "version": "4",
  "groupKey": "test",
  "status": "firing",
  "receiver": "test",
  "groupLabels": {},
  "commonLabels": {},
  "commonAnnotations": {},
  "externalURL": "http://alertmanager.example.com",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "TestAlert"
      },
      "annotations": {
        "summary": "This is a test alert."
      },
      "startsAt": "2024-01-01T00:00:00Z",
      "endsAt": "2024-01-01T01:00:00Z",
      "generatorURL": "http://prometheus.example.com",
      "fingerprint": "test"
    }
  ]
}
EOF
```
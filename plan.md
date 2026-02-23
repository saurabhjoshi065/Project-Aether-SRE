# 📅 Agent Service Development Plan

## Module 2: The Ear (Completed)

**Goal:** Build the "Ear" of the system—a FastAPI service that receives and validates alerts from Prometheus Alertmanager.

### Phase 1: Skeleton & Infrastructure
- [x] Create `requirements.txt` (FastAPI, Uvicorn, Pydantic).
- [x] Create `Dockerfile` (Python 3.11-slim).
- [x] Update root `docker-compose.yml` to include `agent-service`.

### Phase 2: The Webhook Listener
- [x] Create `main.py` with FastAPI app.
- [x] Implement `POST /v1/alerts` endpoint.
- [x] Define Pydantic models in `schemas.py` to validate Alertmanager payloads.

### Phase 3: Logging & Processing
- [x] Configure structured logging (JSON format preferred).
- [x] Parse the alert payload to extract: `alertname`, `instance`, `summary`, `severity`.
- [x] Log the parsed alert to stdout (so we can see it in `docker logs`).

## Module 3: The Brain (Completed)

**Goal:** Integrate a local LLM (Ollama) into the existing `agent_service` to diagnose alerts.

### Phase 1: LLM Integration
- [x] Add `langchain` and `langchain-ollama` to `requirements.txt`.
- [x] Create `llm.py` to encapsulate the LLM connection logic.
- [x] Integrate the LLM into the `/v1/alerts` endpoint in `main.py`.

### Phase 2: Prompt Engineering
- [x] Create `prompts.py` to store the system prompt.
- [x] Create a robust system prompt that forces the LLM to output structured JSON diagnoses.
- [x] Use a `ChatPromptTemplate` to structure the conversation with the LLM.

### Phase 3: Asynchronous Logic & Fallback
- [x] Ensure LLM calls do not block the main FastAPI event loop by using `ainvoke`.
- [x] Implement a fallback mechanism to handle LLM unavailability gracefully with a `try...except` block.
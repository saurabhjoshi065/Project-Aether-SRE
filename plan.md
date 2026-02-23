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

## Module 4: The Hands (Self-Healing) - PLANNED

**Goal:** Enable the Agent to perform autonomous remediation actions.

### Phase 1: Docker Integration
- [ ] Mount `docker.sock` to the `agent-service` container.
- [ ] Install `docker` Python SDK.
- [ ] Create a `docker_client.py` utility for container operations (restart, stop, logs).

### Phase 2: Action Execution
- [ ] Implement a `RepairEngine` to map LLM recommendations to concrete actions.
- [ ] Add safety checks/confirmation thresholds before executing repairs.

## Module 5: The Eyes (Context Enrichment) - PLANNED

**Goal:** Provide the LLM with deeper system context for better diagnosis.

### Phase 1: Log Ingestion
- [ ] Implement a tool to fetch the last N lines of logs from the failing container.
- [ ] Include these logs in the prompt sent to the LLM.

### Phase 2: Metrics Integration
- [ ] Fetch real-time resource usage (CPU/Mem) from Docker API.
- [ ] Provide delta-analysis (e.g., "Memory increased by 50% in the last 10s").

## Module 6: The Thinker (Agentic Workflow) - PLANNED

**Goal:** Move from a single-shot prompt to a multi-step reasoning loop.

### Phase 1: Tool Definition
- [ ] Define LangChain Tools for log fetching, metric checking, and container management.

### Phase 2: ReAct Agent
- [ ] Implement a ReAct (Reason + Act) loop using LangChain Agents.
- [ ] Allow the Agent to decide which tools to use based on the alert symptoms.
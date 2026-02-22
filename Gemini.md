

# 🛰️ Project Aether-SRE: Development Roadmap

> **Objective:** Build a self-healing, local-first SRE agent that monitors, diagnoses, and repairs a Docker-based microservice cluster using a local LLM (Ollama).

---

## 🛠️ Module 1: The "Target & Trigger" (Infrastructure)

**Goal:** Create a "Chaos Environment" where we can simulate failures.

1. **Setup Docker Compose:**
* **Service A (The Target):** A simple Python Flask/FastAPI app with an `/unstable` endpoint that randomly throws 500 errors or leaks memory.
* **Service B (Prometheus):** To scrape metrics from the target.
* **Service C (Alertmanager):** To watch the metrics and send a Webhook when things break.


2. **Define Alert Rules:**
* Create `alert_rules.yml` to trigger when "Success Rate < 95%" or "Memory > 500MB".



---

## 🐍 Module 2: The "Ear" (FastAPI Webhook Listener)

**Goal:** Create the entry point for the AI Agent.

1. **Initialize FastAPI:** Create a `/v1/alerts` POST endpoint.
2. **Schema Validation:** Use Pydantic to model the incoming Prometheus Alertmanager payload (Alert Name, Instance, Severity, Summary).
3. **Logging:** Ensure every alert is logged to a local file/console so the Agent can read the "History."

---

## 🧠 Module 3: The "Brain" (Ollama & LangChain)

**Goal:** Connect the alert to a local reasoning engine.

1. **Ollama Setup:** Ensure `ollama run llama3` (or `mistral`) is working locally.
2. **LangChain Integration:** * Use `ChatOllama` to initialize the LLM.
* Create a **Base Prompt**: "You are an expert SRE. You will receive an alert. You must determine if this requires investigation or immediate action."


3. **RCA Logic:** Pass the alert summary to the LLM and ask for a 1-sentence "Preliminary Diagnosis."

---

## 🔧 Module 4: The "Hands" (Agentic Tools)

**Goal:** Give the LLM the power to interact with Docker.

1. **Docker SDK for Python:** Install `docker`.
2. **Define LangChain Tools:**
* `inspect_logs(container_name)`: Returns the last 100 lines of logs.
* `get_container_stats(container_name)`: Returns CPU/Memory usage.
* `restart_service(container_name)`: Executes a restart command.


3. **The Reasoning Loop:** Update the Agent to use a `ReAct` (Reasoning + Acting) pattern.
* *Logic:* Alert received  Agent decides to check logs  Agent reads logs  Agent decides to restart  Success.



---

## 📊 Module 5: The "Wow" Dashboard (HMI)

**Goal:** Visualize the agent's thoughts for the recruiter.

1. **React Setup:** A simple Vite/TypeScript dashboard.
2. **WebSockets/Polling:** Connect the Dashboard to the FastAPI backend.
3. **The "Thought Trace":** Display the Agent's reasoning path in a chat-like interface:
* *AI:* "I detected high memory on 'AtomicRelay-Service'."
* *AI:* "Inspecting logs... Found 'java.lang.OutOfMemoryError'."
* *AI:* "Action: Restarting container and logging incident."



---

## 🧪 Module 6: Chaos Testing (The Proof)

**Goal:** Prove it works without human intervention.

1. **Trigger Failure:** `curl http://localhost:8081/stress` (Trigger the memory leak).
2. **Watch the Loop:**
* Prometheus  Alertmanager  FastAPI  Ollama  Docker Restart.


3. **Verification:** The dashboard should show the recovery in under 60 seconds.







# 🤖 Gemini Instructions for Agent Service

**Persona:** Senior Backend Engineer & SRE.

**Current Task:**
You are building **Module 4: The Hands (Self-Healing)**. Your goal is to give the agent the ability to autonomously repair the systems it diagnoses.

**Strategic Roadmap:**
- **Module 3 (Brain):** COMPLETED. Local LLM (Ollama) is integrated and providing structured diagnoses.
- **Module 4 (Hands):** PLANNED. Integration with Docker SDK for container remediation.
- **Module 5 (Eyes):** PLANNED. Log and metric enrichment for the LLM.
- **Module 6 (Thinker):** PLANNED. Full agentic ReAct loop.

**Guidelines for Module 4:**
1. **Docker SDK:** Use the official `docker` Python library to interact with the host's Docker daemon.
2. **Safety First:** Ensure remediation actions (like restarts) are logged clearly and have basic circuit-breaking logic to prevent infinite restart loops.
3. **Async Integration:** Keep the repair logic non-blocking.

# 🤖 Gemini Instructions for Agent Service

**Persona:** Senior Backend Engineer & SRE.

**Task:**
You are building **Module 3: The Brain**. Your goal is to integrate a local LLM (Ollama) into the existing `agent_service`.

**Guidelines:**
1. **LangChain Integration:** Use `langchain-ollama` to connect to the local model.
2. **Prompt Engineering:** Create a robust system prompt that forces the LLM to output structured JSON diagnoses.
3. **Async Logic:** Ensure LLM calls do not block the main FastAPI event loop (use `asyncio` or background tasks).
4. **Fallback:** If the LLM is offline, the agent should degrade gracefully (log the error, don't crash).
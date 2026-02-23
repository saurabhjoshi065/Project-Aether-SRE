# 🧠 Context Memory: Agent Service

## Key Decisions
- **FastAPI:** Chosen for native async support and automatic Swagger UI documentation.
- **Pydantic:** Used for strict type validation of incoming webhooks to prevent malformed data from crashing the agent.
- **Sync vs Async:** The webhook endpoint is `async` to handle high throughput without blocking, especially for the LLM calls.
- **`structlog`**: Chosen for structured, JSON-formatted logging, which is easy to parse and query.
- **LangChain**: Used to build a chain that combines the prompt, the LLM, and an output parser. This makes the code more modular and easier to maintain.

## Current Status
- **Modules 1-3:** **COMPLETE**. The diagnostic pipeline (Ear + Brain) is fully operational.
- **Next Step:** Begin **Module 4: The Hands**, focusing on Docker SDK integration for self-healing actions.

## Future Roadmap
- **Self-Healing:** Enabling autonomous container restarts and remediation.
- **Context Enrichment:** Injecting logs and real-time metrics into the LLM prompt.
- **Agentic Workflows:** Moving from simple prompts to multi-step reasoning agents.
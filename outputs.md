# 📊 Project Aether-SRE: Execution Outputs

This document explains what you will see in the logs when the **Autonomous SRE Agent** is running and handling alerts.

## 1. The Reasoning Loop (ReAct Chain)
When an alert is received, the Agent enters a "Thinking" phase. It decides which tools to use based on the problem.

**Example Log Output (`docker logs agent-service`):**

```text
> Entering new AgentExecutor chain...
The container `chaos-app` is experiencing high memory usage. 
I should investigate the current metrics to confirm if it's an OOM risk.

Action: get_service_metrics
Action Input: chaos-app
Observation: {"memory_usage_bytes": 450000000, "memory_limit_bytes": 512000000, "memory_usage_percent": 87.8}

Thought: Memory usage is very high (87%). I should check the logs to see if there is a specific error or leak.

Action: get_service_logs
Action Input: chaos-app
Observation: [ERROR] Recursive allocation loop detected in /stress endpoint...
[ERROR] Memory limit exceeded.

Thought: The logs confirm a memory leak triggered by the stress endpoint. A restart is required to recover the service.

Action: restart_service
Action Input: chaos-app
Observation: {"status": "success", "message": "Container chaos-app restarted"}

Thought: I have successfully restarted the service. I can now provide the final diagnosis.

Final Answer:
{
  "summary": "High Memory Usage on chaos-app resolved by autonomous restart.",
  "root_cause": "Manual trigger of memory leak via /stress endpoint causing 87% memory saturation.",
  "impact": "Service degradation and imminent crash (OOM).",
  "recommendations": "Investigate /stress endpoint logic and implement memory quotas.",
  "action_taken": "Restarted the chaos-app container."
}
> Finished chain.
```

## 2. Structured JSON Logs
The Agent also outputs structured JSON for ingestion into logging systems (like ELK or Grafana Loki).

```json
{
  "event": "Agent reasoning complete",
  "level": "info",
  "timestamp": "2026-02-23T11:54:44Z",
  "result": {
    "input": "Alert: High Memory Usage on chaos-app. Target: chaos-app.",
    "output": {
      "summary": "The chaos-app container experienced high memory usage and was restarted.",
      "root_cause": "High memory usage detected via metrics and confirmed by logs.",
      "action_taken": "Restarted the chaos-app container."
    }
  }
}
```

## 3. Prometheus & Alertmanager State
- **Prometheus (`localhost:9090`)**: You will see the alert `HighMemoryUsage` or `ChaosServiceDown` transition from **PENDING** to **FIRING** (Red).
- **Alertmanager (`localhost:9093`)**: You will see the alert being routed to the `agent-service` receiver.

## 4. Self-Healing Verification
You can verify the restart happened by checking the container's uptime:
```bash
docker ps --filter "name=chaos-app"
```
You will notice the `STATUS` says `Up Less than a minute` after the Agent has fixed it.

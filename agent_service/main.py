import json
from fastapi import FastAPI, Response, status
from schemas import AlertmanagerWebhook
import structlog
from llm import get_llm
from prompts import SYSTEM_PROMPT
from tools import restart_service, get_service_logs, get_service_metrics
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_core.prompts import PromptTemplate

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(
    title="Project Aether - Agent Service",
    description="An autonomous SRE Agent that diagnoses and repairs infrastructure.",
    version="1.0.0",
)

# Initialize LLM and Tools
llm = get_llm()
tools = [restart_service, get_service_logs, get_service_metrics]

# Define the ReAct prompt template
template = """You are a senior Site Reliability Engineer (SRE). Your goal is to diagnose and resolve alerts.
You have access to the following tools:

{tools}

Use the following format:

Question: the input alert you must diagnose
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (usually the container name)
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: A JSON object with the diagnosis and any actions taken.
{{
  "summary": "...",
  "root_cause": "...",
  "impact": "...",
  "recommendations": "...",
  "action_taken": "..."
}}

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# Create the Agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=5,
    max_execution_time=120 # Timeout after 120 seconds
)

@app.get("/")
def read_root():
    return {"message": "Project Aether Agentic SRE is Active"}


@app.post("/v1/alerts", status_code=status.HTTP_202_ACCEPTED)
async def post_alerts(payload: AlertmanagerWebhook):
    """
    Receives alerts and triggers an autonomous reasoning loop.
    """
    await logger.ainfo("Received alert payload", alert=payload.model_dump())
    
    if payload.alerts:
        alert = payload.alerts[0]
        alert_summary = alert.annotations.get('summary', 'No summary provided')
        container = alert.labels.get('job', 'unknown')
        
        input_msg = f"Alert: {alert_summary}. Target: {container}."
        
        try:
            await logger.ainfo("Starting agentic reasoning loop", input=input_msg)
            # Agents in LangChain 0.1+ are invoked with invoke()
            result = await agent_executor.ainvoke({"input": input_msg})
            await logger.ainfo("Agent reasoning complete", result=result)
        except Exception as e:
            await logger.aerror("Agent execution failed", error=str(e))

    return {"status": "success"}

from fastapi import FastAPI, Response, status
from schemas import AlertmanagerWebhook
import structlog
from llm import get_llm
from prompts import SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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
    description="Receives alerts from Prometheus and uses an LLM to diagnose them.",
    version="0.1.0",
)

llm = get_llm()

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{alert_summary}"),
    ]
)

chain = prompt_template | llm | StrOutputParser()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Agent Service"}


@app.post("/v1/alerts", status_code=status.HTTP_202_ACCEPTED)
async def post_alerts(payload: AlertmanagerWebhook):
    """
    Receives alerts from Prometheus Alertmanager.
    """
    await logger.ainfo("Received alert payload", alert=payload.model_dump())
    
    # For now, just use the first alert
    if payload.alerts:
        alert = payload.alerts[0]
        alert_summary = alert.annotations.get('summary', '')
        
        if not alert_summary:
            await logger.awarning("Alert summary missing, skipping LLM diagnosis")
            return {"status": "skipped_no_summary"}
        
        try:
            response = await chain.ainvoke({"alert_summary": alert_summary})
            await logger.ainfo("LLM response", response=response)
        except Exception as e:
            await logger.aerror("LLM invocation failed", error=str(e))

    return {"status": "success"}

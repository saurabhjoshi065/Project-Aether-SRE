import os
from langchain_ollama import OllamaLLM

def get_llm():
    """
    Returns an instance of the Ollama LLM.
    """
    model_name = os.environ.get("OLLAMA_MODEL", "kimi-k2.5:cloud")
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    return OllamaLLM(model=model_name, base_url=base_url)

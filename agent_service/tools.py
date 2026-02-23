from langchain.tools import tool
from docker_utils import restart_container, get_container_logs, get_container_stats
import json

@tool
def restart_service(container_name: str) -> str:
    """Restarts a specific docker container by its name. Use this when a service is down or behaving abnormally."""
    result = restart_container(container_name)
    return json.dumps(result)

@tool
def get_service_logs(container_name: str) -> str:
    """Fetches the last 50 lines of logs from a specific docker container. Use this to find error messages or stack traces."""
    return get_container_logs(container_name)

@tool
def get_service_metrics(container_name: str) -> str:
    """Fetches real-time memory and resource usage for a container. Use this to check for OOM or resource exhaustion."""
    stats = get_container_stats(container_name)
    return json.dumps(stats)

import docker
import structlog

logger = structlog.get_logger()

try:
    client = docker.from_env()
except Exception as e:
    logger.error("Failed to connect to Docker daemon", error=str(e))
    client = None

def restart_container(container_name: str):
    """
    Restarts a container by its name.
    """
    if not client:
        return {"status": "error", "message": "Docker client not initialized"}
    
    try:
        container = client.containers.get(container_name.strip())
        container.restart()
        return {"status": "success", "message": f"Container {container_name.strip()} restarted"}
    except Exception as e:
        logger.error("Failed to restart container", container=container_name, error=str(e))
        return {"status": "error", "message": str(e)}

def get_container_logs(container_name: str, tail: int = 50):
    """
    Fetches the last N lines of logs from a container.
    """
    if not client:
        return "Error: Docker client not initialized"
    
    try:
        container = client.containers.get(container_name.strip())
        logs = container.logs(tail=tail).decode('utf-8')
        return logs
    except Exception as e:
        logger.error("Failed to fetch logs", container=container_name, error=str(e))
        return f"Error: {str(e)}"

def get_container_stats(container_name: str):
    """
    Fetches real-time stats (like memory usage) for a container.
    """
    if not client:
        return {}
    
    try:
        container = client.containers.get(container_name.strip())
        stats = container.stats(stream=False)
        
        # Simplify stats for the LLM
        memory_usage = stats.get('memory_stats', {}).get('usage', 0)
        memory_limit = stats.get('memory_stats', {}).get('limit', 0)
        
        return {
            "memory_usage_bytes": memory_usage,
            "memory_limit_bytes": memory_limit,
            "memory_usage_percent": (memory_usage / memory_limit) * 100 if memory_limit > 0 else 0
        }
    except Exception as e:
        logger.error("Failed to fetch stats", container=container_name, error=str(e))
        return {}

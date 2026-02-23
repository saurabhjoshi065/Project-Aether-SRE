from fastapi import FastAPI
import threading
import time

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Chaos Service Operational"}

@app.post("/stress")
def trigger_stress():
    """Triggers a memory leak to crash the container."""
    def consume_memory():
        data = []
        while True:
            data.append(' ' * 10**7)  # Allocate 10MB chunks
            time.sleep(0.1)
            
    threading.Thread(target=consume_memory).start()
    return {"status": "Memory stress triggered"}
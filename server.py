from fastapi import FastAPI
import psutil

app = FastAPI()

@app.get("/stats")
async def stats():
    return{
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
        "network_sent": psutil.net_io_counters().bytes_sent,
        "network_received": psutil.net_io_counters().bytes_recv,
    }

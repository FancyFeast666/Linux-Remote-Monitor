from fastapi import FastAPI
import os

app = FastAPI()

pipe = "/tmp/system_stats"

@api.get("/stats")
async def stats():
    #reads the system stats from the pipe and returns it under the /stats"
    try:
        with open(pipe, "r") as data:
            stats_str = data.readline().strip()  # obtains the latest stats from the pipe
            return eval(stats_str)  # taking the string from the pipe and converting it back to a dict
    except Exception as e:
        return {"error": f"Failed to read stats: {str(e)}"}

#used for the initial connection to determine if the server is available
@app.get("/status")
asyic def status():
    return True
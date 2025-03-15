import os
import psutil
import time

FIFO_PATH = "/tmp/system_stats"

def write_stats():
    #will continuously update the pipe with the updated stats
    while True:
        stats = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
            "network_sent": psutil.net_io_counters().bytes_sent,
            "network_received": psutil.net_io_counters().bytes_recv,
            "boot_time": get_uptime(),
            "swap": psutil.swap_memory().percent,
            "load_avg": get_load_avg()
        }

        #converting the dictionary stats to a string form to be sent into the pipe
        stats_str = str(stats)

        # Open the pipe and write data
        with open(FIFO_PATH, "w") as fifo:
            fifo.write(stats_str + "\n")

        time.sleep(1)  #updating the pipe with new stats each second

#used to obtain the current uptime of the server in seconds
def get_uptime():
    with open("/proc/uptime","r") as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

#used to obtain the 1-minute load average of the server
def get_load_avg():
    with open("/proc/loadavg", "r") as f:
        loadavg = f.read().split()[:3]
        return {float(loadavg[0])}

if __name__ == "__main__":
    write_stats()

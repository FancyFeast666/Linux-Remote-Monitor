import requests
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fetch_stats():
    global IP
    try:
        response = requests.get(IP + "/stats", timeout=2)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None

def connectGridDeactivate():
    connect.grid_forget()
    labelIP.grid_forget()
    entryIP.grid_forget()
    labelPort.grid_forget()
    entryPort.grid_forget()

def connectGridActivate():
    labelIP.grid(row=1, column=0, ipady=10)
    entryIP.grid(row =2, column=0, ipady=10)
    labelPort.grid(row=3, column=0, ipady=10)
    entryPort.grid(row=4, column=0, ipady=10)
    connect.grid(row=9, column=0, ipady=10)

def graphEnable():
    cpu_label.grid(row=6, column=0)
    memory_label.grid(row=6, column=1)
    disk_label.grid(row=7, column=0)
    network_label.grid(row=7, column=1)
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)
    boot_label.grid(row=8, column=0)
    swap_label.grid(row = 8, column=1)
def connect():
    global IP, PORT
    IP = entryIP.get()
    PORT = entryPort.get()
    IP = "http://" + IP + ":" + PORT
    try:
        response = requests.get(IP + "/status", timeout=2)
        #200 code will not trigger an exception

        connectGridDeactivate()
        graphEnable()
        start_monitoring()
    except Exception as e:
        messagebox.showwarning("Connection Error", f"{e}")

def start_monitoring():
    stats = fetch_stats()
    update_stats(stats)
    update_graph(stats)
    window.after(1000, start_monitoring)  # Refresh every second

def update_stats(stats):
    if stats:
        cpu_label.config(text=f"CPU Usage: {stats['cpu_usage']}%")
        memory_label.config(text=f"Memory Usage: {stats['memory_usage']}%")
        disk_label.config(text=f"Disk Usage: {stats['disk_usage']}%")
        network_label.config(text=f"Network Sent: {stats['network_sent']} | Received: {stats['network_received']}")
        boot_label.config(text=f"Current Boot Time: {stats['boot_time']}")
        swap_label.config(text=f"Swap Memory: {stats['swap']}%")

def update_graph(stats):
    if stats:
        for key, value in [("cpu", stats["cpu_usage"]), ("memory", stats["memory_usage"]), ("disk", stats["disk_usage"]), ("swap", stats["swap"]), ("load", stats["load"])]:
            history[key].append(value)
            if len(history[key]) > 60:  # Keep only last 60 seconds
                history[key].pop(0)
            #if history[key][len(history[key])-2] == value:
            #    history[key][-1] += 0.0001
        load1, load5, load15 = history["load"]
        print(load1, load5, load15)
        cpu_line.set_ydata(history["cpu"])
        memory_line.set_ydata(history["memory"])
        disk_line.set_ydata(history["disk"])
        swap_line.set_ydata(history["swap"])
        load1_line.set_ydata(history["load"][0])
        load5_line.set_ydata(history["load"][1])
        load15_line.set_ydata(history["load"][2])


        cpu_line.set_xdata(range(len(history["cpu"])))
        memory_line.set_xdata(range(len(history["memory"])))
        disk_line.set_xdata(range(len(history["disk"])))
        swap_line.set_xdata(range(len(history["swap"])))
        load1_line.set_xdata(range(len(history["load"][0])))
        load5_line.set_xdata(range(len(history["load"][1])))
        load15_line.set_xdata(range(len(history["load"][2])))


        ax.relim()
        ax.autoscale_view()
        canvas.draw()






if __name__ == "__main__":
    window = tk.Tk()
    window.title("Server Monitoring")
    window.geometry("600x600")


    labelIP = tk.Label(window, text="Enter IP Address of Server")
    labelIP.grid(row=1, column=0, ipady=10)

    entryIP = tk.Entry(window)
    entryIP.grid(row =2, column=0, ipady=10)

    labelPort = tk.Label(window, text="Enter Port Address of Server")
    labelPort.grid(row=3, column=0, ipady=10)

    entryPort = tk.Entry(window)
    entryPort.grid(row=4, column=0, ipady=10)

    connect = tk.Button(window, text="Connect", command=connect)
    connect.grid(row=9, column=0, ipady=10)

    cpu_label = tk.Label(window, text="CPU Usage: --%")
    memory_label = tk.Label(window, text="Memory Usage: --%")
    disk_label = tk.Label(window, text="Disk Usage: --%")
    network_label = tk.Label(window, text="Network Sent/Received: --")
    boot_label = tk.Label(window, text= "Current Boot Time: --")
    swap_label = tk.Label(window, text= "Swap memory: --%")

    # --- Graph Setup ---
    history = {"cpu": [], "memory": [], "disk": [], "networkSent": [], "networkReceived": [], "swap": [], "load": []}
    fig, ax = plt.subplots()
    ax.set_ylim(0, 100)  # Assuming percentage values
    ax.set_xlim(0, 60)  # 60 seconds history
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Usage (%)")

    cpu_line, = ax.plot([], [], label="CPU")
    memory_line, = ax.plot([], [], label="Memory")
    disk_line, = ax.plot([], [], label="Disk")
    swap_line, =ax.plot([],[], label="Swap")
    load1_line, = ax.plot([],[], label="Load (1-Min)")
    load5_line, = ax.plot([],[], label="Load (5-Min)")
    load15_line, = ax.plot([],[], label="Load (15-Min)")

    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=window)

    window.mainloop()

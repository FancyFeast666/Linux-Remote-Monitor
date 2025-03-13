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


def connect():
    global IP, PORT
    IP = entryIP.get()
    PORT = entryPort.get()
    IP = "http://" + IP + ":" + PORT
    try:
        response = requests.get(IP + "/status", timeout=2)
        #200 code will not trigger an exception

        connectGridDeactivate()
        start_monitoring()
        graphEnable()
    except Exception as e:
        messagebox.showwarning("Connection Error", f"{e}")

def start_monitoring():
    graphEnable()
    update_stats()
    update_graph()

def update_stats():
    stats = fetch_stats()
    if stats:
        cpu_label.config(text=f"CPU Usage: {stats['cpu_usage']}%")
        memory_label.config(text=f"Memory Usage: {stats['memory_usage']}%")
        disk_label.config(text=f"Disk Usage: {stats['disk_usage']}%")
        network_label.config(text=f"Network Sent: {stats['network_sent']} | Received: {stats['network_received']}")

    window.after(1000, update_stats)  # Refresh every second



def update_graph():
    stats = fetch_stats()
    if stats:
        for key, value in [("cpu", stats["cpu_usage"]), ("memory", stats["memory_usage"]), ("disk", stats["disk_usage"]), ("networkSent", stats["network_sent"]), ("networkReceived", stats["network_received"])]:
            history[key].append(value)
            if len(history[key]) > 60:  # Keep only last 60 seconds
                history[key].pop(0)

        cpu_line.set_ydata(history["cpu"])
        memory_line.set_ydata(history["memory"])
        disk_line.set_ydata(history["disk"])
        networkRecv_line.set_ydata((history["networkSent"]))
        networkSent_line.set_ydata((history["networkReceived"]))
        cpu_line.set_xdata(range(len(history["cpu"])))
        memory_line.set_xdata(range(len(history["memory"])))
        disk_line.set_xdata(range(len(history["disk"])))
        networkRecv_line.set_xdata(range(len(history["networkSent"])))
        networkSent_line.set_xdata(range(len(history["networkReceived"])))


        ax.relim()
        ax.autoscale_view()
        canvas.draw()

    window.after(1000, update_graph)





if __name__ == "__main__":
    window = tk.Tk()
    window.title("Server Monitoring")
    window.geometry("500x500")


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


    # --- Graph Setup ---
    history = {"cpu": [], "memory": [], "disk": [], "networkSent": [], "networkReceived": []}
    fig, ax = plt.subplots()
    ax.set_ylim(0, 100)  # Assuming percentage values
    ax.set_xlim(0, 60)  # 60 seconds history
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Usage (%)")

    cpu_line, = ax.plot([], [], label="CPU")
    memory_line, = ax.plot([], [], label="Memory")
    disk_line, = ax.plot([], [], label="Disk")
    networkRecv_line, = ax.plot([],[], label="Network Recv")
    networkSent_line, = ax.plot([],[], label="Network Sent")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=window)

    window.mainloop()

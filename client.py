import requests
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import customtkinter
import matplotlib.pyplot as plt


API_URL = "http://192.168.1.107:5000/stats"
def fetch_stats():
    try:
        response = requests.get(API_URL, timeout=2)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None

def connect():
    global IP, PORT
    IP = entryIP.get()
    PORT = entryPort.get()
    IP = "http://" + IP + ":" + PORT + "/status"
    response = requests.get(IP, timeout=2)
    if response.status_code == 200:
        print( response.json())

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


    window.mainloop()

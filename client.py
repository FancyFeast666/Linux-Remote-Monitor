import requests
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import customtkinter

API_URL = "http://192.168.1.107:5000/stats"
def fetch_stats():
    try:
        response = requests.get(API_URL, timeout=2)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None

#print(fetch_stats())

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Server Monitoring")
    window.geometry("700x700")


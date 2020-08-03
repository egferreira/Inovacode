import pandas as pd
import numpy as np
import Tela
import tkinter as tk
import threading

# def MyThread (threading.thread):
#     # doing something........
#     print("Something")

def run_app():
    # hide main window
    # root = tkinter.Tk()
    root = tk.Tk()
    root.title("Cardeal Assist")
    tela = Tela.Tela(root)
    tela.setup()
    root.mainloop()
    

run_app()
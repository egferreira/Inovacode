import pandas as pd
import numpy as np
import Tela
import tkinter as tk
import tkcalendar
import threading

    
def run_app():

    root = tk.Tk()
    root.title("Cardeal Assist")
    tela = Tela.Tela(root)

    tela.setup()

    root.mainloop()
    

run_app()
import pandas as pd
import numpy as np
import Tela
import tkinter as tk
import tkcalendar
import threading
import GoogleCalendarApi as calendar
import pendulum

# def MyThread (threading.thread):
#     # doing something........
#     print("Something")

def run_app():
    # hide main window
    # root = tkinter.Tk()
    # root = tk.Tk()
    # root.title("Cardeal Assist")
    # tela = Tela.Tela(root)
    # tela.setup()
    # root.mainloop()
    google_calendar = calendar.GoogleCalendarApi("marchesan.gregory@gmail.com")
    events = google_calendar.get_next_events(last_day=pd.to_datetime(pendulum.now().end_of('week')), number=100)
    
    # print(events.dtypes)
    # df = google_calendar.process_work_slices()
    print(events)
    # today = 
    # start = today.start_of('week')
    # end = 
    # print(end)
    pass

    

run_app()
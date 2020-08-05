import pandas as pd
import numpy as np
# import Tela
import tkinter as tk
import tkcalendar
import threading
import GoogleCalendarApi as calendar
import pendulum
import Rewards



data = {"Task" : ["Fazer cafe", "Ganhar Hackathon", "Anotar"],
                     "Time" : [50, 900, 300],
                     "Priority" : [4, 5, 1]}
tasks = pd.DataFrame(data=data)

def run_app():
    rewards = Rewards.Reward("marchesan.gregory@gmail.com")
    rewards.start()
    # hide main window
    # root = tkinter.Tk()
    # root = tk.Tk()
    # root.title("Cardeal Assist")
    # tela = Tela.Tela(root)
    # tela.setup()
    # root.mainloop()
    # google_calendar = calendar.GoogleCalendarApi("marchesan.gregory@gmail.com")
    # events = google_calendar.get_next_events(last_day=pd.to_datetime(pendulum.now().end_of('week')), number=100)
    
    # print(events.dtypes)

    # df = google_calendar.process_work_slices()
    # google_calendar.schedule_time(tasks, events)
    # print(google_calendar.check_concluded_events_this_week())
    # today = 
    # start = today.start_of('week')
    # end = 
    # print(end)

    

run_app()
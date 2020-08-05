
import pandas as pd
import numpy as np

# Screen
import PySimpleGUI as sg
from PySimpleGUI import Window, Text, Button, CBox, Input, change_look_and_feel

import sys

import tkcalendar
import threading
import GoogleCalendarApi as calendar
import pendulum
import Rewards
import PySimpleGUI as sg




data = {"Task" : ["Fazer cafe", "Ganhar Hackathon", "Anotar"],
                     "Time" : [50, 900, 300],
                     "Priority" : [4, 5, 1]}

tasks = pd.DataFrame( data = data)

change_look_and_feel('Reds')   # Add a little color for fun

layout = None
window = None
def setLayout( ):
    layout = [  [sg.Text(' Atividades para a semana', size=(25,1), justification='center', font=("Verdana", "10", "bold"))],
                [sg.Text('Atividade:', size=(10,1), justification='right'), sg.I(key='-ATIVIDADE-', do_not_clear=False)],
                [sg.T('Tempo:', size=(10,1), justification='right'), sg.I(key='-TEMPO-', do_not_clear=False)],
                [sg.T('Prioridade:', size=(10,1), justification='right'), sg.I(key='-PRIORIDADE-', do_not_clear=False)],
                [sg.T(' '*20), sg.Button('Inserir'), sg.Button('Excluir')],                
                [sg.T( key = '-MESSAGE-', size=(30,1), font=("Verdana", "9", "italic"))]]

    layout +=  [[Text('Progresso', justification = 'Left', font="Verdana 10")]]  # a title line t

    try:
        layout += [[Text(f'{i+1}. '), CBox(''), sg.I(data['Task'][i])] for i in range( len( data['Task']))]  # the checkboxes and descriptions
    except:    
        layout += [[Text(f'{i}. '), CBox(''), Input()] for i in range(1, 6)]  # the checkboxes and descriptions

    window = sg.Window('Cardeal Assist', layout, font = 'Calibri 10', default_element_size = (25,1))
    return window

window = setLayout()


while True:             # Event Loop
    event, values = window.read()
    print(event, values)    
    if event is None:
        break
    
    if event == 'Inserir':
        newData =   (values['-ATIVIDADE-'],
                    values['-TEMPO-'],
                    values['-PRIORIDADE-'])        

        data['Task'].append(newData[0])
        data['Time'].append(newData[1])
        data['Priority'].append(newData[2])
                                        
        window.close()                                        
        window = setLayout()        

    print(data)

        




def run_app():            
    print("run")
        
    # rewards = Rewards.Reward("marchesan.gregory@gmail.com")
    # rewards.start()
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

import pandas as pd
import numpy as np
import Pomodoro
# Screen
import PySimpleGUI as sg
from PySimpleGUI import Window, Text, Button, CBox, Input, change_look_and_feel
import sys
import threading
import GoogleCalendarApi as calendar
import Rewards
import pendulum



# Variables definition
data = {"Task" : ["Fazer cafe", "Ganhar Hackathon", "Anotar"],
                     "Time" : [50, 900, 300],
                     "Priority" : [4, 5, 1]}

tasks = pd.DataFrame( data = data) # Data frame
change_look_and_feel('Cardeal') # Color Scheme
layout = None # Layout
window = None # Frame
workSlices = None # Global
mail = "seu_email@gmail.com"
google_calendar = None

# Atualizar calendar
def updateCalendar( google_calendar):
    events = google_calendar.get_next_events(last_day=pd.to_datetime(pendulum.now().end_of('week')), number=100)            
    return events

# Definindo os parametros do calendário
def setupCalendar():    
    rewards = Rewards.Reward(mail)
    rewards.start()            
    google_calendar = calendar.GoogleCalendarApi(mail)
    events = google_calendar.get_next_events(last_day=pd.to_datetime(pendulum.now().end_of('week')), number=100)                
    return events, google_calendar
    #print(google_calendar.check_concluded_events_this_week())    

# Seta Oo Layout da aplicação
def setLayout():
    layout = [  [sg.Text(' Atividades para a semana', size=(25,1), justification='center', font=("Verdana", "10", "bold"))],
                [sg.Text('Atividade:', size=(10,1), justification='right'), sg.I(key='-ATIVIDADE-', do_not_clear=False)],
                [sg.T('Tempo:', size=(10,1), justification='right'), sg.I(key='-TEMPO-', do_not_clear=False)],
                [sg.T('Prioridade:', size=(10,1), justification='right'), sg.I(key='-PRIORIDADE-', do_not_clear=False)],
                [sg.T(' '*5), sg.Button('Inserir'), sg.Button('Pomodoro'), sg.Button('Agendar')],                
                [sg.T( key = '-MESSAGE-', size=(30,1), font=("Verdana", "9", "italic"))]]

    layout +=  [[Text('Progresso', justification = 'Left', font="Verdana 10")]]  # a title line t
    try:
        layout += [[Text(f'{i+1}. '), CBox(''), sg.I(data['Task'][i])] for i in range( len( data['Task']))]  # the checkboxes and descriptions
    except:    
        layout += [[Text(f'{i}. '), CBox(''), Input()] for i in range(1, 6)]  # the checkboxes and descriptions
    window = sg.Window('Cardeal Assist', layout, font = 'Calibri 10', default_element_size = (25,1))
    return window

# Inicializando 
window = setLayout()
workSlices, google_calendar = setupCalendar()

# Main Loop da aplicação
while True:     
    event, values = window.read()
    # Caso a aplicação não tenha mudanças continua mostrando        
    if event is None:
        break               

    # Atividades dos eventos
    if event == 'Inserir':  # Botao Inserir
        newData =   (values['-ATIVIDADE-'],
                    values['-TEMPO-'],
                    values['-PRIORIDADE-'])        

        data['Task'].append(newData[0])
        try:
            data['Time'].append(int(newData[1]))
        except:
            pass        
        try:
            data['Priority'].append(int(newData[2]))
        except:
            pass
                                        
        window.close()                                        
        window = setLayout()  

    elif event == 'Pomodoro': # Botao do pomodoro       
        Pomodoro.Pomodoro()        
        pass

    elif event == 'Agendar':  # Agenda no google Agendas
        tasks = pd.DataFrame( data = data)
        workSlices = updateCalendar(google_calendar)        
        google_calendar.schedule_time(tasks, workSlices)
            
    





    

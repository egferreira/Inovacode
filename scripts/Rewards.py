# Import
try:
    import winsound
except ImportError:
    import os
    def playsound(frequency,duration):
        #apt-get install beep
        os.system('beep -f %s -l %s' % (frequency,duration))
else:
    def playsound(frequency,duration):
        winsound.Beep(frequency,duration)
        
from threading import Thread
import pandas as pd
import GoogleCalendarApi as calendar
import time

REWARDS_FILE = "../config/rewards.csv"

# Inicizalizacao da thread da aplicacao
class Reward(Thread):
    tasks_complete = 0
    hours_work = pd.Timedelta(hours=0)
    rewards = pd.DataFrame()
    subject = None
    agenda = None
    reward = False
    tasks_complete = 0
    hours_work = pd.Timedelta(hours=0)
    rewards = pd.DataFrame()
    subject = None
    agenda = None
    reward = False
    last_reward = None
    last_i = 0

    # Inicializacao da thread
    def __init__(self, subject):
        Thread.__init__(self)        
        self.subject = subject
        self.agenda = calendar.GoogleCalendarApi(subject)
        self.load_rewards_file()

    # Loop para a thread
    def run(self):        
        while(True):
            try:
                complete_tasks = self.agenda.check_concluded_events_this_week()
                complete_tasks['DURATION'] = complete_tasks['end'] - complete_tasks['start']
                total_time = complete_tasks['DURATION'].sum()
                total_tasks = len(complete_tasks)
                self.check_reward(total_time, total_tasks)                
            except:
                pass
            time.sleep(30)
            #print("running rewards")

    # Carrega as recompensas
    def load_rewards_file(self):
        self.rewards = pd.read_csv(REWARDS_FILE)
        self.rewards['TOTAL_TIME'] = self.rewards['TOTAL_TIME'].apply(lambda x: pd.Timedelta(minutes=x))
    
    # Checa as tarefas para garantir que existe recompensa
    def check_reward(self, total_time, total_tasks):
        for i in range(self.last_i, len(self.rewards)):
            if(total_time >= self.rewards.loc[i, 'TOTAL_TIME'] and total_tasks >= self.rewards.loc[i, 'TASKS_NUMBER']):
                if(self.last_reward != self.rewards.loc[i, 'REWARD']):
                    self.reward = True
                    self.last_reward = self.rewards.loc[i, 'REWARD']
                    self.last_i = i
                    
                    print( "Você ganhou  " + self.rewards.loc[i, 'REWARD'])
                    #easygui.msgbox("Você ganhou  " + self.rewards.loc[i, 'REWARD'], title="NEW REWARD")                                        
    

    
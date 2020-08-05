import tkinter
from tkinter import messagebox
from tkinter import simpledialog
import winsound
from threading import Thread
import pandas as pd
import GoogleCalendarApi as calendar
import time

REWARDS_FILE = "../config/rewards.csv"

class Reward(Thread):
    tasks_complete = 0
    hours_work = pd.Timedelta(hours=0)
    rewards = pd.DataFrame()
    subject = None
    agenda = None
    last_reward = None
    last_i = 0

    def __init__(self, subject):
        Thread.__init__(self)
        self.subject = subject
        self.agenda = calendar.GoogleCalendarApi(subject)
        self.load_rewards_file()

    def run(self):
        while(True):
            complete_tasks = self.agenda.check_concluded_events_this_week()
            complete_tasks['DURATION'] = complete_tasks['end'] - complete_tasks['start']

            total_time = complete_tasks['DURATION'].sum()
            total_tasks = len(complete_tasks)

            self.check_reward(total_time, total_tasks)
            time.sleep(30)

    def load_rewards_file(self):
        self.rewards = pd.read_csv(REWARDS_FILE)
        self.rewards['TOTAL_TIME'] = self.rewards['TOTAL_TIME'].apply(lambda x: pd.Timedelta(minutes=x))

    def check_reward(self, total_time, total_tasks):
        for i in range(self.last_i, len(self.rewards)):
            if(total_time >= self.rewards.loc[i, 'TOTAL_TIME'] and total_tasks >= self.rewards.loc[i, 'TASKS_NUMBER']):
                if(self.last_reward != self.rewards.loc[i, 'REWARD']):
                    self.last_reward = self.rewards.loc[i, 'REWARD']
                    self.last_i = i
                    messagebox.showinfo("NEW REWARD!", "Você ganhou: " + self.rewards.loc[i, 'REWARD'])

    

    
# !/usr/bin/env python3

import tkinter as tk
from tkcalendar import *
import Pomodoro
import Semana

class Tela( object):
    cal = None
    root = None
    openSemScreen = None

    def __init__(self, root):
        self.root = root
        self.cal = Calendar(root, seLectmode ="day", year=2020, month=8, day=2, firstweekday = "sunday")
        self.openSemScreen = False

    def getDate(self):
        print(self.cal.get_date())

    def showSemana( self):
        self.root.geometry("600x800")
        #semanaWindow.title("Atividades para a semana")
        if ( self.openSemScreen == False):
            self.openSemScreen = True
            a = Semana.MultiColumnListbox()
            print (a)

        

    def start_pomodoro(self):
        pomodoro = Pomodoro.Pomodoro()
        pomodoro.start()
        # self.root.destroy()

    def setup(self):
        self.root.geometry("600x400")
        self.cal.pack(pady=20)
    
        botao = tk.Button( self.root, text = "Mostrar Semana", width=10, height=1, command=self.showSemana)
        botao.pack( padx = 10)

        #botao = tk.Button(self.root, text = "Selecionar Dia", command=self.getDate)
        #botao.pack(pady=20)        
        pomodoro = tk.Button(self.root, text = "Start pomodoro", command=self.start_pomodoro)
        pomodoro.pack(pady=20)





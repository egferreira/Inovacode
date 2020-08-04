# !/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk
from tkcalendar import *
import Pomodoro
import pandas as pd


class Tela( object):
    cal = None
    root = None
    openSemScreen = None
    fileName = None
    header = None
    active_list = None

    def __init__( self, root):
        self.root = root
        self.cal = Calendar(root, seLectmode ="day", year=2020, month=8, day=2, firstweekday = "sunday")
        self.openSemScreen = False
        self.fileName = ImageTk.PhotoImage( file = "background.png")
        self.header = ['Atividade', 'Tempo', 'Prioridade']
        self.active_list = []      
        
        #root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage( file = "cardeal.png"))

    def getDate( self):
        print( self.cal.get_date())
        
    def insert_data(self):
        itens = self.name_entry.get() , self.time_entry.get() , self.idnumber_entry.get()
        self.active_list.append( itens)        
        self.treeview.insert('', 'end',  text = self.name_entry.get(), 
                             values = ( self.time_entry.get(), self.idnumber_entry.get() ) )
        
    def delete_data( self):
        self.getDf()
        #row_id = int( self.tree.focus())
        #self.treeview.delete( row_id)
        #self.active_list.remove( row_id)
            
    def set_tree( self):
        self.tree = ttk.Treeview( self.root, columns = ( self.header[0], self.header[1], self.header[2]))
        self.tree.heading('#0', text = self.header[0])
        self.tree.heading('#1', text = self.header[1])
        self.tree.heading('#2', text = self.header[2])
        self.tree.column( '#0', stretch = tk.YES)
        self.tree.column( '#1', stretch = tk.YES)
        self.tree.column( '#2', stretch = tk.YES)
 
        self.tree.grid( row = 7, columnspan = 3, sticky ='nsew')
        self.treeview = self.tree
        
        
    def start_pomodoro(self):
        pomodoro = Pomodoro.Pomodoro()
        pomodoro.start()
        # self.root.destroy()

        
    def setup(self):

        background_label = tk.Label( self.root,  image = self.fileName)
        background_label.place( x = 0, y = 0, relwidth = 1, relheight = 1)
        self.root.geometry("640x640")
        
        #self.root.iconphoto( False, tk.PhotoImage(file='/path/to/ico/icon.png'))
        
        #self.dummy = tk.Label( self.root, text = "")
        #self.dummy.grid( row = 0, column = 0 , sticky = tk.N)
        
        # Entrada de dados
        self.name_label = tk.Label( self.root, text = "Atividade:    ")
        self.name_entry = tk.Entry( self.root)
        self.name_label.grid( row = 2, column = 0 , sticky = tk.W)
        self.name_entry.grid( row = 2, column = 1)
        
        self.idnumber_label = tk.Label( self.root, text = "Prioridade:")
        self.idnumber_entry = tk.Entry( self.root)
        self.idnumber_label.grid( row = 3, column = 0, sticky = tk.W)
        self.idnumber_entry.grid( row = 3, column = 1)
        
        self.time_proposed = tk.Label( self.root, text = "Tempo Alocado:")
        self.time_entry = tk.Entry( self.root)
        self.time_proposed.grid( row = 4, column = 0, sticky = tk.W)
        self.time_entry.grid( row = 4, column = 1)
        
        self.submit_button = tk.Button( self.root, text = "Inserir", command = self.insert_data)
        self.submit_button.grid( row = 5, column = 1, sticky = tk.W)
        
        self.delete_button = tk.Button( self.root, text = "Delete", command = self.delete_data)
        self.delete_button.grid( row = 5, column = 2, sticky = tk.W)
        
        self.set_tree( )
        
        pomodoro = tk.Button( self.root, text = "Start pomodoro", command = self.start_pomodoro)
        pomodoro.grid( column = 1, sticky = tk.W)
        

    def getDf( self):
        df = pd.DataFrame (self.active_list, columns = [ self.header[0], self.header[1], self.header[2]])
        print (df)




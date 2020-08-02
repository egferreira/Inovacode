# !/usr/bin/env python3

from tkinter import *
from tkcalendar import *


def getDate():
    print( cal.get_date()  )

root = Tk()
root.title( "Exemplo de tela")
root.geometry("600x400")

cal = Calendar(root, seLectmode ="day", year=2020, month=8, day=2, firstweekday = "sunday")

cal.pack(pady=20)
botao = Button(root, text = "Selecionar Dia", command=getDate)
botao.pack(pady=20)




root.mainloop()

import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import ttk
import json
import Calculate
import Draw

def start():

    def calculate(output):
        recipe = recipes_list_choose.get()
        Calculate.calculate(recipe, output)

    mainW.destroy()

    StartW = tk.Tk()
    StartW.geometry(f'175x240+100+100')
    StartW['bg'] = 'white'
    StartW.title('Start')
    StartW.wm_attributes('-topmost', 1)

    tk.Label(StartW, text='Рецепт:', font=('Arial', 15), bg='white', fg='blue').grid(row=0, column=0, stick='s',padx=5, pady=5)
    recipes_list = ['ротор','винт','железный прут','железный слиток']
    recipes_list_choose = ttk.Combobox(StartW,values = recipes_list, background='white',foreground='blue',font=('Arial', 10))
    recipes_list_choose.grid(row = 1,column=0,stick='wens',padx=5,pady=5)

    tk.Label(StartW, text='Выход в минуту:', font=('Arial', 15), bg='white', fg='blue').grid(row=2, column=0, stick='s',padx=5, pady=5)
    output = tk.Entry(StartW, justify=tk.CENTER, font=('Arial', 15), width=6, bg='white', fg='blue')
    output.grid(row=3, column=0,stick='w')

    tk.Button(StartW,justify=tk.CENTER, text='Ввод', bd=5, font=('Arial', 13), bg='white', fg='blue', command = lambda: calculate(int(output.get()))).grid(row=4, column=0, stick='wens', padx=5, pady=5)

    StartW.mainloop()

def recipeF():
    pass

def settings():
    settingsW = tk.Tk()
    settingsW.geometry(f'270x300+1300+400')
    settingsW['bg'] = 'white'
    settingsW.title('Settings')
    settingsW.wm_attributes('-topmost', 1)

    tk.Label(settingsW, text='Разрешение экрана:', font=('Arial', 13), bg='white', fg='blue').grid(row=0, column=0, stick='s', padx=5, pady=5)
    tk.Entry(settingsW, justify=tk.CENTER, font=('Arial', 15), width=6, bg='white', fg='blue').grid(row=1, column=0,stick='w', padx=5, pady=5)
    tk.Label(settingsW, text='x', font=('Arial', 13), bg='white', fg='blue').grid(row=0, column=1, stick='s', padx=5, pady=5)
    tk.Entry(settingsW, justify=tk.CENTER, font=('Arial', 15), width=6, bg='white', fg='blue').grid(row=1, column=0,stick='w', padx=5, pady=5)
    tk.Button(settingsW,justify=tk.CENTER, text='Авто', bd=5, font=('Arial', 13), bg='white', fg='blue', command = settings).grid(row=1, column=1, stick='wens', padx=5, pady=5)

    tk.Label(settingsW, text='цвет текста:', font=('Arial', 13), bg='white', fg='blue').grid(row=0, column=1, stick='s', padx=5, pady=5)
    tk.Label(settingsW, text='цвет фона:', font=('Arial', 13), bg='white', fg='blue').grid(row=0, column=1, stick='s', padx=5, pady=5)

    tk.Label(settingsW, text='размещение окон:', font=('Arial', 13), bg='white', fg='blue').grid(row=0, column=1, stick='s', padx=5, pady=5)

    settingsW.mainloop()

mainW = tk.Tk()
mainW.geometry(f'210x100+1000+400')
mainW['bg'] = 'white'
mainW.title('Menu')
mainW.wm_attributes('-topmost', 1)

tk.Button(mainW,justify=tk.CENTER, text='Старт', bd=5, font=('Arial', 13), bg='white', fg='blue', command = start).grid(row=0, column=0,columnspan=2, stick='wens', padx=5, pady=5)
tk.Button(mainW,justify=tk.CENTER, text='Рецепты', bd=5, font=('Arial', 13), bg='white', fg='blue', command = recipeF).grid(row=1, column=0, stick='wens', padx=5, pady=5)
tk.Button(mainW,justify=tk.CENTER, text='Настройки', bd=5, font=('Arial', 13), bg='white', fg='blue', command = settings).grid(row=1, column=1, stick='wens', padx=5, pady=5)


mainW.mainloop()
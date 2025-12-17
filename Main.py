import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import ttk
import json
import Calculate
import Draw


class WindowManager:
    """Класс для управления окнами и навигацией"""
    
    def __init__(self):
        # Цветовая схема
        self.colors = {
            'bg_main': '#2C3E50',      # Темно-синий фон
            'bg_secondary': '#34495E',  # Светлее для элементов
            'bg_button': '#3498DB',     # Синий для кнопок
            'bg_button_hover': '#2980B9', # Темнее при наведении
            'text_primary': '#ECF0F1',   # Светлый текст
            'text_secondary': '#BDC3C7', # Серый текст
            'accent': '#E74C3C',        # Красный акцент
            'success': '#27AE60'        # Зеленый для успеха
        }
        
        # Шрифты
        self.fonts = {
            'title': ('Arial', 18, 'bold'),
            'heading': ('Arial', 14, 'bold'),
            'normal': ('Arial', 11),
            'small': ('Arial', 9)
        }
        
        self.root = None
        self.current_window = None
        
    def create_main_window(self):
        """Создает главное окно приложения"""
        self.root = tk.Tk()
        self.root.geometry('350x250+1000+400')
        self.root['bg'] = self.colors['bg_main']
        self.root.title('Sat2v - Калькулятор Satisfactory')
        self.root.resizable(False, False)
        
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text='Sat2v Calculator', 
            font=self.fonts['title'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        title_label.pack(pady=(20, 15))
        
        # Кнопки меню
        button_frame = tk.Frame(self.root, bg=self.colors['bg_main'])
        button_frame.pack(pady=15)
        
        self.create_styled_button(
            button_frame, 
            'Старт', 
            self.show_calculator_window,
            width=22
        ).pack(pady=6)
        
        self.create_styled_button(
            button_frame, 
            'Рецепты', 
            self.show_recipes_window,
            width=22
        ).pack(pady=6)
        
        self.create_styled_button(
            button_frame, 
            'Настройки', 
            self.show_settings_window,
            width=22
        ).pack(pady=6)
        
        self.current_window = self.root
        return self.root
    
    def create_styled_button(self, parent, text, command, width=15, height=1):
        """Создает стилизованную кнопку"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=self.fonts['normal'],
            bg=self.colors['bg_button'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['bg_button_hover'],
            activeforeground=self.colors['text_primary'],
            relief=tk.RAISED,
            bd=2,
            width=width,
            height=height,
            cursor='hand2'
        )
        return btn
    
    def create_back_button(self, window, callback):
        """Создает кнопку Назад"""
        back_btn = tk.Button(
            window,
            text='← Назад',
            command=callback,
            font=self.fonts['small'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['bg_button'],
            activeforeground=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=1,
            cursor='hand2',
            padx=10,
            pady=5
        )
        return back_btn
    
    def show_calculator_window(self):
        """Показывает окно калькулятора"""
        if self.current_window and self.current_window != self.root:
            self.current_window.destroy()
        
        calc_window = tk.Toplevel(self.root)
        calc_window.geometry('350x380+100+100')
        calc_window['bg'] = self.colors['bg_main']
        calc_window.title('Калькулятор')
        calc_window.resizable(False, False)
        
        # Кнопка Назад
        back_btn = self.create_back_button(calc_window, lambda: self.close_window(calc_window))
        back_btn.pack(anchor='nw', padx=10, pady=10)
        
        # Заголовок
        title = tk.Label(
            calc_window,
            text='Расчет производства',
            font=self.fonts['heading'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        title.pack(pady=(0, 20))
        
        # Форма
        form_frame = tk.Frame(calc_window, bg=self.colors['bg_main'])
        form_frame.pack(pady=10)
        
        # Выбор рецепта
        recipe_label = tk.Label(
            form_frame,
            text='Рецепт:',
            font=self.fonts['normal'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        recipe_label.pack(pady=5)
        
        recipes_list = ['ротор', 'винт', 'железный прут', 'железный слиток']
        recipe_combo = ttk.Combobox(
            form_frame,
            values=recipes_list,
            font=self.fonts['normal'],
            state='readonly',
            width=20
        )
        recipe_combo.pack(pady=5)
        recipe_combo.current(0)
        
        # Выход в минуту
        output_label = tk.Label(
            form_frame,
            text='Выход в минуту:',
            font=self.fonts['normal'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        output_label.pack(pady=(15, 5))
        
        output_entry = tk.Entry(
            form_frame,
            justify=tk.CENTER,
            font=self.fonts['normal'],
            width=15,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            relief=tk.SUNKEN,
            bd=2
        )
        output_entry.pack(pady=5)
        output_entry.insert(0, '60')
        
        # Кнопка расчета
        def calculate():
            try:
                recipe = recipe_combo.get()
                output = int(output_entry.get())
                if output <= 0:
                    raise ValueError("Выход должен быть положительным числом")
                
                # Выполняем расчет
                result = Calculate.calculate(recipe, output)
                
                if result:
                    error_label.config(text="Расчет выполнен! Открывается чертеж...", fg=self.colors['success'])
                    calc_window.update()
                    
                    # Визуализируем результат
                    Draw.draw(result, show=True)
                else:
                    error_label.config(text="Ошибка: рецепт не найден", fg=self.colors['accent'])
                    
            except ValueError as e:
                error_label.config(text=f"Ошибка: введите число", fg=self.colors['accent'])
            except Exception as e:
                error_label.config(text=f"Ошибка: {str(e)}", fg=self.colors['accent'])
        
        calc_btn = self.create_styled_button(
            form_frame,
            'Рассчитать',
            calculate,
            width=18
        )
        calc_btn.pack(pady=15)
        
        # Метка для ошибок
        error_label = tk.Label(
            form_frame,
            text='',
            font=self.fonts['small'],
            bg=self.colors['bg_main'],
            fg=self.colors['accent']
        )
        error_label.pack(pady=5)
        
        self.current_window = calc_window
        calc_window.transient(self.root)
        calc_window.grab_set()
    
    def show_recipes_window(self):
        """Показывает окно рецептов"""
        if self.current_window and self.current_window != self.root:
            self.current_window.destroy()
        
        recipes_window = tk.Toplevel(self.root)
        recipes_window.geometry('600x500+100+100')
        recipes_window['bg'] = self.colors['bg_main']
        recipes_window.title('Рецепты')
        recipes_window.resizable(False, False)
        
        # Кнопка Назад
        back_btn = self.create_back_button(recipes_window, lambda: self.close_window(recipes_window))
        back_btn.pack(anchor='nw', padx=10, pady=10)
        
        # Заголовок
        title = tk.Label(
            recipes_window,
            text='База рецептов',
            font=self.fonts['heading'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        title.pack(pady=(0, 15))
        
        # Загрузка рецептов
        try:
            with open('recipes.json', 'r', encoding='utf-8') as file:
                recipes = json.load(file)
            
            # Создание текстового виджета с прокруткой
            text_frame = tk.Frame(recipes_window, bg=self.colors['bg_secondary'])
            text_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget = tk.Text(
                text_frame,
                font=self.fonts['normal'],
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                yscrollcommand=scrollbar.set,
                wrap=tk.WORD,
                padx=10,
                pady=10,
                relief=tk.FLAT
            )
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=text_widget.yview)
            
            # Вывод рецептов
            for recipe_name, recipe_data in recipes.items():
                text_widget.insert(tk.END, f"📦 {recipe_name.upper()}\n", 'title')
                text_widget.insert(tk.END, f"   Здание: {recipe_data['building']}\n", 'normal')
                text_widget.insert(tk.END, f"   Выход: {recipe_data['output']} шт.\n", 'normal')
                text_widget.insert(tk.END, "   Ингредиенты:\n", 'normal')
                for ing, amount in recipe_data['ingredients'].items():
                    text_widget.insert(tk.END, f"      • {ing}: {amount}\n", 'normal')
                text_widget.insert(tk.END, "\n", 'normal')
            
            text_widget.tag_config('title', font=self.fonts['heading'], foreground=self.colors['text_primary'])
            text_widget.tag_config('normal', font=self.fonts['normal'], foreground=self.colors['text_secondary'])
            text_widget.config(state=tk.DISABLED)
            
        except FileNotFoundError:
            error_label = tk.Label(
                recipes_window,
                text='Файл recipes.json не найден!',
                font=self.fonts['normal'],
                bg=self.colors['bg_main'],
                fg=self.colors['accent']
            )
            error_label.pack(pady=50)
        
        self.current_window = recipes_window
        recipes_window.transient(self.root)
        recipes_window.grab_set()
    
    def show_settings_window(self):
        """Показывает окно настроек"""
        if self.current_window and self.current_window != self.root:
            self.current_window.destroy()
        
        settings_window = tk.Toplevel(self.root)
        settings_window.geometry('420x450+100+100')
        settings_window['bg'] = self.colors['bg_main']
        settings_window.title('Настройки')
        settings_window.resizable(False, False)
        
        # Кнопка Назад
        back_btn = self.create_back_button(settings_window, lambda: self.close_window(settings_window))
        back_btn.pack(anchor='nw', padx=10, pady=10)
        
        # Заголовок
        title = tk.Label(
            settings_window,
            text='Настройки',
            font=self.fonts['heading'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        title.pack(pady=(0, 20))
        
        # Форма настроек
        form_frame = tk.Frame(settings_window, bg=self.colors['bg_main'])
        form_frame.pack(pady=10)
        
        # Разрешение экрана
        resolution_label = tk.Label(
            form_frame,
            text='Разрешение экрана:',
            font=self.fonts['normal'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        resolution_label.pack(pady=10)
        
        resolution_frame = tk.Frame(form_frame, bg=self.colors['bg_main'])
        resolution_frame.pack()
        
        width_entry = tk.Entry(
            resolution_frame,
            justify=tk.CENTER,
            font=self.fonts['normal'],
            width=8,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary']
        )
        width_entry.pack(side=tk.LEFT, padx=5)
        width_entry.insert(0, '1920')
        
        tk.Label(
            resolution_frame,
            text='x',
            font=self.fonts['normal'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=5)
        
        height_entry = tk.Entry(
            resolution_frame,
            justify=tk.CENTER,
            font=self.fonts['normal'],
            width=8,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary']
        )
        height_entry.pack(side=tk.LEFT, padx=5)
        height_entry.insert(0, '1080')
        
        def auto_resolution():
            """Автоматическое определение разрешения"""
            settings_window.update_idletasks()
            width = settings_window.winfo_screenwidth()
            height = settings_window.winfo_screenheight()
            width_entry.delete(0, tk.END)
            width_entry.insert(0, str(width))
            height_entry.delete(0, tk.END)
            height_entry.insert(0, str(height))
        
        auto_btn = tk.Button(
            resolution_frame,
            text='Авто',
            command=auto_resolution,
            font=self.fonts['small'],
            bg=self.colors['bg_button'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['bg_button_hover'],
            cursor='hand2',
            padx=10
        )
        auto_btn.pack(side=tk.LEFT, padx=5)
        
        # Информация
        info_label = tk.Label(
            form_frame,
            text='Другие настройки в разработке...',
            font=self.fonts['small'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_secondary']
        )
        info_label.pack(pady=30)
        
        self.current_window = settings_window
        settings_window.transient(self.root)
        settings_window.grab_set()
    
    def close_window(self, window):
        """Закрывает дочернее окно и возвращает фокус на главное"""
        window.destroy()
        self.current_window = self.root
        if self.root:
            self.root.deiconify()
            self.root.lift()
    
    def run(self):
        """Запускает приложение"""
        if self.root:
            self.root.mainloop()


# Инициализация и запуск
if __name__ == '__main__':
    app = WindowManager()
    app.create_main_window()
    app.run()
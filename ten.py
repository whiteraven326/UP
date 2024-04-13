import tkinter as tk
import sys
from t2 import Tennis
from t1 import TennisSolo


class GameMenu:
    def __init__(self, master):
        self.master = master
        master.title("Меню игры")
        master.geometry("600x670")
        master.geometry(f"+{(master.winfo_screenwidth() - 670) // 2}+{(master.winfo_screenheight() - 670) // 2}")
        master.configure(bg="#5F9EA0")
        master.resizable(False, False)
        master.iconbitmap('ico.ico')

        self.menu_visible = True  # Флаг для отслеживания состояния меню
        self.instructions_visible = False  # Флаг для отслеживания состояния инструкций

        self.title_label = tk.Label(master, text="Игра Теннис", font=("Comic Sans MS", 55, "bold"), bg="#5F9EA0")
        self.title_label.pack(pady=50)  # Создаем и размещаем метку с заголовком в главном окне
        # с некоторыми параметрами настройки

        self.start_button = tk.Button(master, text="Играть", font=("Comic Sans MS", 16, "bold"), fg="#1a1a1a",
                                      bg="#6495ED", width=23, height=1, command=self.show_game_options)
        self.start_button.pack(pady=10)  # Создаем и размещаем кнопку "Играть" в главном окне
        # с некоторыми параметрами настройки

        self.instructions_button = tk.Button(master, text="Правила управления", font=("Comic Sans MS", 16, "bold"),
                                             fg="#1a1a1a", bg="#6495ED", width=23, height=1,
                                             command=self.toggle_instructions)
        self.instructions_button.pack(pady=10)  # Создаем и размещаем кнопку "Правила игры" в главном окне
        # с некоторыми параметрами настройки

        self.quit_button = tk.Button(master, text="Выход из игры", font=("Comic Sans MS", 16, "bold"), fg="#1a1a1a",
                                     bg="#6495ED", width=23, height=1, command=self.quit_game)
        self.quit_button.pack(pady=10)  # Создаем и размещаем кнопку "Выход из игры" в главном окне
        # с некоторыми параметрами настройки

        self.game_window_open = False  # Флаг для отслеживания состояния окна игры

        self.instructions_label = tk.Label(master, text="", font=("Comic Sans MS", 16, "bold"), fg="#fff", bg="#1a1a1a")
        self.return_button = tk.Button(master, text="Вернуться в главное меню", font=("Comic Sans MS", 16, "bold"),
                                       fg="#1a1a1a", bg="#6495ED", width=23, height=1, command=self.return_to_menu)
        self.return_button.pack_forget()

        self.single_player_button = tk.Button(master, text="Одиночная игра", font=("Comic Sans MS", 16, "bold"),
                                              fg="#1a1a1a", bg="#6495ED", width=23, height=1,
                                              command=self.start_single_player_game)
        self.single_player_button.pack_forget()

        self.multiplayer_button = tk.Button(master, text="Игра вдвоём", font=("Comic Sans MS", 16, "bold"),
                                            fg="#1a1a1a", bg="#6495ED", width=23, height=1,
                                            command=self.start_multiplayer_game)
        self.multiplayer_button.pack_forget()

    def show_game_options(self):
        self.start_button.pack_forget()
        self.instructions_button.pack_forget()
        self.quit_button.pack_forget()

        self.single_player_button.pack(pady=10)
        self.multiplayer_button.pack(pady=10)
        self.return_button.pack(pady=100)

    def toggle_instructions(self):
        if self.menu_visible:
            self.menu_visible = False
            self.instructions_visible = True
            self.title_label.pack_forget()
            self.start_button.pack_forget()
            self.instructions_button.pack_forget()
            self.quit_button.pack_forget()
            self.instructions_label.config(text="Для управления ракетками в игре используйте английскую раскладку\n"
                                                "клавиатуры.\n "
                                                "Одиночная игра:\n"
                                                "W - переместить ракетку вверх\n"
                                                "S - переместить ракетку вниз\n"
                                                " Игра вдвоем:\n"
                                                "игрок первый:\n"
                                                "W - переместить ракетку вверх\n"
                                                "S - переместить ракетку вниз\n"
                                                "игрок второй:\n"
                                                "стрелка вверх - переместить ракетку вверх\n"
                                                "стрелка вниз - переместить ракетку вниз\n"
                                                "Для того, чтобы поставить на паузу нажмите P, Esc - вернуться в меню."
                                           , font=("Helvetica", 12), fg="#1a1a1a", bg="#6495ED", width=60, height=15,
                                           relief='solid', bd=1)
            self.instructions_label.pack(pady=60)
            self.return_button.pack(pady=100)
        else:
            self.menu_visible = True
            self.instructions_visible = False
            self.title_label.pack()
            self.start_button.pack()
            self.instructions_button.pack()
            self.quit_button.pack()
            self.instructions_label.pack_forget()
            self.return_button.pack_forget()
            self.return_to_menu()  # Вызываем функцию return_to_menu при скрытии инструкций

    def start_single_player_game(self):
        if not self.game_window_open:  # Проверяем, что окно игры не открыто
            self.master.withdraw()  # Скрываем окно меню
            game_window = tk.Toplevel()  # Создаем новое окно для игры в одиночку
            game_window.protocol("WM_DELETE_WINDOW", self.return_to_menu)  # Обрабатываем событие закрытия окна игры
            TennisSolo(game_window)
            self.game_window_open = True  # Устанавливаем флаг, что окно игры открыто

    def start_multiplayer_game(self):
        if not self.game_window_open:  # Проверяем, что окно игры не открыто
            self.master.withdraw()  # Скрываем окно меню
            game_window = tk.Toplevel()  # Создаем новое окно для многопользовательской игры
            game_window.protocol("WM_DELETE_WINDOW", self.return_to_menu)  # Обрабатываем событие закрытия окна игры
            Tennis(game_window)
            self.game_window_open = True  # Устанавливаем флаг, что окно игры открыто

    def return_to_menu(self):
        # Логика для возвращения в меню при закрытии окна игры
        self.game_window_open = False
        self.master.deiconify()  # Восстанавливаем окно меню при закрытии окна игры

        # Центрирование элементов интерфейса
        self.title_label.pack(pady=50)
        self.start_button.pack(pady=10)
        self.instructions_button.pack(pady=10)
        self.quit_button.pack(pady=10)
        self.single_player_button.pack_forget()
        self.multiplayer_button.pack_forget()
        self.instructions_label.pack_forget()
        self.return_button.pack_forget()

    def quit_game(self):
        self.master.destroy()
        sys.exit()


root = tk.Tk()
menu = GameMenu(root)
root.mainloop()

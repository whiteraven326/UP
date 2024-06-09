import tkinter as tk
from tkinter import Canvas, PhotoImage, ALL, messagebox
import random
import sys


class Menu:
    def __init__(self, master):
        self.master = master
        master.title("Меню игры")
        master.configure(bg="#5F9EA0")
        master.geometry("600x670")
        master.geometry(f"+{(master.winfo_screenwidth() - 670) // 2}+{(master.winfo_screenheight() - 670) // 2}")
        master.resizable(False, False)
        master.iconbitmap('Benefit/ico.ico')
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.menu_visible = True
        self.instructions_visible = False
        self.title_label = tk.Label(master, text="Игра Теннис", font=("Comic Sans MS", 55, "bold"), bg="#5F9EA0")
        self.title_label.pack(pady=50)
        self.start_button = tk.Button(master, text="Играть", font=("Comic Sans MS", 16, "bold"), fg="#1a1a1a",
                                      bg="#6495ED", width=23, height=1, command=self.show_game_options)
        self.start_button.pack(pady=10)
        self.instructions_button = tk.Button(master, text="Правила управления", font=("Comic Sans MS", 16, "bold"),
                                             fg="#1a1a1a", bg="#6495ED", width=23, height=1,
                                             command=self.toggle_instructions)
        self.instructions_button.pack(pady=10)
        self.quit_button = tk.Button(master, text="Выход из игры", font=("Comic Sans MS", 16, "bold"), fg="#1a1a1a",
                                     bg="#6495ED", width=23, height=1, command=self.quit_game)
        self.quit_button.pack(pady=10)
        self.game_window_open = False
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
            self.instructions_label.config(text="Для управления в игре используйте английскую раскладку клавиатуры.\n "
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
                                                "Для того, чтобы поставить на паузу нажмите Q, Esc - вернуться в меню.",
                                           font=("Helvetica", 12), fg="#1a1a1a", bg="#6495ED", width=60, height=15,
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
            self.return_to_menu()

    def start_single_player_game(self):
        if not self.game_window_open:
            self.master.withdraw()
            game_window = tk.Toplevel()
            game_window.protocol("WM_DELETE_WINDOW", self.return_to_menu)
            screen_width = game_window.winfo_screenwidth()
            screen_height = game_window.winfo_screenheight()
            center_x = screen_width // 2
            center_y = screen_height // 2
            window_width = 900
            window_height = 540
            x = center_x - window_width // 2
            y = center_y - window_height // 2
            game_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            TennisSolo(game_window)
            self.game_window_open = True

    def start_multiplayer_game(self):
        if not self.game_window_open:
            self.master.withdraw()
            game_window = tk.Toplevel()
            game_window.protocol("WM_DELETE_WINDOW", self.return_to_menu)
            screen_width = game_window.winfo_screenwidth()
            screen_height = game_window.winfo_screenheight()
            center_x = screen_width // 2
            center_y = screen_height // 2
            window_width = 900
            window_height = 540
            x = center_x - window_width // 2
            y = center_y - window_height // 2
            game_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            Tennis(game_window)
            self.game_window_open = True

    def return_to_menu(self):
        self.game_window_open = False
        self.menu_visible = True
        self.instructions_visible = False
        self.master.deiconify()
        self.title_label.pack(pady=50)
        self.start_button.pack(pady=10)
        self.instructions_button.pack(pady=10)
        self.quit_button.pack(pady=10)
        self.single_player_button.pack_forget()
        self.multiplayer_button.pack_forget()
        self.instructions_label.pack_forget()
        self.return_button.pack_forget()

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы хотите закрыть игру?"):
            self.master.destroy()
            sys.exit()

    def quit_game(self):
        self.master.destroy()
        sys.exit()


class BaseTennis:
    def __init__(self, root, title, bg_image_file):
        self.root = root
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.iconbitmap('Benefit/ico.ico')
        self.game_over_image = None
        self.width = 900
        self.height = 540
        self.bg_image = PhotoImage(file=bg_image_file)
        self.c = Canvas(self.root, width=self.width, height=self.height)
        self.c.create_image(0, 0, image=self.bg_image, anchor='nw')
        self.c.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.c.focus_force()
        self.p_speed = 20
        self.speed_l_p = 0
        self.speed_r_p = 0
        self.p_l = self.c.create_line(5, 0, 5, 140, width=10, fill="#EC3D3D")
        self.p_r = self.c.create_line(895, 0, 895, 140, width=10, fill="#2A2CEC")
        self.speed_up = 1.01
        self.speed_max = 100
        self.r = 30
        self.speed_init = 17
        self.speed_x = self.speed_init
        self.speed_y = self.speed_init
        self.ball = self.c.create_oval(435, 255, 465, 285, fill="#ECD931")
        self.bl_score = 0
        self.red_score = 0
        self.right_line_distance = 892
        self.p_blue_text = self.c.create_text(694, 33, text=self.bl_score, font="Arial 29", fill="#FEFFFC")
        self.p_red_text = self.c.create_text(209, 33, text=self.red_score, font="Arial 29", fill="#FEFFFC")
        self.countdown_text = self.c.create_text(450, 270, text="", font="Helvetica 65", fill="black")
        self.pause = False
        self.countdown_paused = False
        self.countdown_time = 5
        self.pause = False

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы хотите закрыть игру?"):
            self.root.destroy()
            sys.exit()
        else:
            self.c.focus_force()

    @staticmethod
    def load_menu():
        global root, menu
        root = tk.Tk()
        menu = Menu(root)
        root.mainloop()

    def end_game(self):
        self.c.delete(ALL)
        self.c.create_image(self.width / 2, self.height/2, image=self.game_over_image)
        self.c.pack()


class TennisSolo(BaseTennis):
    def __init__(self, root):
        super().__init__(root, "Теннис_Соло", "Benefit/ten.png")
        self.countdown(self.countdown_time)
        self.c.bind("<KeyPress>", self.movement_handler)
        self.c.bind("<KeyRelease>", self.stop_pad)
        self.Kp = 0.1

    def countdown(self, num):
        if self.pause:
            self.countdown_paused = True
            self.countdown_time = num
            return
        self.countdown_paused = False
        if num > 0:
            self.c.itemconfig(self.countdown_text, text=str(num))
            self.root.after(1000, self.countdown, num - 1)
        else:
            self.c.itemconfig(self.countdown_text, text="")
            self.start_game()

    def start_game(self):
        self.c.itemconfig(self.countdown_text, text="")
        self.spawn_ball()
        self.main()

    def main(self):
        if not self.pause:
            self.move_ball()
            self.move_pads()
        self.c.after(20, self.main)

    def score(self, player):
        if player == "right":
            self.bl_score += 1
            self.c.itemconfig(self.p_blue_text, text=self.bl_score)
            if self.bl_score == 5:
                self.game_over_image = PhotoImage(file="Benefit/los_solo.png")
                self.end_game()
        else:
            self.red_score += 1
            self.c.itemconfig(self.p_red_text, text=self.red_score)
            if self.red_score == 5:
                self.game_over_image = PhotoImage(file="Benefit/win_s.png")
                self.end_game()

    def spawn_ball(self):
        self.speed_x = -(self.speed_x * -self.speed_init) / abs(self.speed_x)
        self.c.coords(self.ball, self.width / 2 - self.r / 2,
                      self.height / 2 - self.r / 2,
                      self.width / 2 + self.r / 2,
                      self.height / 2 + self.r / 2)

    def bounce(self, action):
        if action == "strike":
            self.speed_y = random.randrange(-10, 10)
            if abs(self.speed_x) < self.speed_max:
                self.speed_x *= -self.speed_up
            else:
                self.speed_x = -self.speed_x
        else:
            self.speed_y = -self.speed_y

    def move_ball(self):
        ball_coords = self.c.coords(self.ball)
        if not ball_coords:
            return
        ball_left, ball_top, ball_right, ball_bot = self.c.coords(self.ball)
        ball_center = (ball_top + ball_bot) / 2
        if ball_right + self.speed_x < self.right_line_distance and \
                ball_left + self.speed_x > 8:
            self.c.move(self.ball, self.speed_x, self.speed_y)
        elif ball_right == self.right_line_distance or ball_left == 8:
            if ball_right > self.width / 2:
                if self.c.coords(self.p_r)[1] < ball_center < self.c.coords(self.p_r)[3]:
                    self.bounce("strike")
                else:
                    self.score("left")
                    self.spawn_ball()
            else:
                if self.c.coords(self.p_l)[1] < ball_center < self.c.coords(self.p_l)[3]:
                    self.bounce("strike")
                else:
                    self.score("right")
                    self.spawn_ball()
        else:
            if ball_right > self.width / 2:
                self.c.move(self.ball, self.right_line_distance - ball_right, self.speed_y)
            else:
                self.c.move(self.ball, -ball_left + 8, self.speed_y)
        if ball_top + self.speed_y < 0 or ball_bot + self.speed_y > self.height:
            self.bounce("ricochet")

    def move_pads(self):
        left_pad_coords = self.c.coords(self.p_l)
        if len(left_pad_coords) > 1:
            left_pad_top = left_pad_coords[1]
            left_pad_bot = left_pad_coords[3]
        else:
            left_pad_top = 0
            left_pad_bot = 0
        right_pad_coords = self.c.coords(self.p_r)
        if len(right_pad_coords) > 1:
            right_pad_top = right_pad_coords[1]
            right_pad_bot = right_pad_coords[3]
        else:
            right_pad_top = 0
            right_pad_bot = 0
        ball_coords = self.c.coords(self.ball)
        if ball_coords:
            ball_y = (ball_coords[1] + ball_coords[3]) / 2
        else:
            ball_y = 0
        bot_pad_y = (right_pad_top + right_pad_bot) / 2
        error = ball_y - bot_pad_y
        self.speed_r_p = self.Kp * error
        if self.speed_r_p > self.p_speed:
            self.speed_r_p = self.p_speed
        elif self.speed_r_p < -self.p_speed:
            self.speed_r_p = -self.p_speed
        new_right_pad_top = right_pad_top + self.speed_r_p
        new_right_pad_bot = right_pad_bot + self.speed_r_p
        if new_right_pad_top < 0:
            diff = 0 - new_right_pad_top
            new_right_pad_top += diff
            new_right_pad_bot += diff
        elif new_right_pad_bot > self.height:
            diff = new_right_pad_bot - self.height
            new_right_pad_top -= diff
            new_right_pad_bot -= diff
        self.c.coords(self.p_r,
                      self.width - 8 / 2, new_right_pad_top,
                      self.width - 8 / 2, new_right_pad_bot)
        if left_pad_top + self.speed_l_p >= 0 and left_pad_bot + self.speed_l_p <= self.height:
            self.c.move(self.p_l, 0, self.speed_l_p)

    def handle_input(self, event, is_key_press):
        key = event.keysym.lower()
        if key in {"w", "s"}:
            self.speed_l_p = self.p_speed if (key == "s" and is_key_press) else (
                -self.p_speed if key == "w" and is_key_press else 0)
        elif is_key_press:
            if key == "q":
                self.pause = not self.pause
                self.c.delete("pause")
                if self.pause:
                    self.c.create_rectangle(0, 0, 900, 540, fill="black", stipple="gray75", tags="pause")
                    self.c.create_text(442, 255, text="Игра на паузе", font=("Comic Sans MS", 75, "bold"), fill="red",
                                       anchor="center", tags="pause")
                    if self.countdown_paused:
                        self.countdown(self.countdown_time)
                else:
                    self.c.delete("pause")
                    if self.countdown_paused:
                        self.countdown(self.countdown_time)
            elif key == "escape":
                self.root.destroy()
                self.root.after(100, self.load_menu)

    def movement_handler(self, event):
        self.handle_input(event, True)

    def stop_pad(self, event):
        self.handle_input(event, False)


class Tennis(BaseTennis):
    def __init__(self, root):
        super().__init__(root, "Теннис_Вдвоём", "Benefit/ten.png")
        self.countdown(self.countdown_time)
        self.c.bind("<KeyPress>", self.movement_handler)
        self.c.bind("<KeyRelease>", self.stop_pad)

    def countdown(self, num):
        if self.pause:
            self.countdown_paused = True
            self.countdown_time = num
            return
        self.countdown_paused = False
        if num > 0:
            self.c.itemconfig(self.countdown_text, text=str(num))
            self.root.after(1000, self.countdown, num - 1)
        else:
            self.c.itemconfig(self.countdown_text, text="")
            self.start_game()

    def start_game(self):
        self.c.itemconfig(self.countdown_text, text="")
        self.reset_ball()
        self.main()

    def main(self):
        if not self.pause:
            self.move_ball()
            self.move_pads()
        self.c.after(20, self.main)

    def move_ball(self):
        ball_coords = self.c.coords(self.ball)
        if ball_coords:
            ball_left, ball_top, ball_right, ball_bot = ball_coords
            ball_center = (ball_top + ball_bot) / 2
            if ball_right + self.speed_x < self.right_line_distance and \
                    ball_left + self.speed_x > 8:
                self.c.move(self.ball, self.speed_x, self.speed_y)
            elif ball_right == self.right_line_distance or ball_left == 8:
                if ball_right > self.width / 2:
                    if self.c.coords(self.p_r)[1] < ball_center < self.c.coords(self.p_r)[3]:
                        self.speed_y = random.randrange(-10, 10)
                        if abs(self.speed_x) < self.speed_max:
                            self.speed_x *= -self.speed_up
                        else:
                            self.speed_x = -self.speed_x
                    else:
                        self.score("red")
                        self.reset_ball()
                else:
                    if self.c.coords(self.p_l)[1] < ball_center < self.c.coords(self.p_l)[3]:
                        self.speed_y = random.randrange(-10, 10)
                        if abs(self.speed_x) < self.speed_max:
                            self.speed_x *= -self.speed_up
                        else:
                            self.speed_x = -self.speed_x
                    else:
                        self.score("green")
                        self.reset_ball()
            else:
                if ball_right > self.width / 2:
                    self.c.move(self.ball, self.right_line_distance - ball_right, self.speed_y)
                else:
                    self.c.move(self.ball, -ball_left + 8, self.speed_y)
            if ball_top + self.speed_y < 0 or ball_bot + self.speed_y > self.height:
                self.speed_y = -self.speed_y

    def reset_ball(self):
        self.speed_x = -(self.speed_x * -self.speed_init) / abs(self.speed_x)
        self.c.coords(self.ball, self.width / 2 - self.r / 2,
                      self.height / 2 - self.r / 2,
                      self.width / 2 + self.r / 2,
                      self.height / 2 + self.r / 2)

    def move_pads(self):
        pads = {self.p_l: self.speed_l_p,
                self.p_r: self.speed_r_p}
        for pad in pads:
            pad_coords = self.c.coords(pad)
            if pad_coords:
                self.c.move(pad, 0, pads[pad])
                if pad_coords[1] < 0:
                    self.c.move(pad, 0, -pad_coords[1])
                elif pad_coords[3] > self.height:
                    self.c.move(pad, 0, self.height - pad_coords[3])

    def handle_input(self, event, is_key_press):
        key = event.keysym.lower()
        if key in ("w", "s"):
            self.speed_l_p = self.p_speed if key == "s" else -self.p_speed
        elif key in ("up", "down"):
            self.speed_r_p = self.p_speed if key == "down" else -self.p_speed
        elif is_key_press:
            if key == "q":
                self.pause = not self.pause
                self.c.delete("pause")
                if self.pause:
                    self.c.create_rectangle(0, 0, 900, 540, fill="black", stipple="gray75", tags="pause")
                    self.c.create_text(442, 255, text="Игра на паузе", font=("Comic Sans MS", 75, "bold"), fill="red",
                                       anchor="center", tags="pause")
                    if self.countdown_paused:
                        self.countdown(self.countdown_time)
                else:
                    self.c.delete("pause")
                    if self.countdown_paused:
                        self.countdown(self.countdown_time)
            elif key == "escape":
                self.root.destroy()
                self.root.after(100, self.load_menu)
        if not is_key_press:
            if key in ("w", "s"):
                self.speed_l_p = 0
            elif key in ("up", "down"):
                self.speed_r_p = 0

    def movement_handler(self, event):
        self.handle_input(event, True)

    def stop_pad(self, event):
        self.handle_input(event, False)

    def score(self, player):
        if player == "green":
            self.bl_score += 1
            self.c.itemconfig(self.p_blue_text, text=self.bl_score)
        else:
            self.red_score += 1
            self.c.itemconfig(self.p_red_text, text=self.red_score)
        if self.bl_score == 5:
            self.game_over_image = PhotoImage(file="Benefit/win_bl.png")
            self.end_game()
        elif self.red_score == 5:
            self.game_over_image = PhotoImage(file="Benefit/win_red.png")
            self.end_game()


root = tk.Tk()
menu = Menu(root)
root.mainloop()

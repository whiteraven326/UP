from tkinter import *
import random
from tkinter import Canvas, PhotoImage


class TennisSolo:
    def __init__(self, root):
        self.root = root
        self.root.title("Теннис_Соло")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.resizable(False, False)
        self.root.iconbitmap('ico.ico')
        self.game_over_image = None
        self.width = 900
        self.height = 540
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.bg_image = PhotoImage(file="поле5.png")
        self.c = Canvas(self.root, width=self.width, height=self.height)
        self.c.create_image(0, 0, image=self.bg_image, anchor='nw')
        self.c.pack()
        self.p_w = 8
        self.p_h = 140
        self.PAD_WIDTH = 10  # переменная для ширины ракеток
        self.p_speed = 20
        self.speed_l_p = 0
        self.speed_r_p = 0

        self.p_l = self.c.create_line(self.p_w / 2, 0, self.p_w / 2, self.p_h, width=self.PAD_WIDTH, fill="#FF0104")
        self.p_r = self.c.create_line(self.width - self.p_w / 2, 0, self.width - self.p_w / 2, self.p_h,
                                      width=self.PAD_WIDTH, fill="#3BFF08")
        # Константы для мяча
        self.speed_up = 1.01
        self.speed_max = 100
        self.r = 30
        self.speed_init = 20
        self.speed_x = self.speed_init
        self.speed_y = self.speed_init
        self.change_x = 20
        self.change_y = 0
        self.Kp = 0.1

        self.BALL = self.c.create_oval(self.width / 2 - self.r / 2,
                                       self.height / 2 - self.r / 2,
                                       self.width / 2 + self.r / 2,
                                       self.height / 2 + self.r / 2, fill="#FEFFFC")

        self.score_1 = 0
        self.score_2 = 0
        self.right_line_distance = self.width - self.p_w
        self.p_1_text = self.c.create_text(697, 27, text=self.score_1, font="Arial 20", fill="#FEFFFC")
        self.p_2_text = self.c.create_text(212, 27, text=self.score_2, font="Arial 20", fill="#FEFFFC")
        self.countdown_text = self.c.create_text(self.width / 2, self.height / 2, text="", font="Helvetica 65 bold",
                                                 fill="black")

        self.c.focus_set()
        self.c.bind("<KeyPress>", self.movement_handler)
        self.c.bind("<KeyRelease>", self.stop_pad)
        # Запуск игры
        self.countdown(3)
        self.is_paused = False

    def on_closing(self):
        pass

    def start_game(self):
        self.c.itemconfig(self.countdown_text, text="")
        self.spawn_ball()
        self.main()

    def countdown(self, num):
        # Отсчет до начала игры
        if num > 0:
            self.c.itemconfig(self.countdown_text, text=str(num))
            self.root.after(1000, self.countdown, num - 1)
        else:
            self.c.itemconfig(self.countdown_text, text="")
            self.root.after(1000, self.start_game)

    def update_score(self, player):
        if player == "right":
            self.score_1 += 1
            self.c.itemconfig(self.p_1_text, text=self.score_1)
            if self.score_1 == 5:
                self.game_over_image = PhotoImage(file="lose.png")
                self.end_game("     ВЫ\nПРОИГРАЛИ!")

        else:
            self.score_2 += 1
            self.c.itemconfig(self.p_2_text, text=self.score_2)
            if self.score_2 == 5:
                self.game_over_image = PhotoImage(file="win2.png")
                self.end_game("     ВЫ\nПОБЕДИЛИ!")

    def spawn_ball(self):
        self.speed_x = -(self.speed_x * -self.speed_init) / abs(self.speed_x)
        self.c.coords(self.BALL, self.width / 2 - self.r / 2,
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
        ball_coords = self.c.coords(self.BALL)
        if not ball_coords:
            return  # Выход из метода, если координаты мяча отсутствуют
        ball_left, ball_top, ball_right, ball_bot = self.c.coords(self.BALL)
        ball_center = (ball_top + ball_bot) / 2
        if ball_right + self.speed_x < self.right_line_distance and \
                ball_left + self.speed_x > self.p_w:
            self.c.move(self.BALL, self.speed_x, self.speed_y)
        elif ball_right == self.right_line_distance or ball_left == self.p_w:
            if ball_right > self.width / 2:
                if self.c.coords(self.p_r)[1] < ball_center < self.c.coords(self.p_r)[3]:
                    self.bounce("strike")
                else:
                    self.update_score("left")
                    self.spawn_ball()
            else:
                if self.c.coords(self.p_l)[1] < ball_center < self.c.coords(self.p_l)[3]:
                    self.bounce("strike")
                else:
                    self.update_score("right")
                    self.spawn_ball()
        else:
            if ball_right > self.width / 2:
                self.c.move(self.BALL, self.right_line_distance - ball_right, self.speed_y)
            else:
                self.c.move(self.BALL, -ball_left + self.p_w, self.speed_y)
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
        ball_coords = self.c.coords(self.BALL)
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
                      self.width - self.p_w / 2, new_right_pad_top,
                      self.width - self.p_w / 2, new_right_pad_bot)
        if left_pad_top + self.speed_l_p >= 0 and left_pad_bot + self.speed_l_p <= self.height:
            self.c.move(self.p_l, 0, self.speed_l_p)

    def movement_handler(self, event):
        if event.keysym == "w":
            self.speed_l_p = -self.p_speed
        elif event.keysym == "s":
            self.speed_l_p = self.p_speed
        elif event.keysym == "p":
            self.is_paused = not self.is_paused
            self.pause()
        elif event.keysym == "Escape":
            self.root.destroy()  # Закрыть текущее окно
            self.root.after(100, self.load_menu)  # Загрузить меню через небольшую задержку

    @staticmethod
    def load_menu():
        global root, menu
        from ten import GameMenu
        root = Tk()
        menu = GameMenu(root)
        root.mainloop()

    def stop_pad(self, event):
        if event.keysym in {"w", "s"}:
            self.speed_l_p = 0

    def pause(self):
        self.c.delete("pause")
        if self.is_paused:
            self.c.create_rectangle(0, 0, self.width, self.height, fill="black", stipple="gray75", tag="pause")
            self.c.create_text(self.width // 2, self.height // 2, text="Игра на паузе",
                               font=("Comic Sans MS", 75, "bold"), fill="red", anchor="center", tags="pause")

    def end_game(self, message):
        self.c.delete(ALL)  # Удалить все элементы с холста
        self.c.create_image(self.width / 2, self.height/2, image=self.game_over_image)
        self.c.create_text(self.width/3, self.height/3, text=message, font=("Comic Sans MS", 55, "bold"), fill="black")
        self.c.pack()

    def main(self):
        if not self.is_paused:
            self.move_ball()
            self.move_pads()
        self.c.after(20, self.main)


if __name__ == "__main__":
    root = Tk()
    menu = TennisSolo(root)
    root.mainloop()

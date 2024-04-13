from tkinter import *
import random
from tkinter import Canvas, PhotoImage


class TennisSolo:
    def __init__(self, root):
        self.root = root
        self.root.title("Теннис")
        self.root.resizable(False, False)
        self.root.iconbitmap('ico.ico')  # Добавляем иконку
        # Введение основных переменных
        self.WIDTH = 900
        self.HEIGHT = 540
        # Получение ширины и высоты экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Позиционирование окна по центру экрана
        x = (screen_width-self.WIDTH)//2
        y = (screen_height-self.HEIGHT)//2
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

        self.PAD_W = 8
        self.PAD_H = 140
        self.PAD_WIDTH = 10  # переменная для ширины ракеток
        self.BALL_SPEED_UP = 1.01
        self.BALL_MAX_SPEED = 100
        self.BALL_RADIUS = 30
        self.INITIAL_SPEED = 20
        self.BALL_X_SPEED = self.INITIAL_SPEED
        self.BALL_Y_SPEED = self.INITIAL_SPEED
        self.PLAYER_1_SCORE = 0
        self.PLAYER_2_SCORE = 0
        self.right_line_distance = self.WIDTH - self.PAD_W
        self.BALL_X_CHANGE = 20
        self.BALL_Y_CHANGE = 0
        self.PAD_SPEED = 20
        self.LEFT_PAD_SPEED = 0
        self.RIGHT_PAD_SPEED = 0

        self.bg_image = PhotoImage(file="поле5.png")
        # Создание холста для отрисовки игровых объектов
        self.c = Canvas(self.root, width=self.WIDTH, height=self.HEIGHT)
        self.c.create_image(0, 0, image=self.bg_image, anchor='nw')
        self.c.pack()
        self.background_image = None

        self.BALL = self.c.create_oval(self.WIDTH / 2 - self.BALL_RADIUS / 2,
                                       self.HEIGHT / 2 - self.BALL_RADIUS / 2,
                                       self.WIDTH / 2 + self.BALL_RADIUS / 2,
                                       self.HEIGHT / 2 + self.BALL_RADIUS / 2, fill="white")
        self.LEFT_PAD = self.c.create_line(self.PAD_W / 2, 0, self.PAD_W / 2, self.PAD_H, width=self.PAD_WIDTH,
                                           fill="red")
        self.RIGHT_PAD = self.c.create_line(self.WIDTH - self.PAD_W / 2, 0, self.WIDTH - self.PAD_W / 2, self.PAD_H,
                                            width=self.PAD_WIDTH, fill="green")

        self.p_1_text = self.c.create_text(697, 27, text=self.PLAYER_1_SCORE, font="Arial 20", fill="white")

        self.p_2_text = self.c.create_text(212, 27, text=self.PLAYER_2_SCORE, font="Arial 20", fill="white")
        self.countdown_text = self.c.create_text(self.WIDTH / 2, self.HEIGHT / 2, text="", font="Arial 60",
                                                 fill="black")

        self.c.focus_set()
        self.c.bind("<KeyPress>", self.movement_handler)
        self.c.bind("<KeyRelease>", self.stop_pad)
        # Запуск игры
        self.countdown(3)
        self.is_paused = False

    def countdown(self, num):
        # Отсчет до начала игры
        if num > 0:
            self.c.itemconfig(self.countdown_text, text=str(num))
            self.root.after(1000, self.countdown, num - 1)
        else:
            self.c.itemconfig(self.countdown_text, text="")
            self.root.after(1000, self.start_game)

    def start_game(self):
        # Начало игры
        self.c.itemconfig(self.countdown_text, text="")
        self.spawn_ball()
        self.main()

    def update_score(self, player):
        if player == "right":
            self.PLAYER_1_SCORE += 1
            self.c.itemconfig(self.p_1_text, text=self.PLAYER_1_SCORE)
            if self.PLAYER_1_SCORE == 5:
                self.end_game("Вы проиграли!\nНажмите Esc, чтобы вернуться в меню")

        else:
            self.PLAYER_2_SCORE += 1
            self.c.itemconfig(self.p_2_text, text=self.PLAYER_2_SCORE)
            if self.PLAYER_2_SCORE == 5:
                self.end_game("Вы победили!\nНажмите Esc, чтобы вернуться в меню")

    def end_game(self, message):
        self.c.delete(ALL)  # Удалить все элементы с холста
        self.c.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill="#6495ED")
        self.c.create_text(self.WIDTH / 2, self.HEIGHT / 2, text=message, font="Arial 35", fill="black")
        self.c.pack()

    def spawn_ball(self):
        self.BALL_X_SPEED = -(self.BALL_X_SPEED * -self.INITIAL_SPEED) / abs(self.BALL_X_SPEED)
        self.c.coords(self.BALL, self.WIDTH / 2 - self.BALL_RADIUS / 2,
                      self.HEIGHT / 2 - self.BALL_RADIUS / 2,
                      self.WIDTH / 2 + self.BALL_RADIUS / 2,
                      self.HEIGHT / 2 + self.BALL_RADIUS / 2)

    def bounce(self, action):
        if action == "strike":
            self.BALL_Y_SPEED = random.randrange(-10, 10)
            if abs(self.BALL_X_SPEED) < self.BALL_MAX_SPEED:
                self.BALL_X_SPEED *= -self.BALL_SPEED_UP
            else:
                self.BALL_X_SPEED = -self.BALL_X_SPEED
        else:
            self.BALL_Y_SPEED = -self.BALL_Y_SPEED

    def move_ball(self):
        ball_coords = self.c.coords(self.BALL)

        if not ball_coords:
            return  # Выход из метода, если координаты мяча отсутствуют
        ball_left, ball_top, ball_right, ball_bot = self.c.coords(self.BALL)
        ball_center = (ball_top + ball_bot) / 2

        if ball_right + self.BALL_X_SPEED < self.right_line_distance and \
                ball_left + self.BALL_X_SPEED > self.PAD_W:
            self.c.move(self.BALL, self.BALL_X_SPEED, self.BALL_Y_SPEED)
        elif ball_right == self.right_line_distance or ball_left == self.PAD_W:
            if ball_right > self.WIDTH / 2:
                if self.c.coords(self.RIGHT_PAD)[1] < ball_center < self.c.coords(self.RIGHT_PAD)[3]:
                    self.bounce("strike")
                else:
                    self.update_score("left")
                    self.spawn_ball()
            else:
                if self.c.coords(self.LEFT_PAD)[1] < ball_center < self.c.coords(self.LEFT_PAD)[3]:
                    self.bounce("strike")
                else:
                    self.update_score("right")
                    self.spawn_ball()
        else:
            if ball_right > self.WIDTH / 2:
                self.c.move(self.BALL, self.right_line_distance - ball_right, self.BALL_Y_SPEED)
            else:
                self.c.move(self.BALL, -ball_left + self.PAD_W, self.BALL_Y_SPEED)

        if ball_top + self.BALL_Y_SPEED < 0 or ball_bot + self.BALL_Y_SPEED > self.HEIGHT:
            self.bounce("ricochet")

    def move_pads(self):
        left_pad_coords = self.c.coords(self.LEFT_PAD)
        if len(left_pad_coords) > 1:
            left_pad_top = left_pad_coords[1]
            left_pad_bot = left_pad_coords[3]
        else:
            left_pad_top = 0
            left_pad_bot = 0

        right_pad_coords = self.c.coords(self.RIGHT_PAD)
        if len(right_pad_coords) > 1:
            right_pad_top = right_pad_coords[1]
            right_pad_bot = right_pad_coords[3]
        else:
            right_pad_top = 0
            right_pad_bot = 0

        # Получение координат мяча с проверкой их наличия
        ball_coords = self.c.coords(self.BALL)
        if ball_coords:
            ball_y = ball_coords[1] + ball_coords[3]
        else:
            ball_y = 0

        bot_pad_y = right_pad_top + right_pad_bot

        Kp = 0.05
        error = ball_y - bot_pad_y
        self.RIGHT_PAD_SPEED = Kp * error

        if self.RIGHT_PAD_SPEED > self.PAD_SPEED:
            self.RIGHT_PAD_SPEED = self.PAD_SPEED
        elif self.RIGHT_PAD_SPEED < -self.PAD_SPEED:
            self.RIGHT_PAD_SPEED = -self.PAD_SPEED

        new_right_pad_top = right_pad_top + self.RIGHT_PAD_SPEED
        new_right_pad_bot = right_pad_bot + self.RIGHT_PAD_SPEED

        # Проверка и корректировка координат правого пада
        if new_right_pad_top < 0:
            diff = 0 - new_right_pad_top
            new_right_pad_top += diff
            new_right_pad_bot += diff
        elif new_right_pad_bot > self.HEIGHT:
            diff = new_right_pad_bot - self.HEIGHT
            new_right_pad_top -= diff
            new_right_pad_bot -= diff

        self.c.coords(self.RIGHT_PAD,
                      self.WIDTH - self.PAD_W / 2, new_right_pad_top,
                      self.WIDTH - self.PAD_W / 2, new_right_pad_bot)

        self.c.move(self.LEFT_PAD, 0, self.LEFT_PAD_SPEED)

        if left_pad_top + self.LEFT_PAD_SPEED < 0:
            self.LEFT_PAD_SPEED = 0
        elif left_pad_bot + self.LEFT_PAD_SPEED > self.HEIGHT:
            self.LEFT_PAD_SPEED = 0

    def movement_handler(self, event):
        if event.keysym == "w":
            self.LEFT_PAD_SPEED = -self.PAD_SPEED
        elif event.keysym == "s":
            self.LEFT_PAD_SPEED = self.PAD_SPEED
        elif event.keysym == "p":
            self.is_paused = not self.is_paused
            self.show_pause_screen()
        elif event.keysym == "Escape":
            self.root.destroy()  # Закрыть текущее окно
            self.root.after(100, self.load_menu)  # Загрузить меню через небольшую задержку

    @staticmethod
    def load_menu():
        global root, menu
        from ten import GameMenu
        # Создать экземпляр класса GameMenu или вызвать необходимые методы из файла меню
        root = Tk()
        menu = GameMenu(root)
        root.mainloop()

    def stop_pad(self, event):
        if event.keysym in {"w", "s"}:
            self.LEFT_PAD_SPEED = 0

    def show_pause_screen(self):
        self.c.delete("pause_screen")

        if self.is_paused:
            self.c.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill="black", stipple="gray75", tag="pause_screen")
            self.c.create_text(self.WIDTH / 2, self.HEIGHT / 2 - 40, text="Игра на паузе", font="Arial 42",
                               fill="red", tag="pause_screen")
            self.c.create_text(self.WIDTH / 2, self.HEIGHT / 2, text="Для продолжения нажмите кнопку P",
                               font="Arial 23", fill="red", tag="pause_screen")
            self.c.create_text(self.WIDTH / 2, self.HEIGHT / 2 + 40, text="Для выхода в меню нажмите ESC",
                               font="Arial 23", fill="red", tag="pause_screen")

    def main(self):
        if not self.is_paused:
            self.move_ball()
            self.move_pads()

        self.c.after(20, self.main)


if __name__ == "__main__":
    root = Tk()
    menu = TennisSolo(root)
    root.mainloop()

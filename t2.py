from tkinter import *
import random
import tkinter as tk
from tkinter import Canvas, PhotoImage


class Tennis:
    def __init__(self, root):
        self.root = root
        self.root.title("Теннис")
        self.root.resizable(False, False)
        self.root.iconbitmap('ico.ico')  # Добавляем иконку

        # Определение размеров игрового поля
        self.WIDTH = 900
        self.HEIGHT = 540
        # Получение ширины и высоты экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Позиционирование окна по центру экрана
        x = (screen_width - self.WIDTH) // 2
        y = (screen_height - self.HEIGHT) // 2
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

        self.PAD_W = 8
        self.PAD_H = 140
        self.PAD_WIDTH = 10  # переменная для ширины ракеток

        # Константы для управления скоростью и размерами мяча
        self.BALL_SPEED_UP = 1.01
        self.BALL_MAX_SPEED = 100
        self.BALL_RADIUS = 30
        self.INITIAL_SPEED = 15

        # Инициализация переменных для счета игроков
        self.PLAYER_1_SCORE = 0
        self.PLAYER_2_SCORE = 0
        self.right_line_distance = self.WIDTH - self.PAD_W

        self.bg_image = PhotoImage(file="поле5.png")
        # Создание холста для отрисовки игровых объектов
        self.c = Canvas(self.root, width=self.WIDTH, height=self.HEIGHT)
        self.c.create_image(0, 0, image=self.bg_image, anchor='nw')
        self.c.pack()
        self.background_image = None
        # Создание мяча, платформ и текста для отображения счета
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

        # Инициализация переменных для управления мячом и платформами
        self.BALL_X_SPEED = self.INITIAL_SPEED
        self.BALL_Y_SPEED = self.INITIAL_SPEED
        self.PAD_SPEED = 20
        self.LEFT_PAD_SPEED = 0
        self.RIGHT_PAD_SPEED = 0

        # Привязка событий клавиатуры к методам для управления платформами
        self.c.focus_set()
        self.c.bind("<KeyPress>", self.movement_handler)
        self.c.bind("<KeyRelease>", self.stop_pad)
        # Запуск игры
        self.countdown(3)
        self.is_paused = False

    def update_score(self, player):
        if player == "right":
            self.PLAYER_1_SCORE += 1
            self.c.itemconfig(self.p_1_text, text=self.PLAYER_1_SCORE)
            if self.PLAYER_1_SCORE == 5:
                self.end_game("Победил второй игрок!\nНажмите Esc, чтобы вернуться в меню")

        else:
            self.PLAYER_2_SCORE += 1
            self.c.itemconfig(self.p_2_text, text=self.PLAYER_2_SCORE)
            if self.PLAYER_2_SCORE == 5:
                self.end_game("Победил первый игрок!\nНажмите Esc, чтобы вернуться в меню")

    def end_game(self, message):
        self.c.delete(ALL)  # Удалить все элементы с холста
        self.c.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill="#6495ED")
        self.c.create_text(self.WIDTH / 2, self.HEIGHT / 2, text=message, font="Arial 35", fill="black")
        self.c.pack()

    def spawn_ball(self):
        # Инициализация мяча и его скорости при старте и после каждого пропуска
        self.BALL_X_SPEED = -(self.BALL_X_SPEED * -self.INITIAL_SPEED) / abs(self.BALL_X_SPEED)
        self.c.coords(self.BALL, self.WIDTH / 2 - self.BALL_RADIUS / 2,
                      self.HEIGHT / 2 - self.BALL_RADIUS / 2,
                      self.WIDTH / 2 + self.BALL_RADIUS / 2,
                      self.HEIGHT / 2 + self.BALL_RADIUS / 2)

    def bounce(self, action):
        # Отскок мяча от платформы или границ поля
        if action == "strike":
            # Изменение скорости мяча при отскоке от платформы
            self.BALL_Y_SPEED = random.randrange(-10, 10)
            if abs(self.BALL_X_SPEED) < self.BALL_MAX_SPEED:
                self.BALL_X_SPEED *= -self.BALL_SPEED_UP
            else:
                self.BALL_X_SPEED = -self.BALL_X_SPEED
        else:
            # Отскок мяча от границ поля
            self.BALL_Y_SPEED = -self.BALL_Y_SPEED

    def move_ball(self):
        # Перемещение мяча и обработка столкновений
        ball_coords = self.c.coords(self.BALL)

        if ball_coords:
            ball_left, ball_top, ball_right, ball_bot = ball_coords
            ball_center = (ball_top + ball_bot) / 2

            if ball_right + self.BALL_X_SPEED < self.right_line_distance and \
                    ball_left + self.BALL_X_SPEED > self.PAD_W:
                # Перемещение мяча внутри поля
                self.c.move(self.BALL, self.BALL_X_SPEED, self.BALL_Y_SPEED)
            elif ball_right == self.right_line_distance or ball_left == self.PAD_W:
                # Обработка пропуска мяча одним из игроков
                if ball_right > self.WIDTH / 2:
                    if self.c.coords(self.RIGHT_PAD)[1] < ball_center < self.c.coords(self.RIGHT_PAD)[3]:
                        self.bounce("strike")
                    else:
                        # Мяч пропущен правым игроком
                        self.update_score("left")
                        self.spawn_ball()
                else:
                    if self.c.coords(self.LEFT_PAD)[1] < ball_center < self.c.coords(self.LEFT_PAD)[3]:
                        self.bounce("strike")
                    else:
                        # Мяч пропущен левым игроком
                        self.update_score("right")
                        self.spawn_ball()
            else:
                # Обработка отскока мяча от границ поля
                if ball_right > self.WIDTH / 2:
                    self.c.move(self.BALL, self.right_line_distance - ball_right, self.BALL_Y_SPEED)
                else:
                    self.c.move(self.BALL, -ball_left + self.PAD_W, self.BALL_Y_SPEED)

            if ball_top + self.BALL_Y_SPEED < 0 or ball_bot + self.BALL_Y_SPEED > self.HEIGHT:
                # Отскок мяча от верхней и нижней границ поля
                self.bounce("ricochet")

    def move_pads(self):
        # Перемещение платформ
        pads = {self.LEFT_PAD: self.LEFT_PAD_SPEED,
                self.RIGHT_PAD: self.RIGHT_PAD_SPEED}
        for pad in pads:
            pad_coords = self.c.coords(pad)
            if pad_coords:
                self.c.move(pad, 0, pads[pad])
                if pad_coords[1] < 0:
                    # Проверка и корректировка положения верхней границы платформы
                    self.c.move(pad, 0, -pad_coords[1])
                elif pad_coords[3] > self.HEIGHT:
                    # Проверка и корректировка положения нижней границы платформы
                    self.c.move(pad, 0, self.HEIGHT - pad_coords[3])

    def main(self):
        if not self.is_paused:
            self.move_ball()
            self.move_pads()

        self.c.after(20, self.main)

    def movement_handler(self, event):
        # Обработка нажатий клавиш
        if event.keysym == "w":
            self.LEFT_PAD_SPEED = -self.PAD_SPEED
        elif event.keysym == "s":
            self.LEFT_PAD_SPEED = self.PAD_SPEED
        elif event.keysym == "Up":
            self.RIGHT_PAD_SPEED = -self.PAD_SPEED
        elif event.keysym == "Down":
            self.RIGHT_PAD_SPEED = self.PAD_SPEED

    def stop_pad(self, event):
        # Остановка платформы при отпускании клавиши
        if event.keysym in ("w", "s"):
            self.LEFT_PAD_SPEED = 0
        elif event.keysym in ("Up", "Down"):
            self.RIGHT_PAD_SPEED = 0
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


if __name__ == "__main__":
    root = Tk()
    menu = Tennis(root)
    root.mainloop()

import customtkinter as CTk
from tkinter import messagebox
from random import randint
from sys import platform
from db import *
from user import *
from films import *
from settings import *


# Окно авторизации
class Login_window():
    def __init__(self):
        self.window = CTk.CTk()
        self.window.title('Авторизация')
        self.window.geometry('350x400')
        self.window.resizable(False, False)

        self.cinema_icon_img = CTk.CTkImage(light_image=Image.open('./img/icons/login_icon.png'),
                                            dark_image=Image.open('./img/icons/login_icon.png'),
                                            size=(128, 128))
        self.user_login()

    def user_login(self):
        self.cinema_icon = CTk.CTkLabel(self.window, text="", image=self.cinema_icon_img)
        self.cinema_icon.pack()

        self.authorization_label = CTk.CTkLabel(self.window, text='Авторизация', **header_padding)
        self.authorization_label.pack()

        # метка для поля ввода имени
        self.login_label = CTk.CTkLabel(self.window, text='Логин', **base_padding)
        self.login_label.pack()

        # поле ввода имени
        self.login_entry = CTk.CTkEntry(self.window)
        self.login_entry.pack()
        self.login_entry.focus()

        # метка для поля ввода пароля
        self.password_label = CTk.CTkLabel(self.window, text='Пароль', **base_padding)
        self.password_label.pack()

        # поле ввода пароля
        self.password_entry = CTk.CTkEntry(self.window)
        self.password_entry.pack()

        # кнопка отправки формы
        self.send_btn = CTk.CTkButton(self.window, text='Войти', command=self.login)
        self.send_btn.pack(**base_padding)

        self.registration_button = CTk.CTkButton(self.window, text='Регистрация', command=self.to_registration)
        self.registration_button.pack(**base_padding)

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.window.mainloop()

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        all_ok = False
        line = 1

        if login == '' or password == '':
            messagebox.showerror('Ошибка', 'Заполните все поля')
        else:
            while line != Data_base().users_sheet[f'I2'].value + 2:
                if (Data_base().users_sheet[f'C{line}'].value == login) and (
                        Data_base().users_sheet[f'D{line}'].value == password):
                    all_ok = True
                    User.change_user_data(User, login)
                    self.window.destroy()
                    Main_window()
                line += 1
            if not all_ok: messagebox.showerror('Ошибка', 'Неверный логин или пароль')

    def to_registration(self):
        Registration_window()

    def on_exit(self):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.window.destroy()


# Окно регистрации
class Registration_window():
    def __init__(self):
        self.window = CTk.CTkToplevel()
        self.window.title("Регистрация")
        self.window.geometry("300x630")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.code = None
        self.user_registration()

    def user_registration(self):
        self.authorization_icon_img = CTk.CTkImage(light_image=Image.open('./img/icons/new_user_icon.png'),
                                                   dark_image=Image.open('./img/icons/new_user_icon.png'),
                                                   size=(128, 128))

        self.authorization_icon = CTk.CTkLabel(self.window, text="", image=self.authorization_icon_img)
        self.authorization_icon.pack()

        self.authorization_label = CTk.CTkLabel(self.window, text='Регистрация', **header_padding)
        # помещаем виджет в окно по принципу один виджет под другим
        self.authorization_label.pack()

        # метка для поля ввода имени
        self.name_label = CTk.CTkLabel(self.window, text='ФИО', **base_padding)
        self.name_label.pack()

        # поле ввода имени
        self.name_entry = CTk.CTkEntry(self.window)
        self.name_entry.pack()
        self.name_entry.focus()

        self.login_label = CTk.CTkLabel(self.window, text='Логин', **base_padding)
        self.login_label.pack()

        # поле ввода логина
        self.login_entry = CTk.CTkEntry(self.window)
        self.login_entry.pack()
        self.login_entry.focus()

        self.email_label = CTk.CTkLabel(self.window, text='E-mail', **base_padding)
        self.email_label.pack()

        # поле ввода логина
        self.email_entry = CTk.CTkEntry(self.window)
        self.email_entry.pack()

        self.password_label = CTk.CTkLabel(self.window, text='Пароль', **base_padding)
        self.password_label.pack()

        # поле ввода пароля
        self.password_entry = CTk.CTkEntry(self.window)
        self.password_entry.pack()

        # метка для поля ввода пароля
        self.repeat_password_label = CTk.CTkLabel(self.window, text='Повторите пароль', **base_padding)
        self.repeat_password_label.pack()

        # поле ввода пароля
        self.repeat_password_entry = CTk.CTkEntry(self.window)
        self.repeat_password_entry.pack()

    # кнопка отправки формы
        self.send_btn = CTk.CTkButton(self.window, text='Выслать код подтверждения на email', command=self.generate_and_send_code)
        self.send_btn.pack(**base_padding)

        self.code_label = CTk.CTkLabel(self.window, text='Код подтверждения', **base_padding)
        self.code_label.pack()

        self.code_entry = CTk.CTkEntry(self.window)
        self.code_entry.pack()

        # кнопка отправки формы
        self.send_btn = CTk.CTkButton(self.window, text='Принять', command=self.confirm)
        self.send_btn.pack(**base_padding)

    def generate_and_send_code(self):
        self.code = str(randint(100000, 999999))
        letter = f'Вас приветствует кинотеатр Tkinter-cinema!\nВаш код для подтверждения регистрации: {self.code}\nЕсли вы не запрашивали этот код, просто проигнорируйте это сообщение'

        send_to_email(self.email_entry.get(), letter)
        print(self.code)

    def confirm(self):
        User.name = self.name_entry.get()
        User.login = self.login_entry.get()
        User.email = self.email_entry.get()
        User.password = self.password_entry.get()
        User.repeat_password = self.repeat_password_entry.get()
        User.code = self.code_entry.get()
        if User.login == '' or User.password == '' or User.repeat_password == '' or User.email == '':
            messagebox.showerror('Ошибка', 'Заполните все поля')
        elif User.password != User.repeat_password:
            messagebox.showerror('Ошибка', 'Пароли не совпадают')
        elif User.code != self.code:
            messagebox.showerror('Ошибка', 'Неверный код')
        else:
            self.registration()

    def registration(self):
        current_line = Data_base.users_sheet[f'I2'].value + 2
        Data_base.users_sheet[f'A{current_line}'] = Data_base().users_sheet[f'I2'].value + 1
        Data_base.users_sheet[f'B{current_line}'] = User.name
        Data_base.users_sheet[f'C{current_line}'] = User.login
        Data_base.users_sheet[f'D{current_line}'] = User.password
        Data_base.users_sheet[f'E{current_line}'] = User.email
        Data_base.users_sheet[f'F{current_line}'] = self.code
        Data_base.users_sheet[f'G{current_line}'] = f'{data.day}.{data.month}.{data.year}' 
        Data_base.users_sheet[f'I2'] = current_line - 1
        #User.change_user_data(User, login)
        messagebox.showinfo('Успешно', f'Логин: {User.name}\nПароль: {User.password}')
        Data_base.save_data_base(Data_base)
        self.window.destroy()

    def on_exit(self):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.window.destroy()

# Главное окно
class Main_window():
    def __init__(self):
        self.window = CTk.CTk()
        self.window.title('Резервирование билетов в кинотеатр')
        if platform == "linux" or platform == "linux2":
            self.window.attributes('-zoomed', True)
        elif platform == "darwin":
            self.window.attributes('-zoomed', True)
        elif platform == "win32":
            self.window.state('zoomed')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.top_bar_frame = CTk.CTkFrame(self.window, corner_radius=0)
        self.top_bar_frame.grid(row=0, column=0, sticky="nsew")
        self.top_bar_frame.grid_rowconfigure(4, weight=1)

        self.poster_btn = CTk.CTkButton(self.top_bar_frame, corner_radius=0, height=100, border_spacing=10,
                                        text='Афиша', fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), anchor="w", command=self.open_poster_window)
        self.poster_btn.grid(row=0, column=0, sticky="ew")

        self.cinema_btn = CTk.CTkButton(self.top_bar_frame, corner_radius=0, height=100, border_spacing=10,
                                        text='Кинотеатр', fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), anchor="w", command=self.open_cinema_window)
        self.cinema_btn.grid(row=1, column=0, sticky="ew")

        self.account_btn = CTk.CTkButton(self.top_bar_frame, corner_radius=0, height=100, border_spacing=10,
                                         text='Личный кабинет', fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"), anchor="w", command=self.open_account_window)
        self.account_btn.grid(row=2, column=0, sticky="ew")

        if (User.name != 'Guest') and (User.login != 'None'):
            self.account_btn = CTk.CTkButton(self.top_bar_frame, text='Выйти', command=self.logout)
            self.account_btn.grid(row=9, column=0, sticky="ew", pady=5)
        else:
            self.account_btn = CTk.CTkButton(self.top_bar_frame, text='Войти', command=self.logout)
            self.account_btn.grid(row=8, column=0, sticky="ew", pady=5)
            self.account_btn = CTk.CTkButton(self.top_bar_frame, text='Зарегистрируйтесь', command=self.registration)
            self.account_btn.grid(row=9, column=0, sticky="ew", pady=5)

        self.appearance_mode_menu = CTk.CTkOptionMenu(self.top_bar_frame, values=['System', 'Dark', 'Light'],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")

        self.current_frame = CTk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.current_frame.grid(row=0, column=1)

        self.open_cinema_window()

    def open_poster_window(self):

        self.current_frame.destroy()

        self.current_frame = CTk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.current_frame.grid(row=0, column=1)

        self.film_frame_1 = CTk.CTkFrame(self.current_frame, fg_color="transparent")
        self.film_frame_1.grid(row=0, column=0, sticky="w", pady=5)

        film_icon_img_1 = Film.current_film_icon(Film, 4)
        film_icon_1 = CTk.CTkLabel(self.film_frame_1, text="", justify='left', image=film_icon_img_1)
        film_icon_1.grid(row=0, column=0, rowspan=4, sticky="w", padx=1, pady=1)
        film_name_1 = CTk.CTkLabel(self.film_frame_1, height=10, justify='left', text=Film.current_film_name(Film, 4))
        film_name_1.grid(row=1, column=1, padx=1, pady=1, sticky='nw')
        film_description_1 = CTk.CTkLabel(self.film_frame_1, text=Film.current_film_description(Film, 4))
        film_description_1.grid(row=2, column=1, padx=1, pady=1, sticky='nw')
        buy_ticket_btn_1 = CTk.CTkButton(self.film_frame_1, text='Купить билет', command=lambda: self.buy_ticket(4))
        buy_ticket_btn_1.grid(row=3, column=1, sticky="s")

        self.film_frame_2 = CTk.CTkFrame(self.current_frame, fg_color="transparent")
        self.film_frame_2.grid(row=1, column=0, sticky="w", pady=5)
        # self.film_frame_2.grid_columnconfigure(0, weight=1)

        film_icon_img_2 = Film.current_film_icon(Film, 2)
        film_icon_2 = CTk.CTkLabel(self.film_frame_2, text="", image=film_icon_img_2)
        film_icon_2.grid(row=0, column=0, rowspan=4, sticky="w", padx=1, pady=1)
        film_name_2 = CTk.CTkLabel(self.film_frame_2, height=10, justify='left', text=Film.current_film_name(Film, 2))
        film_name_2.grid(row=0, column=1, padx=1, pady=1, sticky='nw')
        film_description_2 = CTk.CTkLabel(self.film_frame_2, text=Film.current_film_description(Film, 2))
        film_description_2.grid(row=1, column=1, padx=1, pady=1, sticky='nw')
        buy_ticket_btn_2 = CTk.CTkButton(self.film_frame_2, text='Купить билет', command=lambda: self.buy_ticket(2))
        buy_ticket_btn_2.grid(row=2, column=1, sticky="s")

        self.film_frame_3 = CTk.CTkFrame(self.current_frame, fg_color="transparent")
        self.film_frame_3.grid(row=2, column=0, sticky="w", pady=5)
        # self.film_frame_3.grid_columnconfigure(0, weight=1)

        film_icon_img_3 = Film.current_film_icon(Film, 3)
        film_icon_3 = CTk.CTkLabel(self.film_frame_3, text="", image=film_icon_img_3)
        film_icon_3.grid(row=0, column=0, rowspan=4, sticky="w", padx=1, pady=1)
        film_name_3 = CTk.CTkLabel(self.film_frame_3, height=10, justify='left', text=Film.current_film_name(Film, 3))
        film_name_3.grid(row=0, column=1, padx=1, pady=1, sticky='nw')
        film_description_2 = CTk.CTkLabel(self.film_frame_3, text=Film.current_film_description(Film, 3))
        film_description_2.grid(row=1, column=1, padx=1, pady=1, sticky='nw')
        buy_ticket_btn_3 = CTk.CTkButton(self.film_frame_3, text='Купить билет', command=lambda: self.buy_ticket(3))
        buy_ticket_btn_3.grid(row=2, column=1, sticky="s")

    def open_cinema_window(self):

        self.current_frame.destroy()

        self.current_frame = CTk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.current_frame.grid(row=0, column=1)

        cinema_icon_img = CTk.CTkImage(light_image=Image.open('img/icons/cinema_icon.png'),
                                       dark_image=Image.open('img/icons/cinema_icon.png'),
                                       size=(256, 256))
        cinema_icon = CTk.CTkLabel(self.current_frame, text="", image=cinema_icon_img)
        cinema_icon.pack()
        cinema_name = CTk.CTkLabel(self.current_frame, text='Кинотеатр "Художественный фильм"')
        cinema_name.pack()

    def open_account_window(self):

        self.current_frame.destroy()

        self.current_frame = CTk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.current_frame.grid(row=0, column=1)

        user_icon_img = CTk.CTkImage(light_image=Image.open('img/icons/user_icon.png'),
                                     dark_image=Image.open('img/icons/user_icon.png'),
                                     size=(256, 256))
        user_icon = CTk.CTkLabel(self.current_frame, text="", image=user_icon_img)
        user_icon.pack()
        user_name = CTk.CTkLabel(self.current_frame, text=User.login)
        user_name.pack()

    def change_appearance_mode_event(self, new_appearance_mode):
        CTk.set_appearance_mode(new_appearance_mode)

    def buy_ticket(self, film_id):
        Buy_ticket(film_id)

    def logout(self):
        self.window.destroy()
        Login_window()

    def registration(self):
        self.window.destroy()
        Registration_window()

    def on_exit(self):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.window.destroy()


class Buy_ticket():
    def __init__(self, film_id):
        self.window = CTk.CTkToplevel()
        self.window.title("Бронирование")
        self.window.geometry('350x530')
        self.window.resizable(False, False)
        self.create_buy_ticket_form(film_id)

    def create_buy_ticket_form(self, film_id):

        film_name = CTk.CTkLabel(self.window,
                                 text=f'{Film.current_film_name(Film, film_id)} {Film.current_film_age_limit(Film, film_id)}',
                                 **base_padding)
        film_name.pack()

        date_label = CTk.CTkLabel(self.window, text='Дата', **base_padding)
        date_label.pack()
        date_arr = Movie_schedule().session_date(film_id)
        self.date_menu = CTk.CTkOptionMenu(self.window, values=date_arr, dynamic_resizing=True)
        self.date_menu.pack()
        data = self.date_menu.get()

        auditorium_label = CTk.CTkLabel(self.window, text='Зал', **base_padding)
        auditorium_label.pack()
        auditorium_arr = Movie_schedule().session_auditorium(film_id, data)
        self.auditorium_menu = CTk.CTkOptionMenu(self.window, values=auditorium_arr, dynamic_resizing=True)
        self.auditorium_menu.pack()
        auditorium = self.auditorium_menu.get()

        time_label = CTk.CTkLabel(self.window, text='Время', **base_padding)
        time_label.pack()
        time_arr = Movie_schedule().session_time(film_id, auditorium)
        self.time_menu = CTk.CTkOptionMenu(self.window, values=time_arr, command=self.update_price,
                                           dynamic_resizing=True)
        self.time_menu.pack()

        row_label = CTk.CTkLabel(self.window, text='Ряд', **base_padding)
        row_label.pack()
        row_arr = list(map(str, range(1, 5)))
        self.row_menu = CTk.CTkOptionMenu(self.window, values=row_arr, command=self.update_row, dynamic_resizing=True)
        self.row_menu.pack()

        place_label = CTk.CTkLabel(self.window, text='Место', **base_padding)
        place_label.pack()
        place_arr = list(map(str, range(1, 5)))
        self.place_menu = CTk.CTkOptionMenu(self.window, values=place_arr, dynamic_resizing=True)
        self.place_menu.pack()
        self.update_row(None)

        username_label = CTk.CTkLabel(self.window, text='ФИО зрителя', **base_padding)
        username_label.pack()
        username_entry = CTk.CTkEntry(self.window)
        username_entry.pack()

        self.price_label = CTk.CTkLabel(self.window, text=f'Цена билета: None\n(оплата при входе в зрительный зал)',
                                        **base_padding)
        self.price_label.pack()
        self.update_price(None)

        buy_btn = CTk.CTkButton(self.window, text='Купить')
        buy_btn.pack()

    def update_row(self, row_menu):
        current_auditorium = self.time_menu.get()
        line = 1
        while line <= int(Data_base().auditorium_sheet['E2'].value) + 1:
            if str(Data_base().schedule_sheet[f'A{line}'].value) == current_auditorium:
                max_row = str(Data_base().schedule_sheet[f'C{line}'].value)
                row_arr = list(map(str, range(1, max_row)))
                self.row_menu.configure(values=row_arr)
                break
            line += 1

    def update_price(self, time_menu):
        current_time = self.time_menu.get()
        line = 1
        while line <= int(Data_base().schedule_sheet['H2'].value) + 1:
            if str(Data_base().schedule_sheet[f'F{line}'].value) == current_time:
                price = str(Data_base().schedule_sheet[f'C{line}'].value)
                self.price_label.configure(text=f'Цена билета: {price}\n(оплата при входе в зрительный зал)')
                break
            line += 1


class Movie_schedule():
    def current_lines(self, current_string):
        line = 1
        lines = []
        while line != Data_base().schedule_sheet[f'H2'].value + 2:
            if Data_base().schedule_sheet[f'B{line}'].value == current_string: lines.append(line)
            line += 1
        return lines

    def session_date(self, film_id):
        session_date_arr = []
        lines = self.current_lines(film_id)
        for line in lines:
            if str(Data_base().schedule_sheet[f'E{line}'].value) in session_date_arr: continue
            session_date_arr.append(str(Data_base().schedule_sheet[f'E{line}'].value))
        return session_date_arr

    def session_auditorium(self, film_id, date):
        session_auditorium_arr = []
        lines = self.current_lines(film_id)
        for line in lines:
            if str(Data_base().schedule_sheet[f'E{line}'].value) == date:
                if str(Data_base().schedule_sheet[f'A{line}'].value) in session_auditorium_arr: continue
                session_auditorium_arr.append(str(Data_base().schedule_sheet[f'A{line}'].value))
            return session_auditorium_arr

    def session_time(self, film_id, auditorium):
        session_time_arr = []
        lines = self.current_lines(film_id)
        for line in lines:
            if str(Data_base().schedule_sheet[f'A{line}'].value) == auditorium:
                if str(Data_base().schedule_sheet[f'F{line}'].value) in session_time_arr: continue
                session_time_arr.append(str(Data_base().schedule_sheet[f'F{line}'].value))
            return session_time_arr


if __name__ == '__main__':
    try:
        Data_base()
    except:
        messagebox.showerror('Ошибка', 'Ошибка загрузки базы данных')
        exit()
    try:
        User()
    except:
        messagebox.showerror('Ошибка', 'Ошибка загрузки данных пользователя')
        exit()
    try:
        Login_window()
    except: 
        messagebox.showerror('Ошибка', 'Ошибка загрузки интерфейса Tkinter')
        exit()

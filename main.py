import customtkinter as CTk
from tkinter import messagebox
from random import randint
from sys import platform
import os
from db.db import *
from user import *
from films import *
from settings import *
from buy_ticket import *
from db.movie_schedule import *
from open_txt import open_txt_file


# Окно авторизации
class Login_window():
    def __init__(self):
        self.window = CTk.CTk()
        self.window.title('Авторизация')
        self.window.geometry('350x510')
        self.window.resizable(False, False)

        self.cinema_icon_img = CTk.CTkImage(light_image=Image.open('./img/icons/login_icon.png'),
                                            dark_image=Image.open('./img/icons/login_icon.png'),
                                            size=(128, 128))
        self.user_login()

    #Форма для авторизации
    def user_login(self):
        self.cinema_icon = CTk.CTkLabel(self.window, text="", image=self.cinema_icon_img)
        self.cinema_icon.pack()

        self.authorization_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=20, weight="bold"), text='Авторизация', **header_padding)
        self.authorization_label.pack()

        self.login_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Логин', **base_padding)
        self.login_label.pack(**base_padding)

        self.login_entry = CTk.CTkEntry(self.window)
        self.login_entry.pack(**base_padding)
        self.login_entry.focus()

        self.password_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Пароль', **base_padding)
        self.password_label.pack(**base_padding)

        self.password_entry = CTk.CTkEntry(self.window)
        self.password_entry.pack(**base_padding)

        self.send_btn = CTk.CTkButton(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Войти', command=self.login)
        self.send_btn.pack(**base_padding)

        self.registration_button = CTk.CTkButton(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Регистрация', command=self.to_registration)
        self.registration_button.pack(**base_padding)

        self.import_file_btn = CTk.CTkButton(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Импортировать текстовый файл', command=lambda: Import_file())
        self.import_file_btn.pack(**base_padding)

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.window.mainloop()

    #Авторизация пользователя
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

    #Переадресация на форму регистрации
    def to_registration(self):
        Registration_window()

    #Подтверждение выхода
    def on_exit(self):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.window.destroy()

#Окно импорта файла
class Import_file():
    def __init__(self):
        self.window = CTk.CTkToplevel()
        self.window.title("Импортировать файл для заказа билета")
        self.window.geometry("400x120")
        self.window.resizable(False, False)
        self.files_arr = []
        self.scan_directory()

        self.files_label = CTk.CTkLabel(self.window, text='Выберите .txt файл из текущей директории', **header_padding)
        self.files_label.pack()

        self.files_menu = self.date_menu = CTk.CTkOptionMenu(self.window, values=self.files_arr, dynamic_resizing=True)
        self.files_menu.pack()

        self.send_btn = CTk.CTkButton(self.window, text='Импортировать', command=self.scan_file)
        self.send_btn.pack(**base_padding)

    #сканирование текущей директории
    def scan_directory(self):
        files = os.listdir('./')
        is_file = False
        for file in files:
            if file[-4:] == '.txt':
                self.files_arr.append(file)
                is_file = True
        if not is_file:
            self.files_arr.append('None')

    #сканирование выбранного файла
    def scan_file(self):
        file_name = self.files_menu.get()
        file = open_txt_file(file_name)
        while True:
            line = file.readline()
            parameter = line.partition(':')[0]
            parameter_data = line.partition(':')[2]
            if parameter == 'Username':
                username=parameter_data.replace('\n','')
            elif parameter =='Film_name':
                film_name = parameter_data.replace(' ','').replace('\n','')
            elif parameter =='Data':
                data = parameter_data.replace(' ','').replace('\n','')
            elif parameter =='Time':
                time = parameter_data.replace(' ','').replace('\n','')
            elif parameter =='Auditorium':
                auditorium = parameter_data.replace(' ','').replace('\n','')
            elif parameter =='Row':
                row = parameter_data.replace(' ','').replace('\n','')
            elif parameter =='Place':
                place = parameter_data.replace(' ','').replace('\n','')
            if not line:
                break
        file.close()

        film_id = None
        line = 2
        is_movie_exist = False
        while line!=Data_base().films_sheet[f'J2'].value+2:
            if film_name == str(Data_base().films_sheet[f'B{line}'].value): 
                film_id = Data_base().films_sheet[f'A{line}'].value
                is_movie_exist = True
                break
            line+=1
        if is_movie_exist:
            buy(username, film_id, data, time, auditorium, row, place)
        else: messagebox.showerror('Ошибка', 'Неккоректное имя фильма')
        
# Окно регистрации
class Registration_window():
    def __init__(self):
        self.window = CTk.CTkToplevel()
        self.window.title("Регистрация")
        self.window.geometry("340x770")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.code = None
        self.user_registration()

    #Форма для регистрации пользователя
    def user_registration(self):
        self.authorization_icon_img = CTk.CTkImage(light_image=Image.open('./img/icons/new_user_icon.png'),
                                                   dark_image=Image.open('./img/icons/new_user_icon.png'),
                                                   size=(128, 128))

        self.authorization_icon = CTk.CTkLabel(self.window, text="", image=self.authorization_icon_img)
        self.authorization_icon.pack()

        self.authorization_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=20, weight="bold"), text='Регистрация', **header_padding)
        self.authorization_label.pack()

        self.name_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='ФИО', **base_padding)
        self.name_label.pack(**base_padding)

        self.name_entry = CTk.CTkEntry(self.window)
        self.name_entry.pack()
        self.name_entry.focus()

        self.login_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Логин', **base_padding)
        self.login_label.pack(**base_padding)

        self.login_entry = CTk.CTkEntry(self.window)
        self.login_entry.pack()

        self.email_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='E-mail', **base_padding)
        self.email_label.pack(**base_padding)

        self.email_entry = CTk.CTkEntry(self.window)
        self.email_entry.pack(**base_padding)

        self.password_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Пароль', **base_padding)
        self.password_label.pack(**base_padding)

        self.password_entry = CTk.CTkEntry(self.window)
        self.password_entry.pack()

        self.repeat_password_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Повторите пароль', **base_padding)
        self.repeat_password_label.pack(**base_padding)

        self.repeat_password_entry = CTk.CTkEntry(self.window)
        self.repeat_password_entry.pack(**base_padding)

        self.send_btn = CTk.CTkButton(self.window, font=CTk.CTkFont(size=15, weight="bold"),  text='Выслать код подтверждения на email', command=self.generate_and_send_code)
        self.send_btn.pack(**base_padding)

        self.code_label = CTk.CTkLabel(self.window, font=CTk.CTkFont(size=15, weight="bold"), text='Код подтверждения', **base_padding)
        self.code_label.pack(**base_padding)

        self.code_entry = CTk.CTkEntry(self.window)
        self.code_entry.pack()

        self.send_btn = CTk.CTkButton(self.window, font=CTk.CTkFont(size=20, weight="bold"), text='Принять', command=self.confirm)
        self.send_btn.pack(**base_padding)

    #Генерация и отправка кода подтверждения на почту
    def generate_and_send_code(self):
        self.code = str(randint(100000, 999999))
        letter = f'Вас приветствует кинотеатр Tkinter-cinema!\nВаш код для подтверждения регистрации: {self.code}\nЕсли вы не запрашивали этот код, просто проигнорируйте это сообщение'
        send_to_email(self.email_entry.get(), letter)

    #Проверка правильности заполнения формы регистрации
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

    #Регистрация пользователя в приложении
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

    #Подтверждение выхода
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

        self.poster_btn = CTk.CTkButton(self.top_bar_frame, corner_radius=0, height=100, border_spacing=10, font=CTk.CTkFont(size=20, weight="bold"),
                                        text='Афиша', fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), anchor="w", command=self.open_poster_window)
        self.poster_btn.grid(row=0, column=0, sticky="ew")

        self.cinema_btn = CTk.CTkButton(self.top_bar_frame, corner_radius=0, height=100, border_spacing=10, font=CTk.CTkFont(size=20, weight="bold"),
                                        text='Кинотеатр', fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), anchor="w", command=self.open_cinema_window)
        self.cinema_btn.grid(row=1, column=0, sticky="ew")

        self.account_btn = CTk.CTkButton(self.top_bar_frame, corner_radius=0, height=100, border_spacing=10, font=CTk.CTkFont(size=20, weight="bold"),
                                         text='Личный кабинет', fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"), anchor="w", command=self.open_account_window)
        self.account_btn.grid(row=2, column=0, sticky="ew")

        if (User.name != 'Guest') and (User.login != 'None'):
            self.account_btn = CTk.CTkButton(self.top_bar_frame, font=CTk.CTkFont(size=20, weight="bold"), text='Выйти', command=self.logout)
            self.account_btn.grid(row=9, column=0, sticky="ew", pady=5)
        else:
            self.account_btn = CTk.CTkButton(self.top_bar_frame, font=CTk.CTkFont(size=20, weight="bold"), text='Войти', command=self.logout)
            self.account_btn.grid(row=8, column=0, sticky="ew", pady=5)
            self.account_btn = CTk.CTkButton(self.top_bar_frame, font=CTk.CTkFont(size=20, weight="bold"), text='Зарегистрируйтесь', command=self.registration)
            self.account_btn.grid(row=9, column=0, sticky="ew", pady=5)

        self.appearance_mode_menu = CTk.CTkOptionMenu(self.top_bar_frame, values=['System', 'Dark', 'Light'],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")

        self.current_frame = CTk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.current_frame.grid(row=0, column=1)

        self.open_cinema_window()

    #Открытие вкладки Афиша
    def open_poster_window(self):

        self.current_frame.destroy()

        self.current_frame = CTk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.current_frame.grid(row=0, column=1)

        self.film_frame_1 = CTk.CTkFrame(self.current_frame, fg_color="transparent")
        self.film_frame_1.grid(row=0, column=0, sticky="w", pady=5)

        film_icon_img_1 = Film.current_film_icon(Film, 4)
        film_icon_1 = CTk.CTkLabel(self.film_frame_1, text="", justify='left', image=film_icon_img_1)
        film_icon_1.grid(row=0, column=0, rowspan=4, sticky="w", padx=10, pady=1)
        film_name_1 = CTk.CTkLabel(self.film_frame_1, height=10, justify='left', text=Film.current_film_name(Film, 4), font=CTk.CTkFont(size=20, weight="bold"))
        film_name_1.grid(row=1, column=1, padx=1, pady=1, sticky='nw')
        film_description_1 = CTk.CTkLabel(self.film_frame_1, justify='left', font=CTk.CTkFont(size=15, weight="bold"), text=Film.current_film_description(Film, 4))
        film_description_1.grid(row=2, column=1, padx=1, pady=1, sticky='nw')
        buy_ticket_btn_1 = CTk.CTkButton(self.film_frame_1, text='Купить билет', font=CTk.CTkFont(size=15, weight="bold"), command=lambda: self.buy_ticket(4))
        buy_ticket_btn_1.grid(row=3, column=1, sticky="e")

        self.film_frame_2 = CTk.CTkFrame(self.current_frame, fg_color="transparent")
        self.film_frame_2.grid(row=1, column=0, sticky="w", pady=5)

        film_icon_img_2 = Film.current_film_icon(Film, 2)
        film_icon_2 = CTk.CTkLabel(self.film_frame_2, text="", image=film_icon_img_2)
        film_icon_2.grid(row=0, column=0, rowspan=4, sticky="w", padx=10, pady=1)
        film_name_2 = CTk.CTkLabel(self.film_frame_2, height=10, justify='left', text=Film.current_film_name(Film, 2), font=CTk.CTkFont(size=20, weight="bold"))
        film_name_2.grid(row=0, column=1, padx=1, pady=1, sticky='nw')
        film_description_2 = CTk.CTkLabel(self.film_frame_2, justify='left', font=CTk.CTkFont(size=15, weight="bold"), text=Film.current_film_description(Film, 2))
        film_description_2.grid(row=1, column=1, padx=1, pady=1, sticky='nw')
        buy_ticket_btn_2 = CTk.CTkButton(self.film_frame_2, text='Купить билет', font=CTk.CTkFont(size=15, weight="bold"), command=lambda: self.buy_ticket(2))
        buy_ticket_btn_2.grid(row=2, column=1, sticky="e")

        self.film_frame_3 = CTk.CTkFrame(self.current_frame, fg_color="transparent")
        self.film_frame_3.grid(row=2, column=0, sticky="w", pady=5)

        film_icon_img_3 = Film.current_film_icon(Film, 3)
        film_icon_3 = CTk.CTkLabel(self.film_frame_3, text="", image=film_icon_img_3)
        film_icon_3.grid(row=0, column=0, rowspan=4, sticky="w", padx=10, pady=1)
        film_name_3 = CTk.CTkLabel(self.film_frame_3, height=10, justify='left', text=Film.current_film_name(Film, 3), font=CTk.CTkFont(size=20, weight="bold"))
        film_name_3.grid(row=0, column=1, padx=1, pady=1, sticky='nw')
        film_description_2 = CTk.CTkLabel(self.film_frame_3, justify='left', font=CTk.CTkFont(size=15, weight="bold"), text=Film.current_film_description(Film, 3))
        film_description_2.grid(row=1, column=1, padx=1, pady=1, sticky='nw')
        buy_ticket_btn_3 = CTk.CTkButton(self.film_frame_3, text='Купить билет', font=CTk.CTkFont(size=15, weight="bold"), command=lambda: self.buy_ticket(3))
        buy_ticket_btn_3.grid(row=2, column=1, sticky="e")

    #Открытие вкладки Кинотеатр
    def open_cinema_window(self):

        self.current_frame.destroy()

        self.current_frame = CTk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.current_frame.grid(row=0, column=1)

        cinema_icon_img = CTk.CTkImage(light_image=Image.open('img/icons/cinema_icon.png'),
                                       dark_image=Image.open('img/icons/cinema_icon.png'),
                                       size=(256, 256))
        cinema_icon = CTk.CTkLabel(self.current_frame, text="", image=cinema_icon_img)
        cinema_icon.pack()
        cinema_name = CTk.CTkLabel(self.current_frame, font=CTk.CTkFont(size=30, weight="bold"), text='Кинотеатр "Художественный фильм"')
        cinema_name.pack()
        cinema_adress = CTk.CTkLabel(self.current_frame, font=CTk.CTkFont(size=20, weight="bold"), text='Адрес: Астрахань, улица Пушкина, дом 231, 3 этаж')
        cinema_adress.pack()

    #Открытие вкладки Личный кабинет
    def open_account_window(self):

        self.current_frame.destroy()

        self.current_frame = CTk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.current_frame.grid(row=0, column=1)

        user_icon_img = CTk.CTkImage(light_image=Image.open('img/icons/user_icon.png'),
                                     dark_image=Image.open('img/icons/user_icon.png'),
                                     size=(256, 256))
        user_icon = CTk.CTkLabel(self.current_frame, text="", image=user_icon_img)
        user_icon.pack(**base_padding)
        user_name = CTk.CTkLabel(self.current_frame, font=CTk.CTkFont(size=30, weight="bold"), text=User.login)
        user_name.pack(**base_padding)
        change_password_btn = CTk.CTkButton(self.current_frame, font=CTk.CTkFont(size=20, weight="bold"), text='Сменить пароль', command= lambda: print('Change password'))
        change_password_btn.pack(**base_padding)

    #Смена темы приложения
    def change_appearance_mode_event(self, new_appearance_mode):
        CTk.set_appearance_mode(new_appearance_mode)

    #Переадресация на форму бронирования билета
    def buy_ticket(self, film_id):
        Buy_ticket(film_id)

    #Выход из учётной записи
    def logout(self):
        self.window.destroy()
        Login_window()

    #Переадресация на форму регистрации
    def registration(self):
        self.window.destroy()
        Registration_window()

    #Подтверждение выхода
    def on_exit(self):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.window.destroy()

#Бронирование билета
class Buy_ticket():
    def __init__(self, film_id):
        self.window = CTk.CTkToplevel()
        self.window.title("Бронирование")
        self.window.geometry('350x530')
        self.window.resizable(False, False)
        self.film_id = film_id
        self.create_buy_ticket_form(self.film_id)

    #Формирание формы бронирования билетов
    def create_buy_ticket_form(self, film_id):

        film_name = CTk.CTkLabel(self.window,
                                 text=f'{Film.current_film_name(Film, self.film_id)} {Film.current_film_age_limit(Film, self.film_id)}',
                                 **base_padding)
        film_name.pack()

        date_label = CTk.CTkLabel(self.window, text='Дата', **base_padding)
        date_label.pack()
        date_arr = Movie_schedule().session_date(self.film_id)
        self.date_menu = CTk.CTkOptionMenu(self.window, values=date_arr, command=self.update_all, dynamic_resizing=True)
        self.date_menu.pack()

        auditorium_label = CTk.CTkLabel(self.window, text='Зал', **base_padding)
        auditorium_label.pack()
        auditorium_arr = Movie_schedule().session_auditorium(self.film_id)
        self.auditorium_menu = CTk.CTkOptionMenu(self.window, values=auditorium_arr, dynamic_resizing=True)
        self.auditorium_menu.pack()

        time_label = CTk.CTkLabel(self.window, text='Время', **base_padding)
        time_label.pack()
        time_arr = Movie_schedule().session_time(self.film_id)
        self.time_menu = CTk.CTkOptionMenu(self.window, values=time_arr, command=self.update_price,
                                           dynamic_resizing=True)
        self.time_menu.pack()

        row_label = CTk.CTkLabel(self.window, text='Ряд', **base_padding)
        row_label.pack()
        row_arr = list(map(str, range(1, 6)))
        self.row_menu = CTk.CTkOptionMenu(self.window, values=row_arr, command=self.update_row, dynamic_resizing=True)
        self.row_menu.pack()

        place_label = CTk.CTkLabel(self.window, text='Место', **base_padding)
        place_label.pack()
        place_arr = list(map(str, range(1, 11)))
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

    def update_all(self, menu):
        self.window.destroy()
        Buy_ticket(self.film_id)

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

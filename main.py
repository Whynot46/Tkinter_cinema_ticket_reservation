# импортируем библиотеку tkinter всю сразу
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from top_bar import *


# кортежи и словари, содержащие настройки шрифтов и отступов
font_header = ('Arial', 15)
font_entry = ('Arial', 12)
label_font = ('Arial', 11)
base_padding = {'padx': 10, 'pady': 8}
header_padding = {'padx': 10, 'pady': 12}


class Login_window:
    def __init__(self):
        self.window = Tk()
        self.window.title('Авторизация')
        self.window.geometry('350x400')
        self.window.resizable(False, False)

        self.cinema_icon = Canvas(self.window, height = 128, width = 128)
        self.cinema_img = PhotoImage(file='./img/cinema_icon.png')
        self.cinema_icon.pack()
        self.cinema_icon.create_image(0, 0, anchor=NW, image=self.cinema_img)

        self.authorization_label = Label(self.window, text='Авторизация', font=font_header, justify=CENTER, **header_padding)
        self.authorization_label.pack()

        # метка для поля ввода имени
        self.login_label = Label(self.window, text='Логин', font=label_font, **base_padding)
        self.login_label.pack()

        # поле ввода имени
        self.login_entry = Entry(self.window, bg='#fff', fg='#444', font=font_entry)
        self.login_entry.pack()
        self.login_entry.focus()

        # метка для поля ввода пароля
        self.password_label = Label(self.window, text='Пароль', font=label_font, **base_padding)
        self.password_label.pack()

        # поле ввода пароля
        self.password_entry = Entry(self.window, bg='#fff', fg='#444', font=font_entry)
        self.password_entry.pack()

        # кнопка отправки формы
        self.send_btn = Button(self.window, text='Войти', command=self.login)
        self.send_btn.pack(**base_padding)

        self.registration_button = Button(text='Регистрация', font=label_font, **base_padding, command=self.to_registration)
        self.registration_button.pack(**base_padding)

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.window.mainloop()


    def login(self):
        User.login = self.login_entry.get()
        User.password = self.password_entry.get()
        self.window.destroy()
        Main_window()


    def to_registration(self):
        Registration_window()


    def on_exit(self):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.window.destroy()


class Registration_window():
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Регистрация")
        self.window.geometry("300x410")
        self.window.resizable(False, False)

        self.new_user_icon = Canvas(self.window, height = 128, width = 128)
        self.new_user_img = PhotoImage(file='./img/new_user_icon.png')
        self.new_user_icon.pack()
        self.new_user_icon.create_image(0, 0, anchor=NW, image=self.new_user_img)

        self.authorization_label = Label(self.window, text='Регистрация', font=font_header, justify=CENTER, **header_padding)
        # помещаем виджет в окно по принципу один виджет под другим
        self.authorization_label.pack()

        # метка для поля ввода имени
        self.login_label = Label(self.window, text='Логин', font=label_font, **base_padding)
        self.login_label.pack()

        # поле ввода имени
        self.login_entry = Entry(self.window, bg='#fff', fg='#444', font=font_entry)
        self.login_entry.pack()
        self.login_entry.focus()

        # метка для поля ввода пароля
        self.password_label = Label(self.window, text='Пароль', font=label_font, **base_padding)
        self.password_label.pack()

        # поле ввода пароля
        self.password_entry = Entry(self.window, bg='#fff', fg='#444', font=font_entry)
        self.password_entry.pack()

        # метка для поля ввода пароля
        self.repeat_password_label = Label(self.window, text='Повторите пароль', font=label_font, **base_padding)
        self.repeat_password_label.pack()

        # поле ввода пароля
        self.repeat_password_entry = Entry(self.window, bg='#fff', fg='#444', font=font_entry)
        self.repeat_password_entry.pack()

        # кнопка отправки формы
        self.send_btn = Button(self.window, text='Принять', command=self.registration)
        self.send_btn.pack(**base_padding)

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)


    def registration(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        repeat_password = self.repeat_password_entry.get()

        if login=='' or password=='' or repeat_password=='':
            messagebox.showerror('Ошибка', 'Заполните все поля')
        elif password == repeat_password:
            messagebox.showinfo('Успешно', f'Логин: {username}\nПароль: {password}')
        else: messagebox.showerror('Ошибка', 'Пароли не совпадают')


    def on_exit(self):
        if messagebox.askokcancel("Прервать регистрацию", "Вы действительно хотите прервать регистрацию?"):
            self.window.destroy()


class Main_window():
    def __init__(self):
        self.window = Tk()
        self.window.title('Резервирование билетов в кинотеатр "Художественный фильм"')
        #self.window.state('zoomed') #Под Windows, если не раскрывается в полный экран, заккоментируйте следующую строчку
        self.window.attributes('-zoomed', True)

        self.top_bar = ttk.Notebook(self.window, width=1000, height=1000)

        self.poster_tab = Poster_tab(self.top_bar)
        self.news_tab = News_tab(self.top_bar)
        self.account_tab = Account_tab(self.top_bar)

        self.top_bar.add(self.poster_tab, text="Афиша")
        self.top_bar.add(self.news_tab, text="Новости")
        self.top_bar.add(self.account_tab, text="Личный кабинет")

        self.top_bar.pack() 


if __name__ == '__main__':
    Login_window()


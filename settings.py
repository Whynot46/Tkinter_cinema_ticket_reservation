import datetime
import smtplib
from tkinter import messagebox
from customtkinter import set_appearance_mode, set_default_color_theme

base_padding = {'padx': 10, 'pady': 8}
header_padding = {'padx': 10, 'pady': 12}

data = datetime.datetime.today()

set_appearance_mode("System")  # Modes: system (default), light, dark
set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

#Отправка кода подтверждения на почту
def send_to_email(email, letter):
    login = 'Tkinter-cinema@yandex.ru'
    password = 'ehnznlmpdooacens'
    try:
        server = smtplib.SMTP_SSL('smtp.yandex.ru:465')

        server.login(login, password)
        server.sendmail(login, email, letter.encode('utf-8'))
        server.quit()
    except: messagebox.showerror('Ошибка', 'Неккоректный email')

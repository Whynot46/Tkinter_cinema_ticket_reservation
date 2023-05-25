from tkinter import *
from tkinter import ttk
from user_data import *


# кортежи и словари, содержащие настройки шрифтов и отступов
font_header = ('Arial', 15)
font_entry = ('Arial', 12)
label_font = ('Arial', 11)
base_padding = {'padx': 10, 'pady': 8}
header_padding = {'padx': 10, 'pady': 12}


class Poster_tab(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		self.poster_label = Label(self, text='Здесь будет афиша', font=label_font, **base_padding)
		self.poster_label.pack()

		self.pack()



class News_tab(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		self.poster_label = Label(self, text='Здесь будут новости', font=label_font, **base_padding)
		self.poster_label.pack()

		self.pack()


class Account_tab(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		self.poster_label = Label(self, text='Личный кабинет', font=label_font, **base_padding)
		self.poster_label.place(relx = 0.45, rely = 0.0)

		self.user_icon = Canvas(self, height = 128, width = 128)
		self.user_icon_img = PhotoImage(file='./img/user_icon.png')
		self.user_icon.place(relx = 0.0195, rely = 0.05)
		self.user_icon.create_image(0, 0, anchor=NW, image=self.user_icon_img)

		self.poster_label = Label(self, text=f'{User.login}', font=label_font, **base_padding)
		self.poster_label.place(relx = 0.03, rely = 0.19)

		self.change_password_btn = Button(self, text='Сменить пароль', command=self.change_password)
		self.change_password_btn.place(relx = 0.02, rely = 0.23)

		self.pack()


	def change_password(self):
		pass

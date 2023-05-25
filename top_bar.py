from tkinter import *
from tkinter import ttk


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

		self.poster_label = Label(self, text='Здесь будет личный кабинет', font=label_font, **base_padding)
		self.poster_label.pack()

		self.pack()
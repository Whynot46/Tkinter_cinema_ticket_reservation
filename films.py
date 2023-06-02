from PIL import Image
from customtkinter import CTkImage
from db import *

#Фильмы
class Film():
    def __init__(self):

        self.icon = CTkImage(light_image=Image.open('img/icons/film_icon.png'),
                                  dark_image=Image.open('img/icons/film_icon.png'),
                                  size=(128, 128))
        self.name = 'Name'
        self.description = 'Description'

    #Выбор нужной строки по id фильма
    def current_line(self, id):
        line = 1
        while line!=Data_base().films_sheet[f'J2'].value+2:
            if Data_base().films_sheet[f'A{line}'].value == id: return line
            line+=1

    #Загрузка иконки фильма
    def current_film_icon(self, id):
        icon = CTkImage(light_image=Image.open(f'img/films/{id}.png'),
                                  dark_image=Image.open(f'img/films/{id}.png'),
                                  size=(256, 256))
        return icon

    #Загрузка имени фильма
    def current_film_name(self, id):
        current_line = self.current_line(self, id)
        name = Data_base().films_sheet[f'B{current_line}'].value
        return name

    #Загрузка описания фильма
    def current_film_description(self, id):
        current_line = self.current_line(self, id)
        description = Data_base().films_sheet[f'C{current_line}'].value
        return description

    #Загрузка продолжительности фильма
    def current_film_duration(self, id):
        current_line = self.current_line(self, id)
        duration = Data_base().films_sheet[f'E{current_line}'].value
        return duration

    #Загрузка возрастного ограничения фильма
    def current_film_age_limit(self, id):
        current_line = self.current_line(self, id)
        age_limit = f'{Data_base().films_sheet[f"F{current_line}"].value}+'
        return age_limit
  
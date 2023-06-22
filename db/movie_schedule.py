from db.db import *


class Movie_schedule():
    #Определение выбранных строк в базе данных
    def current_lines(self, current_string):
        line = 1
        lines = []
        while line != Data_base().schedule_sheet[f'H2'].value + 2:
            if Data_base().schedule_sheet[f'B{line}'].value == current_string: lines.append(line)
            line += 1
        return lines
    
    #Определение дат показов фильмов
    def session_date(self, film_id):
        session_date_arr = []
        lines = self.current_lines(film_id)
        for line in lines:
            if str(Data_base().schedule_sheet[f'E{line}'].value) in session_date_arr: continue
            session_date_arr.append(str(Data_base().schedule_sheet[f'E{line}'].value))
        return session_date_arr

    #Определение залов показа фильмов
    def session_auditorium(self, film_id):
        session_auditorium_arr = []
        lines = self.current_lines(film_id)
        for line in lines:
            if str(Data_base().schedule_sheet[f'A{line}'].value) in session_auditorium_arr: continue
            session_auditorium_arr.append(str(Data_base().schedule_sheet[f'A{line}'].value))
        return session_auditorium_arr

    #Определение времени показа фильмов
    def session_time(self, film_id):
        session_time_arr = []
        lines = self.current_lines(film_id)
        for line in lines:
            if str(Data_base().schedule_sheet[f'F{line}'].value) in session_time_arr: 
                continue
            session_time_arr.append(str(Data_base().schedule_sheet[f'F{line}'].value))
        return session_time_arr
            

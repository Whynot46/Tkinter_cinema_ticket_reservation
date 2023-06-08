from tkinter import messagebox
from db import *

#Покупка билета
def buy(username, film_id, data, time, auditorium, row, place):

    print(username, film_id, data, time, auditorium, row, place)
    
    if auditorium=='1':
        auditorium_sheet = Data_base().wb_films['Зал_1']
    elif auditorium=='2':
        auditorium_sheet = Data_base().wb_films['Зал_2']
    elif auditorium=='3':
        auditorium_sheet = Data_base().wb_films['Зал_3']
    elif auditorium=='4':
        auditorium_sheet = Data_base().wb_films['Зал_4']
    elif auditorium=='5':
        auditorium_sheet = Data_base().wb_films['Зал_5']
    else: messagebox.showerror('Ошибка', 'Неккоректный зал')

    if int(place)<=10 and int(place)>=1:
        if data.count('.')==2:  
            if time == '09:00':
                current_line = int(auditorium_sheet['D2'].value)+3
                if is_place_free(auditorium_sheet, current_line, 'A', 'B', 'C'):
                    auditorium_sheet[f'A{current_line}'] = row
                    auditorium_sheet[f'B{current_line}'] = place
                    auditorium_sheet[f'C{current_line}'] = data
                else: messagebox.showerror('Ошибка', 'Место занято')
            elif time == '11:30':
                current_line = int(auditorium_sheet['H2'].value)+3
                if is_place_free(auditorium_sheet, current_line, 'E', 'F', 'G'):
                    auditorium_sheet[f'E{current_line}'] = row
                    auditorium_sheet[f'F{current_line}'] = place
                    auditorium_sheet[f'G{current_line}'] = data
                else: messagebox.showerror('Ошибка', 'Место занято')
            elif time == '14:00':
                current_line = int(auditorium_sheet['L2'].value)+3
                if is_place_free(auditorium_sheet, current_line, 'I', 'J', 'K'):
                    auditorium_sheet[f'I{current_line}'] = row
                    auditorium_sheet[f'J{current_line}'] = place
                    auditorium_sheet[f'K{current_line}'] = data
                else: messagebox.showerror('Ошибка', 'Место занято')
            elif time == '16:30':
                current_line = int(auditorium_sheet['P2'].value)+3
                if is_place_free(auditorium_sheet, current_line, 'M', 'N', 'O'):
                    auditorium_sheet[f'M{current_line}'] = row
                    auditorium_sheet[f'N{current_line}'] = place
                    auditorium_sheet[f'O{current_line}'] = data
                else: messagebox.showerror('Ошибка', 'Место занято')
            elif time == '19:00':
                current_line = int(auditorium_sheet['T2'].value)+3
                if is_place_free(auditorium_sheet, current_line, 'Q', 'R', 'S'):
                    auditorium_sheet[f'Q{current_line}'] = row
                    auditorium_sheet[f'R{current_line}'] = place
                    auditorium_sheet[f'S{current_line}'] = data
                else: messagebox.showerror('Ошибка', 'Место занято')
            elif time == '21:30':
                current_line = int(auditorium_sheet['X2'].value)+3
                if is_place_free(auditorium_sheet, current_line, 'U', 'V', 'W'):
                    auditorium_sheet[f'U{current_line}'] = row
                    auditorium_sheet[f'V{current_line}'] = place
                    auditorium_sheet[f'W{current_line}'] = data
                else: messagebox.showerror('Ошибка', 'Место занято')
            else: messagebox.showerror('Ошибка', 'Неккоректное время')
        else: messagebox.showerror('Ошибка', 'Неккоректная дата')
    else: messagebox.showerror('Ошибка', 'Неккоректное место')

    if auditorium=='1':
        Data_base().auditorium_1 = auditorium_sheet
    elif auditorium=='2':
        Data_base().auditorium_2 = auditorium_sheet
    elif auditorium=='3':
        Data_base().auditorium_3 = auditorium_sheet
    elif auditorium=='4':
        Data_base().auditorium_4 = auditorium_sheet
    elif auditorium=='5':
        Data_base().auditorium_5 = auditorium_sheet

    Data_base.save_data_base(Data_base)

def is_place_free(auditorium_sheet, current_line, column_row, column_place, column_data):
        print(auditorium_sheet[f'{column_row}{current_line}'].value)
        print(auditorium_sheet[f'{column_place}{current_line}'].value)
        print(auditorium_sheet[f'{column_data}{current_line}'].value)
        if auditorium_sheet[f'{column_row}{current_line}'].value == None:
            if auditorium_sheet[f'{column_place}{current_line}'].value == None:
                if auditorium_sheet[f'{column_data}{current_line}'].value == None:
                    return True
        else: return False

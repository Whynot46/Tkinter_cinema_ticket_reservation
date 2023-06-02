from db import *


#Локальные данные пользователя
class User():
    def __init__(self):
        self.name = 'Guest'
        self.login = 'None'
        self.email = 'None'
        self.password = None
        self.repeat_password = None
        self.code = None
    #Обновление локальных пользовательских данных
    def change_user_data(self, login):
        line = 1
        while line!=Data_base().users_sheet[f'I2'].value+2:
            if Data_base().users_sheet[f'C{line}'].value == login:
                self.name = Data_base().users_sheet[f'B{line}'].value
                self.login = Data_base().users_sheet[f'C{line}'].value
                self.password = Data_base().users_sheet[f'D{line}'].value
                break
            line+=1
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton #модули Aiogram
from aiogram import Bot, Dispatcher, executor, types #модули Aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton #модули Aiogram
from base import SQL
import main #импортирование главного файла
import base #импортирование файла с функциями базы данных

db = SQL('infos.db')
#Inline
kbmain = InlineKeyboardMarkup().add( #Главное Меню Клавиатура
    InlineKeyboardButton(text='Моя полка', callback_data='shelf'), 
    InlineKeyboardButton(text="Инфо", callback_data= "info"),
    InlineKeyboardButton(text='Настройки', callback_data='settings'))

kback = InlineKeyboardMarkup().add( #Клавиатура назад
    InlineKeyboardButton(text='Назад', callback_data='back'))

kbinfo = InlineKeyboardMarkup().add( #Клавиатура информации
    InlineKeyboardButton(text="Назад", callback_data="back"),
    InlineKeyboardButton(text="GitHub", url="https://github.com/coteyka1209/ShelfDeck"))

kbackview = InlineKeyboardMarkup().add( #Клавиатура Назад в просмотре значений
    InlineKeyboardButton(text='Назад', callback_data='back'),
    InlineKeyboardButton(text='Изменить', callback_data='change'))

kbackchange = InlineKeyboardMarkup().add( #Клавиатура Назад в изменении значений
    InlineKeyboardButton(text='Назад', callback_data='backtoshelf'),
    InlineKeyboardButton(text='Просмотреть', callback_data='view'))

kbchooseaction = InlineKeyboardMarkup(row_width=2).add( #клавиатура для выбора действия
    InlineKeyboardButton(text='Изменить', callback_data ='change'),
    InlineKeyboardButton(text='Посмотреть', callback_data='view'),
    InlineKeyboardButton(text = 'Назад', callback_data='back'))

kbchoosemoney = InlineKeyboardMarkup(row_width=3).add( #клавиатура выбора купюры
    InlineKeyboardButton(text='1₽', callback_data='choose1R'),  #1
    InlineKeyboardButton(text='2₽', callback_data='choose2R'),  #2
    InlineKeyboardButton(text='5₽', callback_data='choose5R'),  #3
    InlineKeyboardButton(text='10₽', callback_data='choose10R'),  #4
    InlineKeyboardButton(text='50₽', callback_data='choose50R'),  #5
    InlineKeyboardButton(text='100₽', callback_data='choose100R'),  #6
    InlineKeyboardButton(text='200₽', callback_data='choose200R'),  #7
    InlineKeyboardButton(text='500₽', callback_data='choose500R'),  #8
    InlineKeyboardButton(text='1000₽', callback_data='choose1000R'),  #9
    InlineKeyboardButton(text='2000₽', callback_data='choose2000R'),  #10
    InlineKeyboardButton(text='5000₽', callback_data='choose5000R'), #11
    InlineKeyboardButton(text='Назад', callback_data='backtoshelf'))

kbeditvalue =  InlineKeyboardMarkup(row_width=3).add( #клавиатура для выбора действия
    InlineKeyboardButton(text='-', callback_data='-money'),
    InlineKeyboardButton(text='₽', callback_data='set'),
    InlineKeyboardButton(text='+', callback_data ='+money'),    
    InlineKeyboardButton(text = 'Назад', callback_data='changeback'))


    
#Basic kbs

#Defs
def Logging(type, subtype, message):
    finaltype = "notype"
    finalsubtype = "nosubtype"
    finalmessage = message
    match type:
        case "info":
            finaltype = "info."
        case "warn":
            finaltype = "warning."
        case "err":
            finaltype = "error."
    match subtype:
        case "user":
            finalsubtype= "user."
    finalprint = finaltype + finalsubtype + finalmessage
    print("log." + finalprint)

def summa (id):

    summa1 = db.get_money(id, "R1")*1
    summa2 = db.get_money(id, "R2")*2
    summa5 = db.get_money(id, "R5")*5
    summa10 = db.get_money(id, "R10")*10
    summa50 = db.get_money(id, "R50")*50
    summa100 = db.get_money(id, "R100")*100
    summa200 = db.get_money(id, "R200")*200
    summa500 = db.get_money(id, "R500")*500
    summa1000 = db.get_money(id, "R1000")*1000
    summa2000 = db.get_money(id, "R2000")*2000
    summa5000 = db.get_money(id, "R5000")*5000

    finalsumma = summa1+summa2+summa5+summa10+summa50+summa100+summa200+summa500+summa1000+summa2000+summa5000
    return finalsumma




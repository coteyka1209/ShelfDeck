from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton #модули Aiogram
from aiogram import Bot, Dispatcher, executor, types #модули Aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton #модули Aiogram
import main #импортирование главного файла


#Inline
kbmain = InlineKeyboardMarkup().add( #Главное Меню Клавиатура
    InlineKeyboardButton(text='Моя полка', callback_data='shelf'), 
    InlineKeyboardButton(text="Инфо", callback_data= "info"),
    InlineKeyboardButton(text='Настройки', callback_data='settings'))

kback = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Назад', callback_data='back'))
#Basic


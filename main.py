import config
import asyncio
import logging
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import time
from base import SQL
import threading
import datetime

#задаем уровень логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
db = SQL('infos.db') #соединение с БД

kbmain = InlineKeyboardMarkup().add( #Главное Меню Клавиатура
    InlineKeyboardButton(text='Моя полка', callback_data='shelf'), 
    InlineKeyboardButton(text="Инфо", callback_data= "info"),
    InlineKeyboardButton(text='Настройки', callback_data='settings'))


@dp.message_handler(content_types=['text'])
async def start(message):
    global chat_type, dbusname, dbname, dbstatus #Глобализация данных
    #Получение разных данных о пользователе локально
    id = message.from_user.id #получаем ID пользователя
    name = message.from_user.first_name #получаем имя пользователя (не ник)
    lname = message.from_user.last_name #получаем фамилию пользователя
    usname = message.from_user.username #получаем ник пользователя
    chat_type = message.chat.type
    
    if not db.user_exists(id): #Если данных пользователя нет в базе данных
        db.add_user(id, name, lname, usname, 0)
        db.update_status(id, 1)
        await message.answer ("Привет новый пользователь! Ваши данные записаны! Повторите пожалуйста вашу комманду!")
        print ("INFO:New.User:У нас новый пользователь! Это \"" + name + "\"")
        return
    
    if db.get_name != message.from_user.first_name: #Если пользователь изменил данные о себе в Telegram
        db.update_name(message.from_user.id, message.from_user.first_name)

    if db.get_usname != message.from_user.username:
        db.update_usname(message.from_user.id, message.from_user.username)     

    if db.get_lname != message.from_user.last_name:
        db.update_lname(message.from_user.id, message.from_user.last_name)
    
    
    if message.text == "/start":
        await message.answer("Главное меню бота.", reply_markup = kbmain)


@dp.callback_query_handler() #остальные inline кнопки
async def start_call(call):
    global chat_type, chatid
    id = call.from_user.id # Получаем ID пользователя, который отправил запрос.
    if call.data == "settings":
        await call.message.answer ("В разработке")
    if call.data == "settings":
        await call.message.answer ("Инфо - гитхаб (https://github.com/coteyka1209/ShelfDeck)")

        


   


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
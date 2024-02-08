import config #токен бота
import asyncio #модуль асинхронности
import logging #модуль логов
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton #модули Aiogram
from aiogram import Bot, Dispatcher, executor, types #модули Aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton #модули Aiogram
import keyboards #файл с клавиатурами
from base import SQL #модуль базы данных

#задаем уровень логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#обозначение параметров
bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
db = SQL('infos.db') #соединение с БД
kb = keyboards


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
        db.update_id_money(id)
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
            db.update_status(id,0)
            try:
                await message.edit_text("Главное меню бота", reply_markup = kb.kbmain)
            except:             
                await message.answer("Главное меню бота", reply_markup = kb.kbmain)


@dp.callback_query_handler() #остальные inline кнопки
async def start_call(call):
    global chat_type, chatid
    id = call.from_user.id # Получаем ID пользователя, который отправил запрос.
    if call.data == "settings": #"настройки" в главном меню
        db.update_status(id,0.1)
        try:
            await call.message.edit_text ("В разработке", reply_markup = kb.kback)
        except:
            await call.message.answer ("В разработке", reply_markup = kb.kback)
    if call.data == "info": #"инфо" в главном меню
        db.update_status(id,0.2)
        try:
            await call.message.edit_text ("Инфо - GitHub (https://github.com/coteyka1209/ShelfDeck)", reply_markup = kb.kback)
        except:
            await call.message.answer ("Инфо - GitHub (https://github.com/coteyka1209/ShelfDeck)", reply_markup = kb.kback)
    if call.data == "shelf":#ГЛАВНАЯ ФУНКЦИЯ! Доступ к полке.
        current1 = db.get_R1(id)
        current2 = db.get_R2(id)
        current5 = db.get_R5(id)
        current10 = db.get_R10(id)
        current50 = db.get_R50(id)
        current100 = db.get_R100(id)
        current200 = db.get_R200(id)
        current500 = db.get_R500(id)
        current1000 = db.get_R100(id)
        current2000 = db.get_R2000(id)
        current5000 = db.get_R5000(id)
        try:
            await call.message.edit_text("Это ваша полка. Значения:\n1₽ - {}\n2₽ - {}\n5₽ - {}\n10₽ - {}\n50₽ - {}\n100₽ - {}\n200₽ - {}\n500₽ - {}\n1000₽ - {}\n2000₽ - {}\n5000₽ - {}".format(current1, current2, current5, current10, current50, current100, current200, current500, current1000, current2000, current5000),reply_markup = kb.kback)
        except:             
            await call.message.edit_text("Это ваша полка. Значения:\n1₽ - {}\n2₽ - {}\n5₽ - {}\n10₽ - {}\n50₽ - {}\n100₽ - {}\n200₽ - {}\n500₽ - {}\n1000₽ - {}\n2000₽ - {}\n5000₽ - {}".format(db.get_1r, db.get_2r, db.get_5r, db.get_10r, db.get_50r, db.get_100r, db.get_200r, db.get_500r, db.get_1000r, db.get_2000r, db.get_5000r),reply_markup = kb.kback)

    if call.data == "back" or call.message.text == "/back":
        if db.get_status(id) == 0.1 or 0.2:
            db.update_status(id,0)
            try:
                await call.message.edit_text("Главное меню бота", reply_markup = kb.kbmain)
            except:             
                await call.message.answer("Главное меню бота", reply_markup = kb.kbmain)
            
    

        


   


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
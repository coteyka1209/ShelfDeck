#ВНИМАНИЕ! Этот код частично комментирован и написан с помощью chatGPT. Если вы это читаете, значит вы владелец и вам не нужна эта информация
#Импорт необходимого (и не очень)
import asyncio
import logging
import random #импорт модуля рандома
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from base import SQL
import config

gdzkb = InlineKeyboardMarkup().add( # Клавиатура для /gdz
        InlineKeyboardButton('Математика', callback_data='math'),
        InlineKeyboardButton('Русский', callback_data='rus'),
        InlineKeyboardButton('Английский', callback_data='eng'))

modekb = InlineKeyboardMarkup().add( # Клавиатура для /mode
        InlineKeyboardButton('Режим РП (Для групп', callback_data='grouprp'))

flipackb = InlineKeyboardMarkup().add( #Клавиатура для подбрасывания монетки
        InlineKeyboardButton('Подкинуть', callback_data='flip'))
randomkb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Монетка', callback_data='flip'),
        InlineKeyboardButton(text='Число', callback_data='randnum'),
        InlineKeyboardButton(text='Цвет', callback_data='randcolor')
    ]
])

#Уровень логов
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
db = SQL('infos.db') #соединение с БД


u_status = [] #Статус пользователей
admin_id = [1833854816] #ID админов (внеси сюда новые, чтобы добавить админа)
owner_id = 1833854816 #ID владельца (ну то есть тебя, не меняй его)

''' Обьяснение статусов
#----------------------------------
# Статус 0 - Не участвует ни в чем
# Статус 1 - Учебник
# Статус 2* - Упражнение:
#   2_1 - Упражнение в учебнике по Математике
#   2_2 - Упражнение в учебнике по Русскому Языку
#   2_3 - Страница в учебнике по Английскому Языку    
# Статус 3 - Написание отзыва
#
# * = несуществующие статусы (только в других их обличиях)
#----------------------------------
'''

'''Обьяснение режимов
Режим 0 - дефолт
Режим 1 - режим рп
'''

#Важные части (для других комманд)

color = ["Красный", "Оранжевый", "Желтый", "Зеленый", "Голубой", "Синий", "Фиолетовый", "Фисташковый... Подожди, фисташковый не цвет, это вкус"]

#Непонятно что .-.
@dp.message_handler(content_types=['text'])

#Кластер комманд
async def start(message):
    global chat_type, dbusname, dbname, dbstatus
    #Получение разных данных о пользователе локально
    id = message.from_user.id #получаем ID пользователя
    name = message.from_user.first_name #получаем имя пользователя (не ник)
    lname = message.from_user.last_name #получаем фамилию пользователя
    usname = message.from_user.username #получаем ник пользователя
    chat_type = message.chat.type
    if not db.user_exists(id): 
        db.add_user(id, name, lname, usname)
        await message.answer ("Привет, я записал твой ID и слушаю тебя")
        return
    
    #Обозначение разных параметров из ДБ
    dbname = db.get_name(id)
    dbstatus = db.get_status(id)

    #Админ ли пользователь
    if id in admin_id:
        isadmin = True
    else: 
        isadmin = False

    #Функция /report
    if dbstatus == "reptyp":
        await message.answer("Репорт отправлен!")
        db.update_status(id, 0)
        await bot.send_message(owner_id,"Новый отзыв: "+message.text)
        return
    
#Раздел комманд    
    if message.text == "/number" or message.text == "/number@mynew_adminbot":
        await message.answer("И выпало число: "+str(random.randint(1,100)))
    elif message.text == "/color" or message.text == "/color@mynew_adminbot":
        await message.answer("Выпал цвет: " + random.choice(color))
    elif message.text == "/random" or message.text == "/random@mynew_adminbot":
        await message.answer("Рандомные команды:\nЦвет - рандомный цвет\nЧисло - рандомное число (от 1 до 100)\nМонетка - подброс монетки", reply_markup = randomkb)
    elif message.text == "/flipacoin" or message.text == "/flipacoin@mynew_adminbot":
        await message.answer("Нажми на кнопку снизу чтобы подкинуть монетку", reply_markup = flipackb)
    elif message.text == "/soviet" or message.text == "/soviet@mynew_adminbot":
        await message.answer("Заинтересован? Вот ссылка на Советский язык от моего разработчика https://t.me/setlanguage/russian-ussr.")
    elif message.text == "/status" or message.text == "/status@mynew_adminbot":
        await message.answer(status)
    elif message.text == "/cancel" or message.text == "/cancel@mynew_adminbot":
        db.update_status(id, 0)
        await message.answer("Текущее действие отменено.")
    elif message.text == "/creationdate" or message.text == "/creationdate@mynew_adminbot":
        await message.answer("Я был создан @coteyka1209 **9 декабря 2022 год а в 10:45 PM**")
    elif message.text == "/name" or message.text == "/name@mynew_adminbot":
        await message.answer("Тебя зовут " + name)  
    elif message.text == "/id" or message.text == "/id@mynew_adminbot":
        if isadmin == True:
            await message.answer(db.id)
        else:
            await message.answer("Не знаю где ты достал эту комманду, но она только для админов")
    elif message.text == "/adminstatus" or message.text == "/adminstatus@mynew_adminbot":
        if isadmin == True:
            await message.answer("ДА! Вы - админ. Гордитесь этим")
        else:
            await message.answer("Где то в твоих мечтах...")
    elif message.text == "/report" or message.text == "/report@mynew_adminbot":
        if isadmin == True:
            await message.answer("Писать отзыв самому себе... нецелесообразно.")
        if isadmin == False:
            await message.answer("Введите свой репорт. Вы также можете предложить любую функцию. Если этот бот в группе, пишите репорт в ответ на это сообщение.")
            status = "3"
    elif message.text == "/mode" or message.text == "/mode@mynew_adminbot":
        await message.answer ("Выбери режим, который хочешь включить.", reply_markup=modekb)
    else:
        await message.answer("Я бы с радостью пообщался с тобой на свободную тему, но я всего лишь бот. Напиши /help чтобы посмотреть список комманд")

#Кластер Inline Кнопок
@dp.message_handler(content_types=['text'])
@dp.callback_query_handler()
async def start_call(call):
    global chat_type
    id = call.from_user.id # Получаем ID пользователя, который отправил запрос. 
    if call.data == "flip":
        chat_type = call.message.chat.type
        dbusname = db.get_usname(id)
        flipacoin = random.randint(1,2)
        if not dbusname == "":
            if chat_type == "private": #если это выполняется в приватном чате
                if flipacoin == 1:
                    await call.answer ("Подкинул, выпал орел")
                    await bot.answer_callback_query(call.id)
                if flipacoin == 2:
                    await call.answer ("Подкинул, выпала решка")
                    await bot.answer_callback_query(call.id)
            if chat_type == "group" or chat_type == "supergroup" or chat_type == "channel":
                if flipacoin == 1:
                    await call.message.answer("@" + str(dbusname) +" " + "подкинул монетку, ему выпал орел")
                    await bot.answer_callback_query(call.id)
                if flipacoin == 2:
                    await call.message.answer("@" + str(dbusname) +" " + "подкинул монетку, ему выпала решка")
                    await bot.answer_callback_query(call.id)
        if dbusname == "":
            if chat_type == "private": #если это выполняется в приватном чате
                if flipacoin == 1:
                    await call.answer ("Подкинул, выпал орел")
                    await bot.answer_callback_query(call.id)
                if flipacoin == 2:
                    await call.answer ("Подкинул, выпала решка")
                    await bot.answer_callback_query(call.id)
            if chat_type == "group" or chat_type == "supergroup" or chat_type == "channel":
                if flipacoin == 1:
                    await call.message.answer(str(dbname) + " подкинул монетку, ему выпал орел")
                    await bot.answer_callback_query(call.id)
                if flipacoin == 2:
                    await call.message.answer(str(dbname) +" подкинул монетку, ему выпала решка")
                    await bot.answer_callback_query(call.id)
    if call.data == 'randcolor':
        dbusname = db.get_usname(call.from_user.id)
        choicedcolor = random.choice(color)
        if dbusname:
            if call.message.chat.type == "private":
                await call.answer("Вам выпал " + str(choicedcolor))
            else:
                await call.message.answer("@" + str(dbusname) + " решил выбрать случайный цвет. Ему выпал: " + str(choicedcolor))
            await call.answer()
        else:
            if call.message.chat.type == "private":
                await call.answer("Вам выпал " + str(choicedcolor))
            else:
                await call.message.answer("Решил выбрать случайный цвет. Ему выпал: " + str(choicedcolor))
            await call.answer()
            
    if call.data == 'randnum':
        dbusname = db.get_usname(call.from_user.id)
        choicednum = random.randint(1, 100)

        if dbusname:
            if call.message.chat.type == "private":
                await call.answer("Вам выпало " + str(choicednum))
            else:
                await call.message.answer("@" + str(dbusname) + " решил выбрать случайное число. Ему выпало: " + str(choicednum))
            await call.answer()
        else:
            if call.message.chat.type == "private":
                await call.answer("Вам выпало " + str(choicednum))
            else:
                await call.message.answer("Решил выбрать случайное число. Ему выпало: " + str(choicednum))
            await call.answer()
#Не трогай!
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


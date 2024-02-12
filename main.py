import config #токен бота
import logging #модуль логов
from aiogram import Bot, Dispatcher, executor #модули Aiogram
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
    global dbusname, dbname, dbstatus #Глобализация данных
    #Получение разных данных о пользователе локально
    id = message.from_user.id #получаем ID пользователя
    name = message.from_user.first_name #получаем имя пользователя (не ник)
    lname = message.from_user.last_name #получаем фамилию пользователя
    usname = message.from_user.username #получаем ник пользователя
    
    if not db.user_exists(id): #Если данных пользователя нет в базе данных
        db.add_user(id, name, lname, usname, 0)
        db.update_id_money(id)
        db.update_status(id, 1)
        await message.answer ("Привет новый пользователь! Ваши данные записаны! Повторите пожалуйста вашу комманду!")
        kb.Logging("info","user","join: У нас новый пользователь! Это {} " .format(name))
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
    match call.data:
        case "settings": #Настройки в главном меню
            db.update_status(id,0.1)
            try:
              await call.message.edit_text ("В разработке", reply_markup = kb.kback)
            except:
               await call.message.answer ("В разработке", reply_markup = kb.kback)

        case "info": #Инфо в главном меню
            db.update_status(id,0.2)
            try:
                await call.message.edit_text ("Этот бот предназначен для хранения наличных в цифре. Так можно копить, вести учет, и много чего еще. Также, наш код есть на GitHub!", reply_markup = kb.kbinfo)
            except:
               await call.message.answer ("Этот бот предназначен для хранения наличных в цифре. Так можно копить, вести учет, и много чего еще. Также, наш код есть на GitHub!", reply_markup = kb.kbinfo)
        case "shelf": #ГЛАВНАЯ ФУНКЦИЯ! Доступ к полке.
            db.update_status(id,1)
            try:
                await call.message.edit_text("Это ваша полка.\nВыберите, что вы хотите сделать", reply_markup = kb.kbchooseaction)
            except:             
                await call.message.answer("Это ваша полка.\nВыберите, что вы хотите сделать", reply_markup = kb.kbchooseaction)
        case "view":
            db.update_status(id, 1.1)
            current1 = db.get_money(id, "R1")
            current2 = db.get_money(id, "R2")
            current5 = db.get_money(id, "R5")
            current10 = db.get_money(id, "R10")
            current50 = db.get_money(id, "R50")
            current100 = db.get_money(id, "R100")
            current200 = db.get_money(id, "R200")
            current500 = db.get_money(id, "R500")
            current1000 = db.get_money(id, "R1000")
            current2000 = db.get_money(id, "R2000")
            current5000 = db.get_money(id, "R5000")
            try:
                await call.message.edit_text("Значения:\nМонета 1₽ - {}\nМонета 2₽ - {}\nМонета 5₽ - {}\nМонета 10₽ - {}\nКупюра 50₽ - {}\nКупюра 100₽ - {}\nКупюра 200₽ - {}\nКупюра 500₽ - {}\nКупюра 1000₽ - {}\nКупюра 2000₽ - {}\nКупюра 5000₽ - {}\n\nСумма всех ваших купюр - {}".format(current1, current2, current5, current10, current50, current100, current200, current500, current1000, current2000, current5000,kb.summa(id)), reply_markup = kb.kbackview)
            except:             
                await call.message.answer("Значения:\nМонета 1₽ - {}\nМонета 2₽ - {}\nМонета 5₽ - {}\nМонета 10₽ - {}\nКупюра 50₽ - {}\nКупюра 100₽ - {}\nКупюра 200₽ - {}\nКупюра 500₽ - {}\nКупюра 1000₽ - {}\nКупюра 2000₽ - {}\nКупюра 5000₽ - {}\n\nСумма всех ваших купюр - {}".format(current1, current2, current5, current10, current50, current100, current200, current500, current1000, current2000, current5000, kb.summa(id)), reply_markup = kb.kbackview)
        case "change":
            try:
                await call.message.edit_text("Хорошо!\nДля начала, выберите валюту",reply_markup = kb.kbchoosemoney)
            except:
                await call.message.answer("Хорошо!\nДля начала, выберите валюту",reply_markup = kb.kbchoosemoney)
        
        case "choose1R":
            db.update_status(id, "1.2.1R")
            current = db.get_money(id, "R1")
            try:
                await call.message.edit_text("Изменяем: 1₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 1₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
      
        case "choose2R":
            db.update_status(id, "1.2.2R")
            current = db.get_money(id, "R2")
            try:
                await call.message.edit_text("Изменяем: 2₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 2₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
      
        case "choose5R":
            db.update_status(id, "1.2.5R")
            current = db.get_money(id, "R5")
            try:
                await call.message.edit_text("Изменяем: 5₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 5₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
       
        case "choose10R":
            db.update_status(id, "1.2.10R")
            current = db.get_money(id, "R10")
            try:
                await call.message.edit_text("Изменяем: 10₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 10₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
        
        case "choose50R":
            db.update_status(id, "1.2.50R")
            current = db.get_money(id, "R50")
            try:
                await call.message.edit_text("Изменяем: 50₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 50₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
        
        case "choose100R":
            db.update_status(id, "1.2.100R")
            current = db.get_money(id, "R100")
            try:
                await call.message.edit_text("Изменяем: 100₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 100₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)

        case "choose200R":
            db.update_status(id, "1.2.200R")
            current = db.get_money(id, "R200")
            try:
                await call.message.edit_text("Изменяем: 200₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 200₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
        
        case "choose500R":
            db.update_status(id, "1.2.500R")
            current = db.get_money(id, "R500")
            try:
                await call.message.edit_text("Изменяем: 500₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 500₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
        
        case "choose1000R":
            db.update_status(id, "1.2.1000R")
            current = db.get_money(id, "R1000")
            try:
                await call.message.edit_text("Изменяем: 1000₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 1000₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
        
        case "choose2000R":
            db.update_status(id, "1.2.2000R")
            current = db.get_money(id, "R2000")
            try:
                await call.message.edit_text("Изменяем: 2000₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 2000₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
        
        case "choose5000R":
            db.update_status(id, "1.2.5000R")
            current = db.get_money(id, "R5000")
            try:
                await call.message.edit_text("Изменяем: 5000₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
            except:
                await call.message.answer("Изменяем: 5000₽\nТекущее значение: {}".format (current), reply_markup = kb.kbeditvalue)
        
        case "+money":
            match db.get_status(id):
                case '1.2.1R':
                    moneyplus = db.get_money(id, "R1") + 1
                    db.update_money(id, "R1", moneyplus)
                    current = db.get_money(id, "R1")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 1₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 1₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.2R':
                    moneyplus = db.get_money(id, "R2") + 1
                    db.update_money(id, "R2", moneyplus)
                    current = db.get_money(id, "R2")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅")
                    try:
                        await call.message.edit_text("Изменяем: 2₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 2₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.5R':
                    moneyplus = db.get_money(id, "R5") + 1
                    db.update_money(id, "R5", moneyplus)
                    current = db.get_money(id, "R5")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅")
                    try:
                        await call.message.edit_text("Изменяем: 5₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 5₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.10R':
                    moneyplus = db.get_money(id, "R10") + 1
                    db.update_money(id, "R10", moneyplus)
                    current = db.get_money(id, "R10")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 10₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 10₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.50R':
                    moneyplus = db.get_money(id, "R50") + 1
                    db.update_money(id, "R50", moneyplus)
                    current = db.get_money(id, "R50")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 50₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 50₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.100R':
                    moneyplus = db.get_money(id, "R100") + 1
                    db.update_money(id, "R100", moneyplus)
                    current = db.get_money(id, "R100")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 100₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 100₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.200R':
                    moneyplus = db.get_money(id, "R200") + 1
                    db.update_money(id, "R200", moneyplus)
                    current = db.get_money(id, "R200")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 200₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 200₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.500R':
                    moneyplus = db.get_money(id, "R500") + 1
                    db.update_money(id, "R500", moneyplus)
                    current = db.get_money(id, "R500")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 500₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 500₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.1000R':
                    moneyplus = db.get_money(id, "R1000") + 1
                    db.update_money(id, "R1000", moneyplus)
                    current = db.get_money(id, "R1000")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 1000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 1000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.2000R':
                    moneyplus = db.get_money(id, "R2000") + 1
                    db.update_money(id, "R2000", moneyplus)
                    current = db.get_money(id, "R2000")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 2000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 2000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.5000R':
                    moneyplus = db.get_money(id, "R5000") + 1
                    db.update_money(id, "R5000", moneyplus)
                    current = db.get_money(id, "R5000")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 5000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 5000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

        case "-money":
            match db.get_status(id):
                case '1.2.1R':
                    moneyplus = db.get_money(id, "R1") - 1
                    db.update_money(id, "R1", moneyplus)
                    current = db.get_money(id, "R1")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 1₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 1₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.2R':
                    moneyplus = db.get_money(id, "R2") - 1
                    db.update_money(id, "R2", moneyplus)
                    current = db.get_money(id, "R2")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅")
                    try:
                        await call.message.edit_text("Изменяем: 2₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 2₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.5R':
                    moneyplus = db.get_money(id, "R5") - 1
                    db.update_money(id, "R5", moneyplus)
                    current = db.get_money(id, "R5")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅")
                    try:
                        await call.message.edit_text("Изменяем: 5₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 5₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.10R':
                    moneyplus = db.get_money(id, "R10") - 1
                    db.update_money(id, "R10", moneyplus)
                    current = db.get_money(id, "R10")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 10₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 10₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.50R':
                    moneyplus = db.get_money(id, "R50") - 1
                    db.update_money(id, "R50", moneyplus)
                    current = db.get_money(id, "R50")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 50₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 50₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.100R':
                    moneyplus = db.get_money(id, "R100") - 1
                    db.update_money(id, "R100", moneyplus)
                    current = db.get_money(id, "R100")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 100₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 100₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.200R':
                    moneyplus = db.get_money(id, "R200") - 1
                    db.update_money(id, "R200", moneyplus)
                    current = db.get_money(id, "R200")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 200₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 200₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.500R':
                    moneyplus = db.get_money(id, "R500") - 1
                    db.update_money(id, "R500", moneyplus)
                    current = db.get_money(id, "R500")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 500₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 500₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.1000R':
                    moneyplus = db.get_money(id, "R1000") - 1
                    db.update_money(id, "R1000", moneyplus)
                    current = db.get_money(id, "R1000")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 1000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 1000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.2000R':
                    moneyplus = db.get_money(id, "R2000") - 1
                    db.update_money(id, "R2000", moneyplus)
                    current = db.get_money(id, "R2000")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 2000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 2000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

                case '1.2.5000R':
                    moneyplus = db.get_money(id, "R5000") - 1
                    db.update_money(id, "R5000", moneyplus)
                    current = db.get_money(id, "R5000")
                    await bot.answer_callback_query(call.id)
                    await call.answer("✅") 
                    try:
                        await call.message.edit_text("Изменяем: 5000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)
                    except: 
                        await call.message.answer("Изменяем: 5000₽\nТекущее значение: {}".format(current), reply_markup=kb.kbeditvalue)

        case 'backchoose':
            db.update_status(id,1)
            try:
                await call.message.edit_text("Это ваша полка.\nВыберите, что вы хотите сделать", reply_markup = kb.kbchooseaction)
            except:             
                await call.message.answer("Это ваша полка.\nВыберите, что вы хотите сделать", reply_markup = kb.kbchooseaction)

    

    
        case "changeback":
            db.update_status(id,1)
            try:
                await call.message.edit_text("Это ваша полка.\nВыберите, что вы хотите сделать", reply_markup = kb.kbchooseaction)
            except:             
                await call.message.answer("Это ваша полка.\nВыберите, что вы хотите сделать", reply_markup = kb.kbchooseaction)



    
    if call.data == "back" or call.message.text == "/back":
        db.update_status(id,0)
        try:
            await call.message.edit_text("Главное меню бота", reply_markup = kb.kbmain)
        except:             
            await call.message.answer("Главное меню бота", reply_markup = kb.kbmain)

    

        


   


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
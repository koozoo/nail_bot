from aiogram import Dispatcher, types
from aiogram.types import Message
import bot.keyboards.inline as nav
from bot.misc.GoogleSheets import GoogleSheet
from bot.misc.util import print_data
from bot.misc.config import MASTER_NAME, DB_NAME
import bot.keyboards.reply as rel
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from bot.database.methods import add, get, update

gs = GoogleSheet()


async def start(msg: Message):
    user = msg.from_user
    user_id = user.id
    user_name = user.full_name
    # user_phone = msg.contact.phone_number

    text = f'Привет, {user_name}.\nменя зовут {MASTER_NAME}, хотите записаться на прием или узнать цены на услуги?\n'

    # обновляем дату на сегодняшнюю, со смещением всех заказов
    gs.update_date_in_sheets()

    # user_data = (user_id, )

    await msg.bot.send_message(msg.from_user.id, text, reply_markup=nav.mainMenu)


async def back(msg: Message):
    user_name = msg.from_user.first_name
    await msg.bot.delete_message(msg.from_user.id, msg.message.message_id)
    await msg.bot.send_message(msg.from_user.id, f'{user_name}, желаете записаться ?', reply_markup=nav.mainMenu)


async def watch_price(msg: types.Message):
    # get price data -> 'p_data'
    price_range, dimension = 'прайс!B2:C32', 'ROWS'
    p_data = gs.get_data_sheets(price_range, dimension)
    await msg.bot.delete_message(msg.from_user.id, msg.message.message_id)
    await msg.bot.send_message(msg.from_user.id, print_data(p_data), reply_markup=nav.subMenuPrice)


async def print_week_keybord(msg: types.Message):
    await msg.bot.delete_message(msg.from_user.id, msg.message.message_id)
    await msg.bot.send_message(msg.from_user.id, f'выбирите неделю', reply_markup=nav.weekMenu)


async def print_day_keybord(call: types.callback_query):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    num_week = int(call.data[-1]) - 1
    weeks = gs.get_week_date()
    days = gs.get_available_day(weeks[num_week])
    for_print_lst = []
    for day in days:
        for_print_lst.append(day[0][:2])
    match num_week:
        case 0:
            await call.bot.send_message(call.from_user.id, f'выбирите неделю',
                                        reply_markup=nav.day_keyboard('time',days, for_print_lst))
        case 1:
            await call.bot.send_message(call.from_user.id, f'выбирите неделю',
                                        reply_markup=nav.day_keyboard('time',days, for_print_lst))
        case 2:
            await call.bot.send_message(call.from_user.id, f'выбирите неделю',
                                        reply_markup=nav.day_keyboard('time',days, for_print_lst))
        case 3:
            await call.bot.send_message(call.from_user.id, f'выбирите неделю',
                                        reply_markup=nav.day_keyboard('time',days, for_print_lst))
        case 4:
            await call.bot.send_message(call.from_user.id, f'выбирите неделю',
                                        reply_markup=nav.day_keyboard('time',days, for_print_lst))


async def print_time_keybord(call: types.callback_query):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    day = call.data[-5:]
    time = gs.get_time_in_day(day)
    await call.bot.send_message(call.from_user.id, f'выбирите время',
                                reply_markup=nav.time_keyboard('unit', day, time))


async def add_order(call: types.callback_query):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, 'Для продолжения нажмите на кнопку "Поделиться контактом"'
                                                   ' (для получения контактных данных).', reply_markup=rel.btnContact)

    data = []
    data.append(call.from_user.id)
    data.append(call.from_user.full_name)
    data.append('$'.join(call.data.split(".")))

    get_db = get.GetDataBase(DB_NAME)

    user_in_db = get_db.get_data_where_id(call.from_user.id)
    if user_in_db:
        up_db = update.UpdateDataBase(DB_NAME)
        up_db.update_step1(data[0], data[1:])
    else:
        add_db = add.InsertDataBase(DB_NAME)
        add_db.add_data_step1(data)


async def update_contact_in_table(msg: types.Message):
    db = get.GetDataBase(DB_NAME)
    data = db.get_data_where_id(msg.from_user.id)
    print(data)
    phone = ''
    if msg.contact is not None:
        phone = msg.contact.phone_number

    update_db = update.UpdateDataBase(DB_NAME)
    update_db.update_phone(msg.from_user.id, phone)

    if data[0][1] != None:
        await msg.bot.send_message(msg.from_user.id,
                                   f"{str(data[0][1]).capitalize()}, ждем вас на прием.")
        cq = data[0][-2]
        cell_number = gs.write_order_in_table(cq, [i for i in data[0][:-2]])
        update_db.update_cell_number(msg.from_user.id, cell_number)
    else:
        await msg.bot.send_message(msg.from_user.id, f"Ваше имя {msg.from_user.full_name},"
                                                     f" все верно ?\nЕсли хотите изменить наберите,"
                                                     f" наберите /ch_name ВАШЕ ИМЯ")
        cq = data[0][-2]
        cell_number = gs.write_order_in_table(cq, [i for i in data[0][:-2] if i != None])
        update_db.update_cell_number(msg.from_user.id, cell_number)


async def change_name(msg: types.Message):
    name = msg.text[8:]
    update_db = update.UpdateDataBase(DB_NAME)
    update_db.update_name(msg.from_user.id, name)
    await msg.bot.send_message(msg.from_user.id, f"{name} благодарим вас, за уточнение имени. ")


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.register_message_handler(start, commands=['start', 'main'])
    dp.register_callback_query_handler(watch_price, text='btnPrice')
    dp.register_callback_query_handler(back, text='btnBack')
    dp.register_callback_query_handler(print_week_keybord, text='addEvent')
    dp.register_callback_query_handler(print_day_keybord, text_contains='week')
    dp.register_callback_query_handler(print_time_keybord, text_contains='time')
    dp.register_callback_query_handler(add_order, text_contains='unit')
    dp.register_message_handler(update_contact_in_table, content_types=['contact'])
    dp.register_message_handler(change_name, commands=['ch_name'])







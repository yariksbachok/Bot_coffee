from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
import datetime
from dateutil import relativedelta as rdelta
from datetime import date
from datetime import datetime
from asyncio import sleep
import hashlib
import config
import keyboard
import database
import logic


bot = Bot(token=config.TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())

class contacts(StatesGroup):
    phone = State()

class buy_coffee(StatesGroup):
    id_coffee = State()
    grind = State()
    method = State()
    Weight = State()
    Quantity = State()
    Payment = State()
    comment = State()
    promo = State()

class buy_coffee_change(StatesGroup):
    id_coffee_change = State()
    grind_change = State()
    method_change = State()
    Weight_change = State()
    Quantity_change = State()
    Payment_change = State()
    comment_change = State()

class info_profile(StatesGroup):
    phone = State()
    Fio = State()
    nova_poshta = State()
    adrees = State()
    city = State()
    notification_day = State()
    mailing = State()
    promo = State()
    promo_day = State()
    salse_promo = State()


@dp.message_handler(state=info_profile.notification_day)
async def notification_day(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        n = int(message.text)
        db.update_notifical_day(n, 1)
        inline, text = logic.admin_panel()
        await bot.send_message(message.chat.id, text=text, reply_markup=inline)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, text='Уведите число')
        await info_profile.notification_day.set()

@dp.message_handler(state=info_profile.mailing)
async def mailing(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text='Рассылка запущенна\nПосле завершения рассылки вам прийдет уведомления')
    inline, text = logic.admin_panel()
    await bot.send_message(message.chat.id, text=text, reply_markup=inline)
    await state.finish()
    await mailing_profile(message.text)

@dp.message_handler(state=info_profile.promo)
async def promo(message: types.Message, state: FSMContext):
    await state.update_data(promo=message.text)
    cancel = keyboard.cancel_create_promo()
    await bot.send_message(message.chat.id, text='Уведите дни действия промо, например (7)', reply_markup=cancel)
    await info_profile.salse_promo.set()

@dp.message_handler(state=info_profile.salse_promo)
async def salse_promo(message: types.Message, state: FSMContext):
    await state.update_data(salse_promo=message.text)
    cancel = keyboard.cancel_create_promo()
    await bot.send_message(message.chat.id, text='Увежите скидку для промокода(она будет в процентах), например (10)', reply_markup=cancel)
    await info_profile.promo_day.set()

@dp.message_handler(state=info_profile.promo_day)
async def promo_day(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    promo = user_data['promo']
    salse_promo = user_data['salse_promo']
    db.promo(promo, int(message.text), int(salse_promo))
    inline, text = logic.admin_panel()
    await bot.send_message(message.chat.id, text=text, reply_markup=inline)
    await state.finish()
    await send_promo_all_user()

@dp.message_handler(state=contacts.phone)
async def phone(message: types.Message, state: FSMContext):
    if message.text in keyboard.start_button or message.text in keyboard.Application_button:
        await bot.send_message(message.chat.id, text=keyboard.eror_input)
        button = keyboard.create_start_btn()
        await bot.send_message(message.chat.id, text=keyboard.text_start, reply_markup=button)

    txt = '📲 Контакты\n' \
          f'Текст пользователя: {message.text}\n' \
          f'Username: @{message.from_user.username}\n' \
          f'ID: {message.from_user.id}'

    for i in config.admins:
        await bot.send_message(i, text=txt)

    await state.finish()


@dp.message_handler(state=buy_coffee.comment)
async def comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await bot.send_message(message.chat.id, text='Если у вас есть промокод укажите его, усли нет напишите "-"б усли вы его сейчас уведете промокод будет активирован')
    await buy_coffee.promo.set()

@dp.message_handler(state=buy_coffee.promo)
async def buy_coffee_promo(message: types.Message, state: FSMContext):
    await state.update_data(prom= message.text)
    inline = keyboard.choose_quatyliti(1)
    user_data = await state.get_data()
    Weight = user_data['Weight']
    opt = logic.get_opt(Weight, 1)
    text = keyboard.quantly_coffee + '\n' + opt
    await bot.send_message(message.chat.id, text=text, reply_markup=inline)
    await buy_coffee.Quantity.set()



@dp.message_handler(state=buy_coffee.Weight)
async def Weight(message: types.Message, state: FSMContext):
    if message.text ==keyboard.first_weight or message.text== keyboard.second_weight:
        await state.update_data(Weight=message.text)
        await bot.send_message(message.chat.id, text=keyboard.text_coments)
        await buy_coffee.comment.set()
    else:
        await bot.send_message(message.chat.id, text='Используйте кнопки ниже')




@dp.message_handler(state=buy_coffee.method)
async def method(message: types.Message, state: FSMContext):
    await state.update_data(method=message.text)
    button = keyboard.btn_weight()
    await bot.send_message(message.chat.id, text=keyboard.chose_weight, reply_markup=button)
    await buy_coffee.Weight.set()



@dp.message_handler(state=buy_coffee.grind)
async def grind(message: types.Message, state: FSMContext):
    if message.text == 'Смолоть':
        await state.update_data(grind=message.text)
        await bot.send_message(message.chat.id, text=keyboard.write_method)
        await buy_coffee.method.set()

    elif message.text== 'Не смалывать':
        await state.update_data(grind=message.text)
        await state.update_data(method='None')
        button = keyboard.btn_weight()
        await bot.send_message(message.chat.id, text=keyboard.chose_weight, reply_markup=button)
        await buy_coffee.Weight.set()

    else:
        await bot.send_message(message.chat.id, text='Используйте кнопки ниже')

@dp.message_handler(state=buy_coffee_change.grind_change)
async def grind(message: types.Message, state: FSMContext):
    if message.text == 'Смолоть' or message.text== 'Не смалывать':
        user_data = await state.get_data()
        id_coffe = user_data['id_coffee']
        db.updateGrind(message.text, int(id_coffe))
        logic.get_all_price_change(id_coffe)
        row = db.show_my_order(int(id_coffe))
        text, inline = logic.create_basket(row)
        await bot.send_message(message.from_user.id, text=text,
                                    reply_markup=inline)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, text='Используйте кнопки ниже')

@dp.message_handler(state=info_profile.phone)
async def phone_info(message: types.Message, state: FSMContext):
    if message.text.startswith('0'):
        await state.update_data(phone=message.text)
        await bot.send_message(message.chat.id, text='Введите ФИО:')
        await info_profile.Fio.set()
    else:
        await bot.send_message(message.chat.id, text='Некорретный ввод! Введите номер телефона в числовом формате')
        await info_profile.phone.set()

@dp.message_handler(state=info_profile.Fio)
async def Fio_info(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await bot.send_message(message.chat.id, text='Введите Город:')
    await info_profile.city.set()

@dp.message_handler(state=info_profile.city)
async def city_info(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data()
    what = user_data['payment']
    if 'nova' in what:
        await bot.send_message(message.chat.id, text='Введите отделение Новой почты:')
        await info_profile.nova_poshta.set()

    elif 'delivery' in what:
        await bot.send_message(message.chat.id, text='Введите адрес для доставки:')
        await info_profile.adrees.set()

    elif 'pickup' in what:
        user_data = await state.get_data()
        what = user_data['payment']
        phone = user_data['phone']
        fio = user_data['fio']
        city = user_data['city']
        if ':card_not' in what:
            db.update_pickup(message.from_user.id, phone, fio, city)
            await state.finish()
            await send_admin_goods(card=False, what=what, pickup=True)

        elif ':card_yes' in what:
            db.update_pickup(message.from_user.id, phone, fio, city)
            inline = logic.payment(what)
            await bot.send_message(message.chat.id, text='<b>Оплата:</b>', reply_markup=inline)
            await state.finish()

async def send_admin_goods(card, what, poshta=None, pickup=None, delivery=None):
    text = what.split(':')
    first = text[0]
    last = text[-1]
    n = 0
    for id_zakaz in text:
        if id_zakaz == first:
            pass

        elif id_zakaz == last:
            pass

        else:
            row_zakaz = db.show_weight(id_zakaz)
            row_profile = db.show_user(row_zakaz[0])
            row_goods = db.show_price_coffe(row_zakaz[7])
            db.update_orderr(id_zakaz, 'True')
            db.update_last_zakaz(row_zakaz[0])
            n+=1
            if n == 1:
                await bot.send_message(row_zakaz[0], text=f'Супер🤘Мы уже пакуем твой кофе.\n\n'
                                                          f'Киев, Плодовая 1 (район Берковец), с понедельника по пятницу с 10:00 до 16:00\n\n'
                                                          f'Остались вопросы? Позвони нашему чемпиону Паше +380931063569 🙌\n\n'
                                                          f'пс: работаем каждый будний день, кроме праздников', )
            if row_zakaz[9] == 'True':
                n = 'False'
                db.update_basket(n, int(id_zakaz))
            if poshta != None:
                if card == True:
                    text = f'<b>Заказ #{id_zakaz}</b>\n\n' \
                            '<b>Оплата: Новая Почта (картой)</b>\n' \
                            f'Товар: {row_goods[0]} \n' \
                            f'Вес: {row_zakaz[3]} \n' \
                            f'Количество: {row_zakaz[4]} \n' \
                            f'{row_zakaz[1]} \n'
                    if row_zakaz[2] != 'None':
                        text+=f'Метод: {row_zakaz[2]} \n'

                    text+=f'Коментарий: {row_zakaz[10]}\n' \
                        f'Итого: {row_zakaz[6]} UAH\n\n' \
                        'Заказчик:\n\n' \
                        f'ФИО: {row_profile[2]}\n' \
                        f'Тел: {row_profile[1]}\n' \
                        f'Город: {row_profile[5]}\n' \
                        f'Отделение новой почты: {row_profile[3]}'
                    for i in config.admins:
                        await bot.send_message(i, text=text)
                else:
                    text = f'<b>Заказ #{id_zakaz}</b>\n\n' \
                            '<b>Оплата: Новая Почта (наличними)</b>\n' \
                            f'Товар: {row_goods[0]} \n' \
                            f'Вес: {row_zakaz[3]} \n' \
                            f'Количество: {row_zakaz[4]} \n' \
                            f'{row_zakaz[1]} \n'
                    if row_zakaz[2] != 'None':
                        text+=f'Метод: {row_zakaz[2]} \n'

                    text+=f'Коментарий: {row_zakaz[10]}\n' \
                        f'Итого: {row_zakaz[6]} UAH\n\n' \
                        'Заказчик:\n\n' \
                        f'ФИО: {row_profile[2]}\n' \
                        f'Тел: {row_profile[1]}\n' \
                        f'Город: {row_profile[5]}\n' \
                        f'Отделение новой почты: {row_profile[3]}'
                    for i in config.admins:
                        await bot.send_message(i, text=text)

            elif delivery != None:
                if card == True:
                    text = f'<b>Заказ #{id_zakaz}</b>\n\n' \
                            '<b>Оплата: Самовывоз (картой)</b>\n' \
                            f'Товар: {row_goods[0]} \n' \
                            f'Вес: {row_zakaz[3]} \n' \
                            f'Количество: {row_zakaz[4]} \n' \
                            f'{row_zakaz[1]} \n'
                    if row_zakaz[2] != 'None':
                        text+=f'Метод: {row_zakaz[2]} \n'

                    text+=f'Коментарий: {row_zakaz[10]}\n' \
                            f'Итого: {row_zakaz[6]} UAH\n\n' \
                            'Заказчик:\n\n' \
                            f'ФИО: {row_profile[2]}\n' \
                            f'Тел: {row_profile[1]}\n' \
                            f'Город: {row_profile[5]}\n' \
                            f'Адрес: {row_profile[4]}'
                    for i in config.admins:
                        await bot.send_message(i, text=text)
                else:
                    text = f'<b>Заказ #{id_zakaz}</b>\n\n' \
                            '<b>Оплата: Адресная доставка (наличними)</b>\n' \
                            f'Товар: {row_goods[0]} \n' \
                            f'Вес: {row_zakaz[3]} \n' \
                            f'Количество: {row_zakaz[4]} \n' \
                            f'{row_zakaz[1]} \n'
                    if row_zakaz[2] != 'None':
                        text+=f'Метод: {row_zakaz[2]} \n'

                    text+=f'Итого: {row_zakaz[6]} UAH\n\n' \
                            'Заказчик:\n\n' \
                            f'ФИО: {row_profile[2]}\n' \
                            f'Тел: {row_profile[1]}\n' \
                            f'Город: {row_profile[5]}\n' \
                            f'Адрес: {row_profile[4]}'
                    for i in config.admins:
                        await bot.send_message(i, text=text)

            elif pickup != None:
                if card == True:
                    text = f'<b>Заказ #{id_zakaz}</b>\n\n' \
                            '<b>Оплата: Адресная доставка (картой)</b>\n' \
                            f'Товар: {row_goods[0]} \n' \
                            f'Вес: {row_zakaz[3]} \n' \
                            f'Количество: {row_zakaz[4]} \n' \
                            f'{row_zakaz[1]} \n'
                    if row_zakaz[2] != 'None':
                        text+=f'Метод: {row_zakaz[2]} \n'
                    text+=f'Коментарий: {row_zakaz[10]}\n' \
                            f'Итого: {row_zakaz[6]} UAH\n\n' \
                            'Заказчик:\n\n' \
                            f'ФИО: {row_profile[2]}\n' \
                            f'Тел: {row_profile[1]}\n' \
                            f'Город: {row_profile[5]}\n'
                    for i in config.admins:
                        await bot.send_message(i, text=text)
                else:
                    text = f'<b>Заказ #{id_zakaz}</b>\n\n' \
                            '<b>Оплата: Адресная доставка (наличними)</b>\n' \
                            f'Товар: {row_goods[0]} \n' \
                            f'Вес: {row_zakaz[3]} \n' \
                            f'Количество: {row_zakaz[4]} \n' \
                            f'{row_zakaz[1]} \n'
                    if row_zakaz[2] != 'None':
                        text+=f'Метод: {row_zakaz[2]} \n'
                    text+=f'Коментарий: {row_zakaz[10]}\n' \
                            f'Итого: {row_zakaz[6]} UAH\n\n' \
                            'Заказчик:\n\n' \
                            f'ФИО: {row_profile[2]}\n' \
                            f'Тел: {row_profile[1]}\n' \
                            f'Город: {row_profile[5]}\n'
                    for i in config.admins:
                        await bot.send_message(i, text=text)

@dp.message_handler(state=info_profile.nova_poshta)
async def nova_poshta_info(message: types.Message, state: FSMContext):
    nova_poshta = message.text
    user_data = await state.get_data()
    what = user_data['payment']
    phone = user_data['phone']
    fio = user_data['fio']
    city = user_data['city']
    if ':card_not' in what:
        db.update_nova_poshta(message.from_user.id, phone, fio, nova_poshta, city)
        await state.finish()
        await send_admin_goods(card=False, what=what, poshta=True)

    elif ':card_yes' in what:
        db.update_nova_poshta(message.from_user.id, phone, fio, nova_poshta, city)
        inline = logic.payment(what)
        await bot.send_message(message.chat.id, text='<b>Оплата:</b>', reply_markup=inline)
        await state.finish()


@dp.message_handler(state=info_profile.adrees)
async def nova_poshta_info(message: types.Message, state: FSMContext):
    nova_poshta = message.text
    user_data = await state.get_data()
    what = user_data['payment']
    phone = user_data['phone']
    fio = user_data['fio']
    city = user_data['city']
    if ':card_not' in what:
        db.update_delivery(message.from_user.id, phone, fio, nova_poshta, city)

        await send_admin_goods(card=False, what=what, delivery=True)

    elif ':card_yes' in what:
        db.update_delivery(message.from_user.id, phone, fio, nova_poshta, city)
        inline = logic.payment(what)
        await bot.send_message(message.chat.id, text='<b>Оплата:</b>', reply_markup=inline)
        await state.finish()


@dp.message_handler(state=buy_coffee_change.method_change)
async def methos_change(message: types.Message, state: FSMContext):
        user_data = await state.get_data()
        id_coffe = user_data['id_coffee']
        db.updateMethod(message.text, int(id_coffe))
        row = db.show_my_order(int(id_coffe))
        text, inline = logic.create_basket(row)
        await bot.send_message(message.from_user.id, text=text,
                                    reply_markup=inline)
        await state.finish()


@dp.message_handler(state=buy_coffee_change.comment_change)
async def comment_change(message: types.Message, state: FSMContext):
        user_data = await state.get_data()
        id_coffe = user_data['id_coffee']
        db.updateComment(message.text, int(id_coffe))
        row = db.show_my_order(int(id_coffe))
        text, inline = logic.create_basket(row)
        await bot.send_message(message.from_user.id, text=text,
                                    reply_markup=inline)
        await state.finish()


@dp.message_handler(state=buy_coffee_change.Weight_change)
async def methos_weight(message: types.Message, state: FSMContext):
    if message.text ==keyboard.first_weight or message.text== keyboard.second_weight:
        user_data = await state.get_data()
        id_coffe = user_data['id_coffee']
        db.updateWeight(message.text, int(id_coffe))
        logic.get_all_price_change(int(id_coffe))
        row = db.show_my_order(int(id_coffe))
        text, inline = logic.create_basket(row)
        await bot.send_message(message.from_user.id, text=text,
                               reply_markup=inline)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, text='Используйте кнопки ниже')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    button = keyboard.create_start_btn()
    await bot.send_message(message.chat.id, text=keyboard.text_start, reply_markup=button)
    row = db.show_user(int(message.from_user.id))
    if row == None:
        data = 'None'
        db.add_user(int(message.from_user.id), data, data, data, data, data, data, data)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.from_user.id in config.admins:
        inline, text = logic.admin_panel()
        await bot.send_message(message.chat.id, text=text, reply_markup=inline)


@dp.message_handler(content_types=['text'], state="*")
async def text(message: types.Message, state: FSMContext):
    txt = message.text
    if txt == '🤟 Магазин':
        with open('static/photo_bot/first_photo.jpg', 'rb') as f1, open('static/photo_bot/second_photo.jpg',
                                                                        'rb') as f2, open(
                'static/photo_bot/the_three_photo.jpg', 'rb') as f3:
            await bot.send_media_group(message.chat.id, media=[types.InputMediaPhoto(f1), types.InputMediaPhoto(f2), types.InputMediaPhoto(f3)])
            inline = keyboard.our_price()
            await bot.send_message(message.chat.id, text=keyboard.our_price_text, reply_markup=inline)

    elif txt == '📌 Блог':
        inline = keyboard.btn_blog()
        await bot.send_message(message.chat.id, text='Наш канал @champsblog', reply_markup=inline)

    elif txt == '🔺 Настройки':
        btn = keyboard.setting_lang()
        await bot.send_message(message.chat.id, text=keyboard.setting_text, reply_markup=btn)

    elif txt == '📲 Контакты':
        inline = keyboard.call_me()
        await bot.send_message(message.chat.id, text=keyboard.call_me_text, reply_markup=inline)

    elif txt == '🤝 Оптовые продажи':
        button = keyboard.send_Application()
        await bot.send_message(message.chat.id, text=keyboard.Application_text, reply_markup=button)

    elif txt == '📘 Информация о кофе':
        await bot.send_message(message.chat.id, text=keyboard.info_of_kofe)

    elif txt == '🏠 В меню':
        button = keyboard.create_start_btn()
        await bot.send_message(message.chat.id, text=keyboard.back_menu_text, reply_markup=button)

    elif txt == '📦 Заказы':
        inline = logic.show_order(message.from_user.id)
        if len(inline.inline_keyboard) != 0:
            await bot.send_message(message.chat.id, text=keyboard.you_have_order, reply_markup=inline)
        else:
            await bot.send_message(message.chat.id, text=keyboard.you_have_not_order)

    elif txt == '🛒 Корзина':
        inline = logic.show_basket(message.from_user.id)
        if len(inline.inline_keyboard) > 1:
            await bot.send_message(message.chat.id, text=keyboard.you_have_basket, reply_markup=inline)
        else:
            await bot.send_message(message.chat.id, text=keyboard.you_have_not_basket)

    elif txt == '🇷🇺 Русский':
        button = keyboard.create_start_btn()
        await bot.send_message(message.chat.id, text=keyboard.back_menu_text, reply_markup=button)

    elif txt == '🇺🇦 Українська':
        button = keyboard.create_start_btn()
        await bot.send_message(message.chat.id, text=keyboard.back_menu_text, reply_markup=button)

    else:
        if 'Price:' in message.text:
            pass
        elif message.chat.id == config.group_id:
            id_user = message.reply_to_message.text.split(':')[1]
            id = ''
            for i in id_user:
                if i.isdigit():
                    id += i
            text = message.text
            await bot.send_message(int(id), text=text)
        else:
            row = db.show_group(int(message.from_user.id))
            if row == None:

                inline = keyboard.first_msg()
                await bot.send_message(config.group_id, text=f'<b>ID:{message.from_user.id}\nUsername: @{message.from_user.username}</b>\nТекст: {message.text}', reply_markup=inline)
            else:
                await bot.send_message(config.group_id,
                                       text=f'<b>ID:{message.from_user.id}\nUsername: @{message.from_user.username}</b>\nТекст: {message.text}')



@dp.callback_query_handler(lambda c: c.data, state="*")
async def callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'call_me':
        await bot.send_message(call.message.chat.id, text=keyboard.get_contact)
        await contacts.phone.set()

    elif call.data == 'interval':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, text='Уведите интервал например(21)')
        await info_profile.notification_day.set()

    elif call.data == 'admin_yes':
        print(call)
        id_user = call.message.text.split(':')[1]
        id_user = id_user.split('\n')[0]
        d = str(call.message.date)
        r = d.split(' ')[0]
        db.add_group(int(id_user), r)
        await bot.send_message(config.group_id, text='Вы участвуете в диалоге с пользвателем')
        await bot.send_message(id_user, text='Админ на связи')


    elif call.data == 'off_notifical':
        db.update_notification('False', 1)
        inline, text = logic.admin_panel()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=inline)

    elif call.data == 'create_promo':
        inline = keyboard.cancel_create_promo()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Уведите промо:', reply_markup=inline)
        await info_profile.promo.set()

    elif call.data == 'cancel_create_promo':
        inline, text = keyboard.cancel_create_promo()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=text, reply_markup=inline)
        await state.finish()

    elif call.data == 'on_notifical':
        db.update_notification('True', 1)
        inline, text = logic.admin_panel()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=inline)

    elif call.data == 'mailing':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, text='Уведите текст для рассылки')
        await info_profile.mailing.set()

    elif 'change_basket:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        inline = keyboard.chenge_order(int(n))
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, inline_message_id=call.inline_message_id, reply_markup=inline)

    elif call.data == 'estimate_delivery':
        inline = keyboard.estimate_product(1)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=keyboard.text_week_three, reply_markup=inline)

    elif call.data == 'estimate_product':
        inline = keyboard.estimate_bot(1)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=keyboard.text_week_three, reply_markup=inline)

    elif call.data == 'estimate_bot':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    elif 'back_basket' in call.data:
        inline = logic.show_basket(call.from_user.id)
        if len(inline.inline_keyboard) != 0:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=keyboard.you_have_basket, reply_markup=inline)
        else:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,  text=keyboard.you_have_not_basket)

    elif 'delete_profile:' in call.data:
        db.delete_profile(int(call.from_user.id))
        data = 'None'
        db.add_user(int(call.from_user.id), data, data, data, data, data, data, data)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        n = call.data
        n = n.lower().split(':')[-1]
        inline, text = logic.inline_payment(id_order=n, id_user=call.from_user.id)
        await bot.send_message(call.message.chat.id, text=text, reply_markup=inline)

    elif 'order_from_bs:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        inline, text = logic.inline_payment(id_order=int(n), id_user=int(call.from_user.id))
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=inline)

    elif 'order_from_basket' in call.data:
        all_basket = db.show_basket(call.from_user.id)
        inline, text = logic.inline_payment(all=all_basket, id_user=int(call.from_user.id))
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=inline)

    elif ':card_not' in call.data:
        n = call.data
        n = n.lower().split(':')[1]
        text_r = call.data
        text_r = text_r.split(':')
        first = text_r[0]
        last = text_r[-1]
        bool = True
        for i in text_r:
            if first == i:
                pass
            elif last == i:
                pass
            else:
                method = db.show_me_method(int(i))
                if method[2] != 'None':
                    await bot.answer_callback_query(call.id, text='Отправка молотого кофе возможна только при оплате картой', show_alert=True)
                    bool = False
                    break

        if bool == True:
            row = db.show_user(call.from_user.id)
            print(call.data)
            if row[2] == 'None':
                await state.update_data(payment=call.data)
                await bot.send_message(call.message.chat.id, text='Введите Ваш мобильный номер (В формате 063XXXXXXX):')
                await info_profile.phone.set()

            elif row[4] == 'None' and 'delivery' in call.data :
                await state.update_data(payment=call.data)
                await bot.send_message(call.message.chat.id, text='Введите Ваш мобильный номер (В формате 063XXXXXXX):')
                await info_profile.phone.set()

            elif row[3] == 'None' and 'nova' in call.data :
                await state.update_data(payment=call.data)
                await bot.send_message(call.message.chat.id, text='Введите Ваш мобильный номер (В формате 063XXXXXXX):')
                await info_profile.phone.set()

            elif 'pickup' in call.data and row[5] == 'None':
                await state.update_data(payment=call.data)
                await bot.send_message(call.message.chat.id, text='Введите Ваш мобильный номер (В формате 063XXXXXXX):')
                await info_profile.phone.set()


            else:
                zakaz = call.data.lower().split(':')[0]
                if zakaz == 'nova':
                    await send_admin_goods(card=False, what=call.data, poshta=True)

                if zakaz == 'pickup':
                    await send_admin_goods(card=False, what=call.data, pickup=True)

                if zakaz == 'delivery':
                    await send_admin_goods(card=False, what=call.data, delivery=True)

    elif ':card_yes' in call.data:
        # inline = logic.payment(call.data)
        # await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Оплата', reply_markup=inline)
        await bot.send_invoice(chat_id=call.from_user.id, title='Кофе', description='Кофе', payload=100, provider_token='', prices=types.LabeledPrice(label='sad', amount=1235), currency='UAH', start_parameter='')

    elif 'nova:' in call.data or 'pickup:' in call.data or 'delivery:' in call.data:
        text, inline = keyboard.card_or_not(call.data)
        await bot.send_message(call.message.chat.id, text=text, reply_markup=inline)





    elif 'delete_basket:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        db.delete_from_basket(int(n))
        inline = logic.show_basket(call.from_user.id)
        if len(inline.inline_keyboard) != 0:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=keyboard.you_have_basket, reply_markup=inline)
        else:
            button = keyboard.create_start_btn()
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(call.message.chat.id, text=keyboard.you_have_not_basket, reply_markup=button)

    elif 'plus_change:' in call.data or 'minus_change:' in call.data:
        for i in keyboard.number:
            if call.data == f'plus_change:{i}':
                number = call.message.reply_markup.inline_keyboard[1][0].callback_data
                number = number.lower().split(':')[-1]
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n)+1
                inline = keyboard.choose_quatyliti_change(number, n)
                row = db.show_weight(number)
                Weight = row[3]
                opt = logic.get_opt(Weight, n)
                text = keyboard.quantly_coffee + '\n' + opt
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=inline)

        for i in keyboard.number:
            if call.data == f'minus_change:{i}':
                number = call.message.reply_markup.inline_keyboard[1][0].callback_data
                number = number.lower().split(':')[-1]
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n) - 1
                inline = keyboard.choose_quatyliti_change(number, n)
                row = db.show_weight(number)
                Weight = row[3]
                opt = logic.get_opt(Weight, n)
                text = keyboard.quantly_coffee + '\n' + opt
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                            reply_markup=inline)

    elif call.data == 'back_zakaz':
        inline = logic.show_order(call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=keyboard.you_have_order, reply_markup=inline)

    elif call.data == 'watch_catalog':
        with open('static/photo_bot/first_photo.jpg', 'rb') as f1, open('static/photo_bot/second_photo.jpg',
                                                                        'rb') as f2, open(
            'static/photo_bot/the_three_photo.jpg', 'rb') as f3:
            await bot.send_media_group(call.from_user.id, media=[types.InputMediaPhoto(f1), types.InputMediaPhoto(f2),
                                                               types.InputMediaPhoto(f3)])
            inline = keyboard.our_price()
            await bot.send_message(call.from_user.id, text=keyboard.our_price_text, reply_markup=inline)

    elif call.data == 'to_order':
        user_data = await state.get_data()
        number = call.message.reply_markup.inline_keyboard[0][0].callback_data
        number = number.lower().split(':')[-1]
        Weight = user_data['Weight']
        method = user_data['method']
        grind = user_data['grind']
        id_coffe = user_data['id_coffe']
        basket = user_data['basket']
        comment = user_data['comment']
        prom = user_data['prom']
        order = 'False'
        profile = db.show_user(call.from_user.id)
        if profile[7] == prom:
            prom = 'None'
        else:
            db.update_promo(prom, call.from_user.id)

        all_price = logic.get_all_price(Weight, int(number),
                                        id_coffe, prom)
        n = db.add_order(call.from_user.id, grind, method, Weight, number, order, all_price, id_coffe, basket, comment, prom)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        if basket == 'True':
            button = keyboard.create_start_btn()
            await bot.send_message(call.message.chat.id, text=keyboard.add_basket, reply_markup=button)
        else:
            button = keyboard.create_start_btn()
            inline, text = logic.inline_payment(id_order=n, id_user=call.from_user.id)
            await bot.send_message(call.message.chat.id, text=keyboard.wait_payment, reply_markup=button)
            await bot.send_message(call.message.chat.id, text=text, reply_markup=inline)
        await state.finish()

    elif 'plus_delivery' in call.data or 'minus_delivery' in call.data:
        for i in keyboard.number:
            if call.data == f'plus_delivery:{i}':
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n)+1
                inline = keyboard.estimate_delivery(n)
                await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=inline)

        for i in keyboard.number:
            if call.data == f'minus_delivery:{i}':
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n) - 1
                inline = keyboard.estimate_delivery(n)
                await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                    reply_markup=inline)

    elif 'plus_product' in call.data or 'minus_producty' in call.data:
        for i in keyboard.number:
            if call.data == f'plus_product:{i}':
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n)+1
                inline = keyboard.estimate_product(n)
                await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=inline)

        for i in keyboard.number:
            if call.data == f'minus_producty:{i}':
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n) - 1
                inline = keyboard.estimate_product(n)
                await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                    reply_markup=inline)

    elif 'plus_bot' in call.data or 'minus_bot' in call.data:
        for i in keyboard.number:
            if call.data == f'plus_bot:{i}':
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n)+1
                inline = keyboard.estimate_bot(n)
                await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=inline)

        for i in keyboard.number:
            if call.data == f'minus_bot:{i}':
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n) - 1
                inline = keyboard.estimate_bot(n)
                await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                    reply_markup=inline)

    elif 'plus' in call.data or 'minus' in call.data:
        for i in keyboard.number:
            if call.data == f'plus:{i}':
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n)+1
                inline = keyboard.choose_quatyliti(n)
                user_data = await state.get_data()
                Weight = user_data['Weight']
                opt = logic.get_opt(Weight, n)
                text = keyboard.quantly_coffee+'\n'+opt
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=inline)

        for i in keyboard.number:
            if call.data == f'minus:{i}':
                n = call.data
                n = n.lower().split(':')[-1]
                n = int(n) - 1
                inline = keyboard.choose_quatyliti(n)
                user_data = await state.get_data()
                Weight = user_data['Weight']
                opt = logic.get_opt(Weight, n)
                text = keyboard.quantly_coffee + '\n' + opt
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                            reply_markup=inline)

    elif 'buy:' in call.data or 'basket:' in call.data:
        c_choose = db.show_all_goods()
        for i in c_choose:
            if call.data == f'buy:{i[6]}':
                await state.update_data(id_coffe=i[6])
                button = keyboard.btn_Grind()
                await state.update_data(basket='False')
                await bot.send_message(call.from_user.id, text=keyboard.choose, reply_markup=button)
                await buy_coffee.grind.set()

            elif call.data == f'basket:{i[6]}':
                await state.update_data(id_coffe=i[6])
                button = keyboard.btn_Grind()
                await state.update_data(basket='True')
                await bot.send_message(call.from_user.id, text=keyboard.choose, reply_markup=button)
                await buy_coffee.grind.set()

    elif 'id_order:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        row = db.show_my_order(int(n))
        text, inline = logic.create_order(row)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=inline)

    elif 'id_baskeet:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        row = db.show_my_order(int(n))
        text, inline = logic.create_basket(row)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=inline)
    elif 'grind_or_not:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        await state.update_data(id_coffee = n)
        button = keyboard.btn_Grind()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id, text=keyboard.choose, reply_markup=button)
        await buy_coffee_change.grind_change.set()

    elif 'method_change:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        await state.update_data(id_coffee = n)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id, text=keyboard.write_method)
        await buy_coffee_change.method_change.set()

    elif 'weight_change:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        await state.update_data(id_coffee = n)
        button = keyboard.btn_weight()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id, text=keyboard.choose, reply_markup=button)
        await buy_coffee_change.Weight_change.set()

    elif 'quatili_change:' in call.data:
        print(1)
        n = call.data
        n = n.lower().split(':')[-1]
        inline = keyboard.choose_quatyliti_change(int(n), 1)
        row = db.show_weight(int(n))
        Weight = row[3]
        opt = logic.get_opt(Weight, 1)
        text = keyboard.quantly_coffee + '\n' + opt
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id, text=text, reply_markup=inline)

    elif 'comment_change:' in call.data:
        n = call.data
        n = n.lower().split(':')[-1]
        await state.update_data(id_coffee=n)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id, text=keyboard.text_coments)
        await buy_coffee_change.comment_change.set()

    elif 'to_order_change' in call.data:
        number = call.message.reply_markup.inline_keyboard[0][0].callback_data

        number = number.lower().split(':')[-1]
        n = call.data
        n = n.lower().split(':')[-1]
        db.updateQuantili(number, n)
        logic.get_all_price_change(n)
        row = db.show_my_order(n)
        text, inline = logic.create_basket(row)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                               reply_markup=inline)




@dp.message_handler(content_types=['contact'])
async def contact_send(messahe: types.Message):
        await bot.send_message(messahe.chat.id, text=keyboard.thank_Application)
        for i in config.admins:
            txt = 'Оптовые продажи\n' \
                  f'Username: @{messahe.from_user.username}\n' \
                  f'ID: {messahe.from_user.id}\n' \
                  f'Номер: {messahe.contact.phone_number}' \

            await bot.send_message(i, text=txt)


@dp.inline_handler(lambda inline_query: inline_query.query == 'Filter Roast')
async def filter_roast_inline(inline_query: InlineQuery, state: FSMContext):
        info = db.show_goods('Filter Roast')
        data = []

        for product in info:
            add_buttons_f = keyboard.buy_coffee(product[6])
            data.append(InlineQueryResultArticle(id=hashlib.md5(product[0].encode()).hexdigest(),
                                                              title=product[0], description='● 250 gr ' + str(product[2]) + 'UAH' + "\n● 1 kg " + str(product[3]) + "UAH", reply_markup=add_buttons_f,
                                                              input_message_content=InputTextMessageContent(parse_mode='HTML',
                                                                                                            message_text=product[1] +
                                                                                                            '\n\n<a href="{0}">Фото</a>'.format(product[4])),
                                                              thumb_url=product[4], thumb_height=48, thumb_width=48))

        await bot.answer_inline_query(inline_query.id, results=data, cache_time=1)

        await state.finish()

async def send_three_week():
    while True:
        row = db.show_data()
        seting = db.show_tablese(1)
        inline = keyboard.estimate_delivery(1)
        for i in row:
            now = datetime.datetime.now()
            now_date = now.strftime("%Y-%m-%d")
            not_now_date = i[6]
            y = not_now_date.split('-')[0]
            m = not_now_date.split('-')[1]
            d = not_now_date.split('-')[2]
            y_ = now_date.split('-')[0]
            m_ = now_date.split('-')[1]
            d_ = now_date.split('-')[2]
            now = date(int(y), int(m), int(d))
            not_now_date = date(int(y_), int(m_), int(d_))
            rd = rdelta.relativedelta(now, not_now_date)
            if rd.days == 7:
                await bot.send_message(i[0], text=keyboard.text_week_three, reply_markup=inline)

            if rd.days == seting[2] and seting[1] == 'True':
                await bot.send_message(i[0], text=keyboard.text_week_three)

        await sleep(86400)

async def mailing_profile(message):
    row = db.show_all_profile()
    for i in row:
        await bot.send_message(i[0], text=message)

    for admin in config.admins:
        await bot.send_message(admin, text='Рассылка завершенна')


async def send_promo_all_user():
    row = db.show_tablese(1)
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")
    y_ = now_date.split('-')[0]
    m_ = now_date.split('-')[1]
    d_ = now_date.split('-')[2]
    now_date = date(int(y_), int(m_), int(d_))
    r = now_date + + datetime.timedelta(days=row[4])
    show_all_user = db.show_all_profile()
    text = f'Вам достуана скидка в {row[6]}%\n' \
           f'По промокоду {row[3]}\n' \
           f'Промокод активен к {r}'
    for _ in show_all_user:
        await bot.send_message(_[0], text=text)

if __name__ == '__main__':
    db = database.DBConnection()
    db.create_tables()
    row = db.show_tablese(1)
    if row == None:
        db.add_tables(1, 'True', 21, 'None', 0, 'None', 0)
    executor.start_polling(dp)
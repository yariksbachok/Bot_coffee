import database
import keyboard
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

db = database.DBConnection()

for_way = {1: 'nova', 2:'pickup', 3:'delivery'}

def get_all_price(weight, n, id, promo):
    price = db.show_price_coffe(id)
    if weight == '☕️ 250 g':
        price = price[2]
    else:
        price = price[3]
    all = int(price)*n

    if promo != 'None':
        setting = db.show_tablese(1)
        if promo == setting[3]:
            text = '0.'
            b = setting[6]
            n = text + str(b)
            b = float(n)
            all = round(all * b, 0)

    return all

def get_opt(weight, n):
    int_weight = ''
    number = 0
    for i in weight:
        if i.isdigit():
            int_weight += i
            number+=1
    if number == 1:
        int_weight = int_weight+'000'

    all = n * int(int_weight)
    text_opt = ''
    if all < 2000:
        new_all = 2000 - all
        if new_all == 1000 and int(int_weight) != 250:
            text_opt = 'Возьмите еще один и цена будет оптовая'

        else:
            number = 0
            for i in range(10):
                all+=250
                number += 1
                if all >= 2000:
                    text_opt = f'Возьмите еще {number} и цена будет оптовая'
                    break
    else:
        text_opt = 'У вас цена оптовая'


    return text_opt

def get_all_price_change(id_order):
    weight = db.show_weight(id_order)
    price = db.show_price_coffe(weight[7])
    Quantity = weight[4]
    if weight[3] == '☕️ 250 g':
        price = price[2]
    else:
        price = price[3]
    print(price, Quantity, weight[7])
    all = int(price) * int(Quantity)
    print(all)
    db.updateprice_in_order(all, id_order)

def show_order(id_user):
    inline = InlineKeyboardMarkup()
    row = db.show_order(id_user)
    for _ in row:
        row_goods = db.show_order_one(_[7])
        inline.add(InlineKeyboardButton(text=str(row_goods[0]), callback_data=f'id_order:{_[8]}'))
    return inline


def create_order(row):
    inline = InlineKeyboardMarkup()
    goods = db.show_price_coffe(row[7])
    if row[5] == 'False':
        inline.add(InlineKeyboardButton(text='Выбрать способ оплаты', callback_data=f'orderr:{row[8]}'))
    text=f'<b>Заказ #{row[8]}</b>\n' \
         '<b>Товары:</b>\n' \
         f'{goods[0]} | {row[4]} упак.- {row[3]}({row[6]} UAH {row[1]}'
    if row[2] != 'None':
        text+=f'Метод: {row[2]}'

    text+=f'\nКоментарий: {row[10]}\n'

    setting = db.show_tablese(1)
    if row[11] == setting[3]:
        text += f'У вас активирован промокод, скидкой у {setting[6]}\n'
    else:
        text += 'У вас не активирован промокод или он не активной\n'
    text += f'<b>Итого: {row[6]} UAH</b>'

    inline.add(InlineKeyboardButton(text='Назад', callback_data='back_zakaz'))

    return text, inline

def show_basket(id_user):
    inline = InlineKeyboardMarkup()
    row = db.show_basket(id_user)
    for _ in row:
        row_goods = db.show_order_one(_[7])
        inline.add(InlineKeyboardButton(text=str(row_goods[0]), callback_data=f'id_baskeet:{_[8]}'))
    inline.add(InlineKeyboardButton(text='Выбрать способ оплаты', callback_data=f'order_from_basket:{id_user}'))

    return inline

def create_basket(row):
    inline = InlineKeyboardMarkup(row_width=1)
    goods = db.show_price_coffe(row[7])
    opt = get_opt(row[3], int(row[4]))
    inline.add(InlineKeyboardButton(text='Изменить заказ', callback_data=f'change_basket:{row[8]}'))
    inline.add(InlineKeyboardButton(text='Удалить с корзины', callback_data=f'delete_basket:{row[8]}'))
    inline.add(InlineKeyboardButton(text='Назад', callback_data='back_basket'))
    text=f'<b>Заказ #{row[8]}</b>\n' \
         '<b>Товары:</b>\n' \
         f'{goods[0]} | {row[4]} упак.- {row[3]}({row[6]} UAH {row[1]}'
    if row[2] != 'None':
        text+=f'Метод: {row[2]}'
    text+=f'\n<b>Коментарий:</b>{row[10]}\n' + opt +'\n'

    setting = db.show_tablese(1)
    if row[11] == setting[3]:
        text += f'У вас активирован промокод, скидкой у {setting[6]}\n'
    else:
        text+='У вас не активирован промокод или он не активной\n'
    text+=f'<b>Итого: {row[6]} UAH</b>'
    return text, inline





def inline_payment(id_user, id_order=None, all = None):
    inline = InlineKeyboardMarkup()
    if all != None:
        nova = 'nova:'
        pickup = 'pickup:'
        delivery = 'delivery:'
        last = all[-1]
        for i in all:
            if i == last:
                nova += str(i[8])
                pickup += str(i[8])
                delivery += str(i[8])
            else:
                nova+=str(i[8])+':'
                pickup+=str(i[8])+':'
                delivery+=str(i[8])+':'

        inline.add(
            InlineKeyboardButton(text='Новая почта(от 2 кг - бесплатная доставка)', callback_data=nova))
        inline.add(
            InlineKeyboardButton(text='Самовывоз (Киев, Плодовая 1(район Берковец))', callback_data=pickup))
        inline.add(InlineKeyboardButton(text='Доставка по Киеву 50грн(от 1 кг - бесплатная)',
                                        callback_data=delivery))
    else:
        inline.add(
            InlineKeyboardButton(text='Новая почта(от 2 кг - бесплатная доставка)', callback_data=f'nova:{id_order}'))
        inline.add(
            InlineKeyboardButton(text='Самовывоз (Киев, Плодовая 1(район Берковец))', callback_data=f'pickup:{id_order}'))
        inline.add(InlineKeyboardButton(text='Доставка по Киеву 50грн(от 1 кг - бесплатная)',
                                        callback_data=f'delivery:{id_order}'))
    row = db.show_user(id_user)
    text = ''
    if row[2] != 'None':
        text = 'Выберите способ оплаты:\n\n' \
                'Ваши данные:\n' \
                f'<b>Ваш мобильный номер:</b> {row[1]}\n' \
                f'<b>ФИО:</b> {row[2]}\n' \
                f'<b>Город:</b> {row[5]}\n'

        if row[3] != 'None':
            text += f'<b>Отделение Новой почты:</b> {row[3]}\n'

        if row[4] != 'None':
            text += f'<b>Адрес для доставки по Киеву</b> {row[4]}'
        inline.add(InlineKeyboardButton(text='Сбросить данные', callback_data=f'delete_profile:{id_order}'))
    else:
        text = 'Выберите способ оплаты:'


    return inline, text

def payment(pay):
    n = pay.lower().split(':')[1]
    price = db.show_weight(n)
    price = price[6]
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=f'Оплатить {price} UAH', callback_data='PAYB-Card'))

    return inline


def admin_panel():
    inline = InlineKeyboardMarkup()
    seting = db.show_tablese(1)
    text = ''
    if seting[1] == 'True':
        inline.add(InlineKeyboardButton(text='Выкл Упоминания', callback_data='off_notifical'))
        text = 'Упоминания: Вкл\n'
    else:
        inline.add(InlineKeyboardButton(text='Вкл Упоминания', callback_data='on_notifical'))
        text = 'Упоминания: Выкл\n'
    inline.add(InlineKeyboardButton(text='Указать интервал', callback_data='interval'))
    inline.add(InlineKeyboardButton(text='Запустить рассылку', callback_data='mailing'))
    inline.add(InlineKeyboardButton(text='Задать промокод', callback_data='create_promo'))
    text += f'Интервал: {seting[2]} дней'

    return inline, text
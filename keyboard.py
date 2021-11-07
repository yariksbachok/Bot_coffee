from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton




start_button = ['🤟 Магазин', '🛒 Корзина', '📦 Заказы', '📌 Блог', '🔺 Настройки', '📲 Контакты', '📘 Информация о кофе', '🤝 Оптовые продажи']

Application_button = ['Оставить заявку', '🏠 В меню']

text_start = 'Привет 🤜 я твой личный бот 3 champs roastery 🤟 благодаря мне ты можешь легко и быстро приобрести и оплатить кофе.' \
             'Если у тебя возникли сложности, смело набирай или пиши Паше +38 093 106 3569, он оперативно ответит на возникшие вопросы 😎' \
             'пс: от 1кг у нас действует бесплатная доставка по Киеву и Украине, а в сумме от 2 кг (любого ассортимента) ты можешь приобрести' \
             ' кофе по оптовой цене 😉 не пугайся, когда в корзине будет больше 2кг, но ты увидишь розничные цены: при оплате сумма снимается со ' \
             'скидкой, не бойтесь переходить к оплате 😏 мы очень стараемся решить данный вопрос 🙂'


setting_text = 'Выберите язык'

thank_Application = 'Спасибо, Ваш запрос оставлен'

Application_eror = 'У вас нет номера'

call_me_text = '🙌 Павло Спіцин\n' \
          'Менеджер з роздрібних продажів\n' \
          '+380931063569\n\n' \
          '🤝 Антон Дихніч\n' \
          'Менеджер з оптових продажів\n+380933330595\n\n' \
          '🔥 Олексій Федоровський\n' \
          'Головний обсмажчик\n' \
          '+380956935358\n\n' \
          '🚘 Влад Скарбенчук\n' \
          'Головний по логістиці\n' \
          '+380507646444'


call_me_text_btn = 'Перезвоните мне'


info_of_kofe = 'Прежде чем знакомиться с нашим кофе, дадим тебе подсказку как выбрать кофе под твой метод заваривания.\n\\n' \
               'Эспрессо обжарка подойдет для приготовления в эспрессо машине, гейзерной кофеварке/моке.' \
               'Фильтр обжарка подойдет для фильтр кофемашины, френч-пресса, V60, кемекса, калиты, клевера, аэропресса и других альтернативных способов.\n\n' \
               'Для приготовления в турке/джезве и для заваривания в чашке подойдут оба варианта. Эспрессо обжарка будет более насыщенной и сладкой в этих способах, фильтр обжарка более деликатная и немного кислотней. Рекомендуем поэкспериментировать и выбрать для себя подходящий вариант по вкусовым предпочтениям\n\n' \
               'P.S Все вкусовые описания, которые вы найдете ниже являются субъективным сенсорным опытом нашей команды. \n\n' \
               '🇧🇷Бразилия 2 - старший брат Бразилии 1, кофе который отлично сочетается с молоком. Фруктово - карамельная чашка, с послевкусием молочного шоколада, сбалансированная и сладкая. \n' \
               'Рекомендуем для любителей классического кофейного вкусового профиля. \n\n' \
               '🇪🇹Эфиопия 6 - бум, супер класический профиль Эфиопии, яркая кислотность, цветочный профиль вкуса, чайное тело. Невероятный и захватывающий аромат. \nРекомендуем!\n\n' \
               '🇵🇪Перу 1 - новый кофейный регион в нашем ассортименте. Удивит тебя высокой сладостью и плотным телом. Наш фаворит в сочетании с молоком.\n\n' \
               '🇨🇴Колумбия 5 – первая Колумбия свежего урожая 2021 года в нашем ассортименте.\n' \
               'В фильтре похожа на фруктовый компот из зелёного яблока и нектарина.\n' \
               'В эспрессо - сбалансированный вкус и округлое тело.\nИдеальный выбор кофе на каждый день.\n\n' \
               '🇮🇩Индонезия 1 – новый кофейный регион в нашем ассортименте. Вкусная в фильтре и необычная в эспрессо. Имеет очень плотное тело, кислотность - выше среднего.В чашке ярко выражены цитрусы и красная смородина, на послевкусии можно ощутить нотки песочного печенья.Рекомендуем попробовать тем, кто любит эксперименты.\n\n' \
               '🇳🇮Никарагуа 5 – сочный кофе из Никарагуа в нашем ассортименте, который напоминает летний фруктовый салат.Это первый и очень удачный опыт Соломона Мендеза (владельца фермы) в применении натуральной обработки. Сладкая и очень вкусная, как в фильтре, так и в эспрессо.\n\n' \

Application_text = 'Оставьте номер для связи с менеджером'

get_contact = 'Укажите Ваше имя и номер телефона'

back_menu_text = 'Возвращение в главное меню...'

eror_input = 'Некоррекный номер. Пожалуйста, повторите попытку.'

our_price_text = 'Наш актуальний прайс'

btn_buy_coffee = 'Купить'

btn_in_basket = 'В корзину'

watch_catalog = 'Смотреть каталог'

choose = 'Выбрать'

Grind = 'Смолоть'

not_Grind = 'Не смалывать'


first_weight = '☕️ 250 g'

second_weight = '☕️ 1 kg'

chose_weight = 'Выберите вес'

write_method = 'Напишите, каким методом Вы готовите кофе?'

quantly_coffee = 'Выберете кол-во упаковок'

number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

wait_payment = 'Заказ сформирован. Ожидается оплата.'

add_basket = 'Додано в корзину'

you_have_not_order = 'У вас нет заказов'

you_have_order = 'Ваши заказы:'

you_have_not_basket = 'У вас нет товар в корзине'

you_have_basket = 'Ваша корзина:'

text_coments = 'Уведите коментарий к товару\n' \
               'Если у вас нет коментария уведите "-"'

text_week_three = '3 недели прошло купи'

def create_start_btn():
    button = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    n = 0
    for i in start_button:
        n += 1
        if i == start_button[-2]:
            button.add(KeyboardButton(text=i))

        elif i == start_button[-1]:
            button.add(KeyboardButton(text=i))

        elif n == 1:
            one = KeyboardButton(text=i)

        elif n == 2:
            button.row(
                one, KeyboardButton(text=i)
            )
            n = 0
    return button



def btn_blog():
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='Перейти', url='https://t.me/champsblog'))
    return inline



def setting_lang():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton('🇷🇺 Русский'), KeyboardButton(text='🇺🇦 Українська'))
    return button


def call_me():
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=call_me_text_btn, callback_data='call_me'))
    return inline



def send_Application():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(text=Application_button[0], request_contact=True))
    button.add(KeyboardButton(text=Application_button[1]))
    return button


def our_price():
    inline = InlineKeyboardMarkup(row_width=1)
    inline.add(InlineKeyboardButton(text='Filler Roast', switch_inline_query_current_chat='Filter Roast'),
               InlineKeyboardButton(text='Exspresso Roast', switch_inline_query_current_chat='Espresso Roast'),
               InlineKeyboardButton(text='Legendary coffee', switch_inline_query_current_chat='Legendary coffee'),
               InlineKeyboardButton(text='Cofee shop', switch_inline_query_current_chat='Coffee shop'))
    return inline



def buy_coffee(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=btn_buy_coffee, callback_data=f'buy:{id}'),
               InlineKeyboardButton(text=btn_in_basket, callback_data=f'basket:{id}'))
    inline.add(InlineKeyboardButton(text=watch_catalog, callback_data='watch_catalog'))
    return inline


def btn_Grind():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(text=Grind),
               KeyboardButton(text=not_Grind))
    return button

def btn_weight():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(text=first_weight),
               KeyboardButton(text=second_weight))
    return button

def choose_quatyliti(n):
    if n > 20:
        n = 20
    if n == 0:
        n = 1

    inline = InlineKeyboardMarkup()
    inline.add(
        InlineKeyboardButton(text='➖', callback_data=f'minus:{n}'),
        InlineKeyboardButton(text=str(n)+'/20', callback_data='#'),
        InlineKeyboardButton(text='➕', callback_data=f'plus:{n}')
    )
    inline.add(InlineKeyboardButton(text='Заказать', callback_data='to_order'))
    return inline

def inline_basket(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='Изменить заказ', callback_data=f'change_basket:{id}'),
               InlineKeyboardButton(text='Удалить с корзины', callback_data=f'delete_basket:{id}'),
               InlineKeyboardButton(text='Назад', callback_data='back_basket'))

def chenge_order(id):
    inline = InlineKeyboardMarkup(row_width=1)
    inline.add(InlineKeyboardButton(text='Молоть или не молоть', callback_data=f'grind_or_not:{id}'))
    inline.add(InlineKeyboardButton(text='Каким методом вы готовите кофе', callback_data=f'method_change:{id}'))
    inline.add(InlineKeyboardButton(text='Изменить вес', callback_data=f'weight_change:{id}'))
    inline.add(InlineKeyboardButton(text='Изменить количество', callback_data=f'quatili_change:{id}'))
    inline.add(InlineKeyboardButton(text='Изменить коментарий', callback_data=f'comment_change:{id}'))
    inline.add(InlineKeyboardButton(text='Назад', callback_data=f'id_baskeet:{id}'))

    return inline


def choose_quatyliti_change(id, n):
    if n > 20:
        n = 20
    if n == 0:
        n=1

    inline = InlineKeyboardMarkup()
    inline.add(
        InlineKeyboardButton(text='➖', callback_data=f'minus_change:{n}'),
        InlineKeyboardButton(text=str(n)+'/20', callback_data='#'),
        InlineKeyboardButton(text='➕', callback_data=f'plus_change:{n}')
    )
    inline.add(InlineKeyboardButton(text='Изменить', callback_data=f'to_order_change:{id}'))
    return inline

def card_or_not(callback):
    inline = InlineKeyboardMarkup()
    call_card_not = callback+':card_not'
    call_card_yes = callback+':card_yes'
    text = 'Выберите метод оплаты'
    inline.add(InlineKeyboardButton(text='Наложный платеж', callback_data=call_card_not))
    inline.add(InlineKeyboardButton(text='Картой', callback_data=call_card_yes))

    return text, inline


def estimate_delivery(n):
    if n > 5:
        n = 5
    if n < 0:
        n = 0

    inline = InlineKeyboardMarkup()
    inline.add(
        InlineKeyboardButton(text='➖', callback_data=f'minus_delivery:{n}'),
        InlineKeyboardButton(text=str(n)+'/5', callback_data='#'),
        InlineKeyboardButton(text='➕', callback_data=f'plus_delivery:{n}')
    )
    inline.add(InlineKeyboardButton(text='Оценить', callback_data='estimate_delivery'))

    return inline


def estimate_product(n):
    if n > 5:
        n = 5
    if n < 0:
        n = 0

    inline = InlineKeyboardMarkup()
    inline.add(
        InlineKeyboardButton(text='➖', callback_data=f'minus_producty:{n}'),
        InlineKeyboardButton(text=str(n)+'/5', callback_data='#'),
        InlineKeyboardButton(text='➕', callback_data=f'plus_product:{n}')
    )
    inline.add(InlineKeyboardButton(text='Оценить', callback_data='estimate_product'))

    return inline

def estimate_bot(n):
    if n > 5:
        n = 5
    if n < 0:
        n = 0

    inline = InlineKeyboardMarkup()
    inline.add(
        InlineKeyboardButton(text='➖', callback_data=f'minus_bot:{n}'),
        InlineKeyboardButton(text=str(n)+'/5', callback_data='#'),
        InlineKeyboardButton(text='➕', callback_data=f'plus_bot:{n}')
    )
    inline.add(InlineKeyboardButton(text='Оценить', callback_data='estimate_bot'))

    return inline

def cancel_create_promo():
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='Отменить', callback_data='cancel_create_promo'))

    return inline

def first_msg():
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='Админ на связи', callback_data='admin_yes'))

    return inline
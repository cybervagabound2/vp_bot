from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb
from bot.models import Users
from django.template import loader


def personal_area(bot, update):
    if update.callback_query:
        user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    else:
        user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params = '/PersonalArea'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/personal_area.html').render(context)
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('📢 Мои объявления'), callback_data='PA_my_ads'),
         ikb(user.GetButtons('✉️ Обратная связь'), callback_data='PA_feedback')],
        [ikb(user.GetButtons('💵 Поддержать проект'), callback_data='PA_support')]
    ])
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


def my_ads(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Ads'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/my_ads.html').render(context)
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('📝 Создать объявление'), callback_data='PA_create_ad')],
        [ikb(user.GetButtons('📠 Редактировать объявления'), callback_data='PA_edit_ad')],
        [ikb(user.GetButtons('🗑 Удалить объявление'), callback_data='PA_delete_ad')],
        [ikb(user.GetButtons('«'), callback_data='back_inline')]
    ])
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)












# [ikb(user.GetButtons('📝 Создать объявление'), callback_data='PA_create_ad'),
"""
Авто/мото
Активный отдых
Безопасность
Бизнес и финансы
Дизайн и графика
Домашние животные
Дом и семья
Другое
Женская тематика
Знакомства и общение
Игры
Технологии
Криптовалюты
Каталоги
Кино
Красота и мода
Лайфхак
Литература
Мобильная связь и интернет
Мужская тематика
Музыка
Мотивация/Саморазвитие
Новости и СМИ
Образование
Обустройство и ремонт
Политика
Продукты питания
Промышленность
Психиология
Путешествия
Работа
Развлечения
Спорт
Товары и услуги
Увлечения и хобби
Фото
Цитаты
Эзотерика
Эротика
Юмор
Gif
"""

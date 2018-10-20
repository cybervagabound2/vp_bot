from bot.models import Users, Lang as Language
from telegram.update import Message as MSG
from django.template import loader
from telegram import ReplyKeyboardMarkup


Lang = {'🇷🇺 Русский': 'Rus',
        '🇺🇸 English': 'Eng',
        "🇺🇿 O'zbek": "Uzb"}


def MainMenu(bot, update):
    if update.callback_query:
        user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    elif update.message.text:
        user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params = ''
    context = {'Lang': user.lang}
    user.save()
    msg = loader.get_template('bot/HomeMenu.html').render(context)
    keyboard = ReplyKeyboardMarkup([[user.GetButtons('🗂 Список ВП'), user.GetButtons('💻 Личный кабинет')]], resize_keyboard=True)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard)

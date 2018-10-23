from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb, ReplyKeyboardMarkup
from django.template import loader
from bot.models import Users, MutualPRCategory, Ad


def mutual_menu(bot, update):
    if update.message:
        user = Users.objects.get(telegram_id=update.message.chat.id)
    elif update.callback_query:
        user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params = '/Mutual'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/Mutual_PR/mutual_menu.html').render(context)
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('Instagram'), callback_data='MP_instagram'),
         ikb(user.GetButtons('Telegram'), callback_data='MP_telegram')]
    ])
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)
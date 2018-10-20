from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb
from django.template import loader
from bot.models import Users


def support(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Support'
    user.save()
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('🤖 Проголосовать в StoreBot'), url='https://google.com')],
        [ikb(user.GetButtons('«'), callback_data='back_inline')]
    ])
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/SupportProject/support.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)

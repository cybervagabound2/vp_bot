from bot.models import Users
from django.template import loader
from telegram import ReplyKeyboardMarkup
from bot.handlers.MainMenu import MainMenu


Lang = {'🇷🇺 Русский': 'Rus',
        '🇺🇸 English': 'Eng',
        "🇺🇿 O'zbek": "Uzb"}


def Send(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params += '/Rules'
    context = {'Lang': user.lang}
    user.save()
    msg = loader.get_template('bot/Rules/rules.html').render(context)
    lang = ReplyKeyboardMarkup([[user.GetButtons('✅ Полностью согласен'), user.GetButtons('❌ Не согласен')]], resize_keyboard=True)
    user.SendMessage(bot=bot, msg=msg, keyboard=lang)


def Result(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    if user.GetButtons('✅ Полностью согласен') == update.message.text:
        user.params = ''
        user.rules = True
        user.save()
        context = {'Lang': user.lang,
                   'User': user}
        msg = loader.get_template('bot/Rules/Result.html').render(context)
        user.SendMessage(bot=bot, msg=msg)
        MainMenu(bot, update)
    else:
        return
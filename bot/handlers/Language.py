from bot.models import Users, Lang as Language
from django.template import loader
from telegram import ReplyKeyboardMarkup
from bot.handlers import Rules
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

Lang = {'🇷🇺 Русский': 'Rus',
        '🇺🇸 English': 'Eng',
        "🇺🇿 O'zbek": "Uzb"}


def Send(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params += '/SelectLang'
    user.save()
    msg = loader.get_template('bot/Language/language.html').render()
    lang = ReplyKeyboardMarkup([['🇷🇺 Русский', '🇺🇸 English']],
                               resize_keyboard=True)
    user.SendMessage(bot=bot, msg=msg, keyboard=lang)


def SelectLang(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)

    lang = Language.objects.all()

    try:
        lang = lang.get(lang=Lang[update.message.text])
    except:
        lang = ReplyKeyboardMarkup([['🇷🇺 Русский', '🇺🇸 English']],
                                   resize_keyboard=True)
        msg = loader.get_template('bot/Language/language.html').render()
        user.SendMessage(bot=bot, msg=msg, keyboard=lang)
        return
    user.lang = lang
    user.save()
    if user.params == '/Start/SelectLang':
        Rules.Send(bot, update)
    elif user.params.endswith('SelectLang'):
        user.DelEndParams()


def error(bot, error, update):
    logger.warning('Update "%s" caused error "%s"', update, error)

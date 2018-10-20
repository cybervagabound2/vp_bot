from bot.models import Users
from django.template import loader
from telegram import ReplyKeyboardMarkup
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    if update.message.chat.type == 'private':
        user = add_user(update)
        if user is not None:
            user.params = '/Start/SelectLang'
            user.save()
            msg = loader.get_template('bot/language.html').render()
            lang = ReplyKeyboardMarkup([['🇷🇺 Русский', '🇺🇸 English'],
                                        ["🇺🇿 O'zbek"]], resize_keyboard=True)
            update.message.reply_text(msg, parse_mode='HTML', disable_web_page_preview=True, reply_markup=lang)
        else:
            msg = loader.get_template('bot/Banned.html').render()
            update.message.reply_text(msg)


def add_user(update):
    user = Users.objects.filter(telegram_id=update.message.chat.id)
    if user.count() is 0:
        invated = update.message.text.split(' ')
        if len(invated) > 1 and invated[1] != str(update.message.from_user.id):
            invated_user = Users.objects.filter(telegram_id=invated[1])
            if invated_user.count() != 0:
                invated_user = invated_user.get(telegram_id=invated[1])
                user = Users(telegram_id=update.message.chat.id, username=update.message.chat.username,
                             first_name=update.message.chat.first_name, last_name=update.message.chat.last_name,
                             invited_by=invated_user.id)
                user.save()
                return
        user = Users(telegram_id=update.message.chat.id, username=update.message.chat.username,
                     first_name=update.message.chat.first_name, last_name=update.message.chat.last_name)
        user.save()
    else:
        user = user.get(telegram_id=update.message.chat.id)
        if not user.banned:
            user.first_name = update.message.chat.first_name
            user.last_name = update.message.chat.last_name
            user.params = '[]'
            user.rules = False
            user.blocked = False
            user.save()
        else:
            return None
    return user


def error(bot, error, update):
    logger.warning('Update "%s" caused error "%s"', update, error)
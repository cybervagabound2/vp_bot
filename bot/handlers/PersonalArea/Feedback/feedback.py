from time import sleep
from functools import wraps
from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb, ReplyKeyboardMarkup
from django.template import loader
from bot.models import Users
from telegram import ChatAction
from bot.handlers.PersonalArea import personal_area
from bot.handlers import MainMenu


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            func(bot, update, **kwargs)

        return command_func

    return decorator


def feedback(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Feedback'
    user.save()
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('✉️ Написать сообщение'), callback_data='pa_feedback_create')],
        [ikb(user.GetButtons('«'), callback_data='back_inline')]
    ])
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/Feedback/feedback.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


@send_action(ChatAction.TYPING)
def write_message(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/WriteMessage'
    user.save()
    keyboard = ReplyKeyboardMarkup([['«']], resize_keyboard=True, one_time_keyboard=True)
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/Feedback/write_message.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


@send_action(ChatAction.TYPING)
def send_message(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/Feedback/send_message.html').render(context)
    info = 'Новое сообщение от: ' + '@' + update.message.from_user.username + '\n' \
           'id: ' + str(update.message.chat.id) + '\n'
    bot.send_message(chat_id='@cybervagabounds', text=str(info) + update.message.text)
    user.DelEndParams(3)
    user.SendMessage(bot=bot, msg=msg, save_massage_id=True)
    sleep(4)
    personal_area.personal_area(bot, update)

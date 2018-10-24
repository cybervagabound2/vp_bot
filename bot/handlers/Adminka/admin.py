from telegram import InlineKeyboardButton as ikb, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from bot.models import Ad, Users
from django.template import loader
from time import sleep
from bot.handlers.MainMenu import MainMenu

admin_list = [523792555]


def admin_menu(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    if user.telegram_id not in admin_list:
        user.SendMessage(bot=bot, msg='Poshel naxoy otsudova 🖕', save_massage_id=True)
        sleep(3)
        MainMenu(bot, update)
    else:
        user.params = '/Adminka'
        user.save()
        keyboard = InlineKeyboardMarkup([
            [ikb('Удалить объяление', callback_data='admin_delete_ad'),
             ikb('Рассылка', callback_data='admin_broadcast')],
            [ikb('Написать пользователю', callback_data='admin_send_msg'),
             ikb('Статистика', callback_data='admin_statistic')]
        ])
        user.SendMessage(bot=bot, msg='Админка', keyboard=keyboard, save_massage_id=True)


################
# Send message #
################
def send_msg_menu(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/SendMsg'
    user.save()
    user.SendMessage(bot=bot, msg='Укажите id пользователя для отправки сообщения')


def send_msg_text(bot, update, user_data):
    user_data['user_id'] = update.message.text
    user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params += '/Text'
    user.save()
    user.SendMessage(bot=bot, msg='Напишите текст сообщения:', save_massage_id=True)


def send_msg(bot, update, user_data):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    context = {'Lang': user.lang,
               'Text': update.message.text}
    msg = loader.get_template('bot/Adminka/send_msg.html').render(context)
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('Ответить'), callback_data='admin_msg_reply')]
    ])
    bot.send_message(chat_id=user_data['user_id'], text=msg, reply_markup=keyboard)
    user_data.clear()
    user.SendMessage(bot=bot, msg='Сообщение отправлено', save_massage_id=True)
    sleep(1)
    MainMenu(bot, update)


def reply_to_admin(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/ReplyToAdmin'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/Adminka/reply_to_admin.html').render(context)
    user.SendMessage(bot=bot, msg=msg, save_massage_id=True)


def send_reply_to_admin(bot, update):
    reply_text = update.message.text
    user = Users.objects.get(telegram_id=update.message.chat.id)
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/Adminka/send_reply_to_admin.html').render(context)
    user.DelEndParams()
    info = 'Новое ответное сообщение от: ' + '@' + update.message.from_user.username + '\n' \
           'id: ' + str(update.message.chat.id) + '\n'
    bot.send_message(chat_id='@cybervagabounds', text=str(info) + reply_text)
    sleep(1)
    user.SendMessage(bot=bot, msg=msg, save_massage_id=True)
    sleep(2)
    MainMenu(bot, update)


#############
# Delete ad #
#############
def delete_ad_menu(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/DeleteAd'
    user.save()
    user.SendMessage(bot=bot, msg='Укажите id объявления для удаления:')


def delete_ad_reason(bot, update, user_data):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params += '/Reason'
    user.save()
    user_data['ad_id'] = update.message.text
    user.SendMessage(bot=bot, msg='Укажите причину удаления объявления', save_massage_id=True)


def delete_ads(bot, update, user_data):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    ad = Ad.objects.get(id=user_data['ad_id'])
    context = {'Lang': user.lang,
               'Reason': update.message.text}
    msg = loader.get_template('bot/Adminka/delete_ad.html').render(context)
    creator_id = ad.creator.telegram_id
    ad.delete()
    bot.send_message(chat_id=creator_id, text=msg)
    sleep(1)
    user.SendMessage(bot=bot, msg='Объявление удалено')
    sleep(2)
    user_data.clear()
    MainMenu(bot, update)


#############
# Broadcast #
#############
def broadcast_menu(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Broadcast'
    user.save()
    keyboard = InlineKeyboardMarkup([
        [ikb('Rus', callback_data='broadcast_Rus'),
         ikb('Eng', callback_data='broadcast_Eng')],
        [ikb('Uzb', callback_data='broadcast_Uzb')]
    ])
    user.SendMessage(bot=bot, msg='Выберите локализацию для рассылки', keyboard=keyboard, save_massage_id=True)


def broadcast_text(bot, update, user_data):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Text'
    user.save()
    user_data['localization'] = update.callback_query.data[10:]
    user.SendMessage(bot=bot, msg='Напишите текст рассылки:', save_massage_id=True)


def broadcast(bot, update, user_data):
    text = update.message.text
    user = Users.objects.get(telegram_id=update.message.chat.id)
    lang = ''
    if user_data['localization'] == 'Eng':
        lang = 1
    elif user_data['localization'] == 'Rus':
        lang = 2
    else:
        lang = 3
    all = Users.objects.filter(lang=lang)
    bad = 0
    good = 0
    for usr in all:
        try:
            bot.send_message(chat_id=usr.telegram_id, text=text)
            good += 1
            sleep(0.1)
        except Exception as e:
            bad += 1
    user_data.clear()
    user.SendMessage(bot=bot, msg='Рассылка завершена\n\n'
                                  'Доставлено сообщений: ' + str(good) + '\n\n'
                                  'Не доставлено: ' + str(bad))
    MainMenu(bot, update)


#############
# Statistic #
#############
def statistic(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Statistic'
    users_all = Users.objects.all()
    usr = []
    for uzr in users_all:
        usr.append(uzr.id)
    user.SendMessage(bot=bot, msg='Всего пользователей: ' + str(len(usr)) + '\n\n'
                                  'Rus пользователей: ' + str(len(Users.objects.filter(lang=2))) + '\n\n'
                                  'Eng пользователей: ' + str(len(Users.objects.filter(lang=1))) + '\n\n'
                                  'Uzb пользователей: ' + str(len(Users.objects.filter(lang=3))))

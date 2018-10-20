import re
from time import sleep
from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb, ReplyKeyboardMarkup
from bot.models import Users, Ad, MutualPRCategory
from bot.handlers.helpers import build_menu
from django.template import loader


def delete_ad_menu(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Deleting'
    user.save()
    ads = Ad.objects.filter(creator=user)
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/DeleteAd/delete_ad_menu.html').render(context)
    button_list = []
    for ad in ads:
        if 'nstagram' in ad.channel_name:
            button_list.append(ikb('@' + ad.channel_name[22:] + ' 📸', callback_data='PA_delete_ad' + str(ad.id)))
        else:
            button_list.append(ikb('@' + ad.channel_name[13:] + ' 🚀', callback_data='PA_delete_ad' + str(ad.id)))
    button_list.append(ikb(user.GetButtons('«'), callback_data='back_inline'))
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(build_menu(button_list, n_cols=2)), save_massage_id=True)


def delete_ad_confirm(bot, update):
    query = update.callback_query
    user = Users.objects.get(telegram_id=query.from_user.id)
    ad = Ad.objects.get(id=query.data[12:])
    user.params += '/' + str(ad.id)
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('Да'), callback_data='pa_delete_ad_yes'),
         ikb(user.GetButtons('Нет'), callback_data='pa_delete_ad_no')]
    ])
    context = {'Lang': user.lang,
               'Ad': ad}
    msg = loader.get_template('bot/PersonalArea/DeleteAd/delete_ad_confirm.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


def delete_ad(bot, update):
    query = update.callback_query
    user = Users.objects.get(telegram_id=query.from_user.id)
    ad = Ad.objects.get(id=int(re.findall('Deleting/(\d+)', user.params)[0]))
    if query.data == 'pa_delete_ad_yes':
        ad.delete()
        context = {'Lang': user.lang}
        msg = loader.get_template('bot/PersonalArea/DeleteAd/delete_ad.html').render(context)
        user.DelEndParams(3)
        user.SendMessage(bot=bot, msg=msg, save_massage_id=True)
        sleep(2)
        delete_ad_menu(bot, update)
    else:
        user.DelEndParams(3)
        delete_ad_menu(bot, update)

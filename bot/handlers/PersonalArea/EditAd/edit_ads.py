from time import sleep
import re
from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb, ReplyKeyboardMarkup
from bot.models import Users, Ad, MutualPRCategory
from bot.handlers.helpers import build_menu
from django.template import loader


def edit_ads_menu(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    if user.params == '/PersonalArea/Ads':
        user.params += '/Editing'
    else:
        user.DelEndParams(3)
        user.params += '/Editing'
    user.save()
    ads = Ad.objects.filter(creator=user)
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/EditAd/edit_ads_menu.html').render(context)
    button_list = []
    for ad in ads:
        if 'nstagram' in ad.channel_name:
            button_list.append(ikb('@' + ad.channel_name[22:] + ' 📸', callback_data='PA_edit_ad' + str(ad.id)))
        else:
            button_list.append(ikb('@' + ad.channel_name[13:] + ' 🚀', callback_data='PA_edit_ad' + str(ad.id)))

    button_list.append(ikb(user.GetButtons('«'), callback_data='back_inline'))
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(build_menu(button_list, n_cols=2)), save_massage_id=True)


def edit(bot, update, user_data):
    if update.callback_query:
        query = update.callback_query
        user = Users.objects.get(telegram_id=query.from_user.id)
        if 'Subcategory' in user.params:
            ad = Ad.objects.get(id=user_data['ad_id'])
            user_data.clear()
            user.DelEndParams(2)
        else:
            ad = Ad.objects.get(id=query.data[10:])
    else:
        user = Users.objects.get(telegram_id=update.message.chat.id)
        ad = Ad.objects.get(id=user_data['ad_id'])
        user_data.clear()
    user.params += '/' + str(ad.id)
    user.save()
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('Подкатегорию'), callback_data='pa_edit_ad_subcategory'),
         ikb(user.GetButtons('Адрес канала'), callback_data='pa_edit_ad_channel_name')],
        [ikb(user.GetButtons('Мин. количество'), callback_data='pa_edit_ad_min_count'),
         ikb(user.GetButtons('Комментарий'), callback_data='pa_edit_ad_comment')],
        [ikb(user.GetButtons('Отменить'), callback_data='pa_edit_ad_cancel'),
         ikb(user.GetButtons('💾 Сохранить'), callback_data='pa_edit_ad_save')]
    ])
    context = {'Lang': user.lang,
               'Ad': ad}
    msg = loader.get_template('bot/PersonalArea/EditAd/edit.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


###############
# Subcategory #
###############
def edit_subcategory(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Subcategory'
    user.save()
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    ads = Ad.objects.filter(creator=user)
    button_list = []
    node = MutualPRCategory.objects.get(category_name=ad.category)
    subcategories = node.get_children()
    for sub in subcategories:
        button_list.append(ikb(sub.category_name, callback_data='pa_edit_subcat_'+sub.category_name))
    button_list.append(ikb(user.GetButtons('«'), callback_data='back_inline'))
    context = {'Lang': user.lang,
               'Ad': ad}
    msg = loader.get_template('bot/PersonalArea/EditAd/edit_subcategory.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(build_menu(button_list, n_cols=2)), save_massage_id=True)


def set_subcategory(bot, update, user_data):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    ad.subcategory = update.callback_query.data[15:]
    ad.save()
    user_data['ad_id'] = ad.id
    edit(bot, update, user_data)


################
# Channel name #
################
def edit_channel_name(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/ChannelName'
    user.save()
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    keyboard = ReplyKeyboardMarkup([['«']], resize_keyboard=True, one_time_keyboard=True)
    context = {'Lang': user.lang,
               'Ad': ad}
    msg = loader.get_template('bot/PersonalArea/EditAd/edit_channel_name.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


def set_channel_name(bot, update, user_data):
    # Здесь я использовал юзер дату, что бы главное меню редактора получило id канала для редактирования
    user = Users.objects.get(telegram_id=update.message.chat.id)
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    ad.channel_name = update.message.text
    ad.save()
    user_data['ad_id'] = ad.id
    user.DelEndParams(2)
    edit(bot, update, user_data)


##############
# Min. count #
##############
def edit_min_count(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/MinCount'
    user.save()
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    keyboard = ReplyKeyboardMarkup([['«']], resize_keyboard=True, one_time_keyboard=True)
    context = {'Lang': user.lang,
               'Ad': ad}
    msg = loader.get_template('bot/PersonalArea/EditAd/edit_min_count.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


def set_min_count(bot, update, user_data):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    ad.min_count = int(update.message.text)
    ad.save()
    user_data['ad_id'] = ad.id
    user.DelEndParams(2)
    edit(bot, update, user_data)


###########
# Comment #
###########
def edit_comment(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Comment'
    user.save()
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    keyboard = ReplyKeyboardMarkup([['«']], resize_keyboard=True, one_time_keyboard=True)
    context = {'Lang': user.lang,
               'Ad': ad}
    msg = loader.get_template('bot/PersonalArea/EditAd/edit_comment.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


def set_comment(bot, update, user_data):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    ad.comment = update.message.text
    ad.save()
    user_data['ad_id'] = ad.id
    user.DelEndParams(2)
    edit(bot, update, user_data)


####################
# Save information #
####################
def save(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/EditAd/save.html').render(context)
    user.DelEndParams(3)
    user.SendMessage(bot=bot, msg=msg, save_massage_id=True)
    sleep(2)
    edit_ads_menu(bot, update)

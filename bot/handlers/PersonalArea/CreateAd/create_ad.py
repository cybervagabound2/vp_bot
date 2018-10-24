from time import sleep
import re
from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb, ReplyKeyboardMarkup
from bot.models import Users, MutualPRCategory, Ad
from django.template import loader
from bot.handlers import MainMenu
from bot.handlers.helpers import build_menu


def ad_category(bot, update):
    if update.callback_query:
        user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    elif update.message:
        user = Users.objects.get(telegram_id=update.message.chat.id)
    ad = Ad.objects.create(creator=user)
    user.params += '/CreateAd'
    user.params += '/' + str(ad.id)
    user.save()
    category = MutualPRCategory.objects.root_nodes()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/CreateAd/create_ad.html').render(context)
    keyboard = []
    for cat in category:
        keyboard.append([ikb(user.GetButtons(cat.category_name), callback_data='PA_create_ad_category_' + cat.category_name)])
    keyboard.append([ikb(user.GetButtons('«'), callback_data='back_inline')])
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(keyboard), save_massage_id=True)


def set_ad_category(bot, update):
    query = update.callback_query
    category = query.data
    user = Users.objects.get(telegram_id=query.from_user.id)
    ad = Ad.objects.get(id=int(re.findall('CreateAd/(\d+)', user.params)[0]))
    ad.category = category[22:]
    ad.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/CreateAd/set_ad_category.html').render(context)
    user.SendMessage(bot=bot, msg=msg, save_massage_id=True)
    sleep(2)
    ad_subcategory(bot, update)


def ad_subcategory(bot, update):
    if update.callback_query:
        user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    elif update.message:
        user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params += '/SubCategory'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/CreateAd/ad_subcategory.html').render(context)
    button_list = []
    ad = Ad.objects.get(id=int(re.findall('CreateAd/(\d+)', user.params)[0]))
    node = MutualPRCategory.objects.get(category_name=ad.category)
    subcategories = node.get_children()
    for sub in subcategories:
        button_list.append(ikb(user.GetButtons(sub.category_name), callback_data='PA_subcategory_' + sub.category_name))
        #button_list.append(ikb(sub.category_name, callback_data='PA_subcategory_' + sub.category_name))
    button_list.append(ikb(user.GetButtons('«'), callback_data='back_inline'))
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(build_menu(button_list, n_cols=2)), save_massage_id=True)


def set_ad_cat_subcat(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    ad = Ad.objects.get(id=int(re.findall('CreateAd/(\d+)', user.params)[0]))
    ad.subcategory = update.callback_query.data[15:]
    ad.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/CreateAd/set_item_cat_subcat.html').render(context)
    user.SendMessage(bot=bot, msg=msg, save_massage_id=True)
    sleep(2)
    ad_channel_name(bot, update)


def ad_channel_name(bot, update):
    if update.callback_query:
        user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    elif update.message:
        user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params += '/ChannelName'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/CreateAd/ad_channel_name.html').render(context)
    keyboard = ReplyKeyboardMarkup([['«']], resize_keyboard=True, one_time_keyboard=True)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard)


def set_channel_name(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    ad = Ad.objects.get(id=int(re.findall('CreateAd/(\d+)', user.params)[0]))
    ad.channel_name = update.message.text
    ad.save()
    min_count(bot, update)


def min_count(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params += '/MinCount'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/CreateAd/min_count.html').render(context)
    keyboard = ReplyKeyboardMarkup([['«']], resize_keyboard=True, one_time_keyboard=True)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard)


def set_min_count(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    ad = Ad.objects.get(id=int(re.findall('CreateAd/(\d+)', user.params)[0]))
    ad.min_count = update.message.text
    ad.save()
    comment(bot, update)


def comment(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    user.params += '/Comment'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/CreateAd/comment.html').render(context)
    keyboard = ReplyKeyboardMarkup([['«']], resize_keyboard=True, one_time_keyboard=True)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard)


def set_comment(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    ad = Ad.objects.get(id=int(re.findall('CreateAd/(\d+)', user.params)[0]))
    ad.comment = update.message.text
    ad.status = 'rd'
    ad.localization = user.lang.lang
    ad.save()
    clean_up = Ad.objects.filter(creator=user, status='nr').delete()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/PersonalArea/CreateAd/set_comment.html').render(context)
    user.DelEndParams()
    user.SendMessage(bot=bot, msg=msg, save_massage_id=True)
    sleep(2)
    MainMenu.MainMenu(bot, update)

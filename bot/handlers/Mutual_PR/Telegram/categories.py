import re
from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb, ReplyKeyboardMarkup
from django.template import loader
from bot.models import Users, Ad, MutualPRCategory
from bot.handlers.helpers import build_menu


def get_count_ads(subcategory, user_lang):
    count = Ad.objects.filter(localization=user_lang, category='Telegram', subcategory=subcategory).count()
    return str(count)


def categories_menu(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Telegram/Subcategory'
    user.save()
    node = MutualPRCategory.objects.get(id=1)
    subcategories = node.get_children()
    button_list = []
    for sub in subcategories:
        button_list.append(ikb(sub.category_name + ' (' + get_count_ads(sub.category_name, user_lang=user.lang) + ')', callback_data='mp_subcategory' + sub.category_name))
    button_list.append(ikb(user.GetButtons('«'), callback_data='back_inline'))
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/Mutual_PR/Telegram/categories_menu.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(build_menu(button_list, n_cols=2)),
                     save_massage_id=True)


def list(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Subcategory'
    user.save()
    ad = Ad.objects.get(id=int(re.findall('Editing/(\d+)', user.params)[0]))
    ads = Ad.objects.filter(creator=user)
    keyboard = []
    node = MutualPRCategory.objects.get(category_name=ad.category)
    subcategories = node.get_children()
    for sub in subcategories:
        keyboard.append([ikb(sub.category_name, callback_data='pa_edit_subcat_'+sub.category_name)])
    keyboard.append([ikb(user.GetButtons('«'), callback_data='back_inline')])
    context = {'Lang': user.lang,
               'Ad': ad}
    msg = loader.get_template('bot/PersonalArea/EditAd/edit_subcategory.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(keyboard), save_massage_id=True)


"""
button_list = [[KeyboardButton(s)] for s in some_strings]


reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
"""


"""
def categories_menu(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Telegram'
    user.save()
    node = MutualPRCategory.objects.get(id=1)
    subcategories = node.get_children()
    button_list = []
    for sub in subcategories:
        button_list.append(ikb(sub.category_name, callback_data='mp_subcategory' + sub.category_name))
    button_list.append(ikb(user.GetButtons('«'), callback_data='back_inline'))
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/Mutual_PR/Telegram/categories_menu.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(build_menu(button_list, n_cols=2)),
                     save_massage_id=True)
"""
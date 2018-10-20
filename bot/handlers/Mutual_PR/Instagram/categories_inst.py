import re
from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb, ReplyKeyboardMarkup
from django.template import loader
from bot.models import Users, Ad, MutualPRCategory
from bot.handlers.helpers import build_menu


def get_count_ads(subcategory, user_lang):
    count = Ad.objects.filter(localization=user_lang, subcategory=subcategory, category='Instagram').count()
    return str(count)


def categories_menu(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.params += '/Instagram'
    user.save()
    node = MutualPRCategory.objects.get(id=2)
    subcategories = node.get_children()
    button_list = []
    for sub in subcategories:
        button_list.append(ikb(sub.category_name + ' (' + get_count_ads(sub.category_name, user_lang=user.lang) + ')',
                               callback_data='i_subcategory' + sub.category_name))
    button_list.append(ikb(user.GetButtons('«'), callback_data='back_inline'))
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/Mutual_PR/Telegram/categories_menu.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(build_menu(button_list, n_cols=2)),
                     save_massage_id=True)

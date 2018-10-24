from telegram import InlineKeyboardMarkup, InlineKeyboardButton as ikb, ReplyKeyboardMarkup
from django.template import loader
from bot.models import Users, Ad, MutualPRCategory
from bot.handlers.helpers import build_menu


def pr_menu_sort(bot, update, user_data):
    query = update.callback_query
    user = Users.objects.get(telegram_id=query.from_user.id)
    if 'mp_subcategory' in query.data:
        user_data['category_name'] = query.data[14:]
    else:
        pass
    user.params += '/Sorting'
    user.save()
    context = {'Lang': user.lang}
    msg = loader.get_template('bot/Mutual_PR/Telegram/pr_menu/pr_menu_sort.html').render(context)
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('Подписчики 🔼'), callback_data='mp_sorting_followers_up'),
         ikb(user.GetButtons('Подписчики 🔽'), callback_data='mp_sorting_followers_down')],
        [ikb(user.GetButtons('Сначала новые 🕓'), callback_data='mp_sorting_date_new'),
         ikb(user.GetButtons('Сначала старые 🕑'), callback_data='mp_sorting_date_old')],
        [ikb(user.GetButtons('«'), callback_data='back_inline')]
    ])
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)


def pr_menu(bot, update, user_data):
    query = update.callback_query
    user = Users.objects.get(telegram_id=query.from_user.id)
    user.params += '/AdsList'
    user.save()
    if query.data == 'mp_sorting_followers_up':
        ads = Ad.objects.filter(localization=user.lang,
                                category='Telegram', subcategory=user_data['category_name']).order_by('min_count')
    elif query.data == 'mp_sorting_followers_down':
        ads = Ad.objects.filter(localization=user.lang,
                                category='Telegram', subcategory=user_data['category_name']).order_by('-min_count')
    elif query.data == 'mp_sorting_date_new':
        ads = Ad.objects.filter(localization=user.lang,
                                category='Telegram', subcategory=user_data['category_name']).order_by('pub_date')
    else:
        ads = Ad.objects.filter(localization=user.lang,
                                category='Telegram', subcategory=user_data['category_name']).order_by('-pub_date')
    button_list = []
    for ad in ads:
        button_list.append(ikb('@' + ad.channel_name[13:]+' от '+str(ad.min_count), callback_data='mp_ad_' + str(ad.id)))
    button_list.append(ikb(user.GetButtons('«'), callback_data='back_inline'))
    context = {'Lang': user.lang,
               'Subcategory': user_data['category_name']}
    msg = loader.get_template('bot/Mutual_PR/Telegram/pr_menu/pr_menu.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=InlineKeyboardMarkup(build_menu(button_list, n_cols=2)),
                     save_massage_id=True)


def view_ad(bot, update):
    query = update.callback_query
    user = Users.objects.get(telegram_id=query.from_user.id)
    user.params += '/ViewAd'
    user.save()
    ad = Ad.objects.get(id=query.data[6:])
    keyboard = InlineKeyboardMarkup([
        [ikb(user.GetButtons('📲 Связаться с администратором'), url='https://t.me/' + ad.creator.username)],
        [ikb(user.GetButtons('«'), callback_data='back_inline')]
    ])
    context = {'Lang': user.lang,
               'Ad': ad}
    msg = loader.get_template('bot/Mutual_PR/Telegram/pr_menu/view_ad.html').render(context)
    user.SendMessage(bot=bot, msg=msg, keyboard=keyboard, save_massage_id=True)

from bot.handlers import MainMenu
from bot.handlers.PersonalArea.personal_area import personal_area, my_ads
from telegram.update import Message as MSG
from django.template import loader
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import re
from telegram import CallbackQuery, User as user_telegram
from bot.models import Users
from bot.handlers.PersonalArea.CreateAd.create_ad import ad_category
from bot.handlers.PersonalArea.EditAd.edit_ads import edit_ads_menu, edit
from bot.handlers.Mutual_PR.mutual_pr import mutual_menu
from bot.handlers.Mutual_PR.Telegram.categories import categories_menu
from bot.handlers.Mutual_PR.Telegram.pr_menu.pr_menu import pr_menu_sort


def back_inline(bot, update, user_data):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.DelEndParams()
    func = user.params
    if func.startswith('/PersonalArea'):
        if 'Ads' in func:
            if '/PersonalArea/Ads/CreateAd' in func:
                if re.match('/PersonalArea/Ads/CreateAd/(\d+)$', user.params):
                    user.DelEndParams(2)
                    ad_category(bot, update)
            elif '/Editing' in func:
                if re.match('/PersonalArea/Ads/Editing/(\d+)$', user.params):
                    edit(bot, update, user_data)
            else:
                user.DelEndParams()
                my_ads(bot, update)
        elif '/Feedback' in func:
            pass
        elif '/Support' in func:
            pass
        else:
            personal_area(bot, update)
    elif func.startswith('/Mutual'):
        if '/Telegram' in func:
            if '/Subcategory' in func:
                if '/Sorting' in func:
                    if 'AdsList' in func:
                        pass
                    else:
                        user.DelEndParams()
                        pr_menu_sort(bot, update, user_data)
                else:
                    user.DelEndParams(2)
                    categories_menu(bot, update)
            else:
                user.DelEndParams()
                mutual_menu(bot, update)
        elif '/Instagram' in func:
            pass
        else:
            mutual_menu(bot, update)


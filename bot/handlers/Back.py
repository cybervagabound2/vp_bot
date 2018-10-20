from bot.handlers import MainMenu
from bot.handlers.PersonalArea.personal_area import personal_area, my_ads
from telegram.update import Message as MSG
from django.template import loader
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import re
from telegram import CallbackQuery, User as user_telegram
from bot.models import Users
from bot.handlers.PersonalArea.CreateAd.create_ad import ad_category


def back_inline(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.DelEndParams()
    func = user.params
    if func.startswith('/PersonalArea'):
        if 'Ads' in func:
            if '/PersonalArea/Ads/CreateAd' in func:
                if re.match('/PersonalArea/Ads/CreateAd/(\d+)$', user.params):
                    user.DelEndParams(2)
                    ad_category(bot, update)
            else:
                my_ads(bot, update)
        elif 'Feedback' in func:
            pass
        elif 'Support' in func:
            pass
        else:
            personal_area(bot, update)


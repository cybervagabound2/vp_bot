from telegram.ext import BaseFilter
from bot.models import Users
import re


class FilterLang(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return user.params.endswith('SelectLang')


class FilterSelectRules(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return user.params.endswith('Rules')


class FilterBan(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return True
        return not user.banned


class FilterRules(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return user.rules


class FilterMainMenu(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return user.params == ''


class FilterPersonalArea(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return user.params == '/PersonalArea'


class FilterButtonPersonalArea(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
            buttons = user.GetButtons('💻 Личный кабинет')
            if message.text == buttons:
                return True
        except:
            return False


class FilterCreateAdSubcategory(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return re.match('/PersonalArea/Ads/CreateAd/(\d+)', user.params)


class FilterMinCount(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return re.match('/PersonalArea/Ads/CreateAd/(\d+)/SubCategory/ChannelName/MinCount', user.params)


class FilterComment(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return re.match('/PersonalArea/Ads/CreateAd/(\d+)/SubCategory/ChannelName/MinCount/Comment', user.params)


class FilterChannelName(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return re.match('/PersonalArea/Ads/CreateAd/(\d+)/SubCategory/ChannelName', user.params)


class FilterEditChannelName(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return re.match('/PersonalArea/Ads/Editing/(\d+)/ChannelName', user.params)


class FilterEditAdMinCount(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return re.match('/PersonalArea/Ads/Editing/(\d+)/MinCount', user.params)


class FilterEditAdComment(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return re.match('/PersonalArea/Ads/Editing/(\d+)/Comment', user.params)


class FilterFeedbackSendMsg(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
        except:
            return False
        return user.params == '/PersonalArea/Feedback/WriteMessage'


class FilterBack(BaseFilter):
    def filter(self, message):
        try:
            user = Users.objects.get(telegram_id=message.chat.id)
            back = user.GetButtons('«')
            if message.text == back:
                return True
        except:
            return False
        return False
"""
DIS.add_handler(MessageHandler(
    Filter & BaseFilters.FilterPersonalArea() & BaseFilters.FilterButtonWishesToImprove(),
    WishesToImprove.start))
DIS.add_handler(MessageHandler(
    Filter & BaseFilters.FilterPersonalArea() & BaseFilters.FilterButtonDonate(),
    Donate.Donate))
DIS.add_handler(MessageHandler(
    Filter & BaseFilters.FilterPersonalArea() & BaseFilters.FilterButtonNewProject(),
    NewProject.NewProject))
DIS.add_handler(MessageHandler(
    Filter & BaseFilters.FilterNewProject() & BaseFilters.FilterButtonNewProjectSelect(),
    NewProject.SelectionProject))

DIS.add_handler(MessageHandler(
    Filter & BaseFilters.FilterPersonalArea() & BaseFilters.FilterButtonTickets(),
"""
from bot.handlers import MainMenu
from bot.handlers.PersonalArea.personal_area import personal_area, my_ads
from telegram.update import Message as MSG
from django.template import loader
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import re
from telegram import CallbackQuery, User as user_telegram
from bot.models import Users

"""
def Back(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    user.DelEndParams()
    func = user.params
    if func == '':
        MainMenu.MainMenu(bot, update)
    elif func.startswith('/PersonalArea'):
        if 'NewProject' in func:
            if 'SelectionProject' in func:
                if 'Bot' in func:
                    if 'Avtomatic' in func:
                        if 'CountUser' in func:
                            if 'Localization' in func:
                                user.DelEndParams()
                                Bot.Localization(bot, update)
                            else:
                                user.DelEndParams()
                                Bot.CountUser(bot, update)
                        else:
                            user.DelEndParams()
                            user.DelEndParams()
                            try:
                                bot_add = Bots.objects.get(user=user, status='avt')
                                bot_add.delete()
                            except Exception as e:
                                user.Error(bot, e, 'Tmarket2bot.back.PersonalArea.NewProject.SelectionProject.Bot')
                            Bot.Bot(bot, update)
                    else:
                        user.DelEndParams()
                        try:
                            bot_add = Bots.objects.get(user=user, status='avt')
                            bot_add.delete()
                        except Exception as e:
                            user.Error(bot, e, 'Back//bot_add.delete()')
                        user.DelEndParams()
                        NewProject.SelectionProject(bot, update)
                elif 'Channel' in func:
                    if 'Avtomatic' in func:
                        if 'CountViews' in func:
                            if 'Localization' in func:
                                user.DelEndParams()
                                Channel.Localization(bot, update)
                            else:
                                user.DelEndParams()
                                Channel.CountViews(bot, update)
                        else:
                            user.DelEndParams()
                            user.DelEndParams()
                            try:
                                Channel_add = Channels.objects.get(user=user, status='avt')
                                bot.leave_chat(chat_id=Channel_add.telegram_id)
                                Channel_add.delete()
                            except Exception as e:
                                user.Error(bot, e, 'Back//bot.leave_chat')
                            Channel.Channel(bot, update)
                    else:
                        user.DelEndParams()
                        user.DelEndParams()
                        try:
                            Channel_add = Channels.objects.get(user=user, status='avt')
                            bot.leave_chat(chat_id=Channel_add.telegram_id)
                            Channel_add.delete()
                        except Exception as e:
                            user.Error(bot, e, 'Back//bot.leave_chat')
                        NewProject.SelectionProject(bot, update)
                elif 'Chat' in func:
                    if 'Avtomatic' in func:
                        if 'Localization' in func:
                            user.DelEndParams()
                            Chat.Localization(bot, update)
                        else:
                            try:
                                chat = Groups.objects.get(user=user, status='avt')
                                bot.leave_chat(chat_id=chat.telegram_id)
                                chat.delete()
                            except Exception as e:
                                user.Error(bot, e, 'Back//bot.leave_chat')
                            user.DelEndParams()
                            user.DelEndParams()
                            Chat.Chat(bot, update)
                    else:
                        try:
                            chat = Groups.objects.get(user=user, status='avt')
                            bot.leave_chat(chat_id=chat.telegram_id)
                            chat.delete()
                        except Exception as e:
                            user.Error(bot, e, 'Back//bot.leave_chat')
                        user.DelEndParams()
                        user.DelEndParams()
                        NewProject.SelectionProject(bot, update)
                elif 'Service' in func:
                    if 'Description' in func:
                        if 'Localization' in func:
                            if 'Photo' in func:
                                user.DelEndParams()
                                Service.Photo(bot, update)
                            else:
                                user.DelEndParams()
                                Service.Localization(bot, update)
                        else:
                            user.DelEndParams()
                            Service.Description(bot, update)
                    else:
                        user.DelEndParams()
                        try:
                            Services_add = Service.Services.objects.get(user=user, status='avt')
                            Services_add.delete()
                        except Exception as e:
                            user.Error(bot, e, 'Back//Services_add.delete')
                        Service.Service(bot, update)
                else:
                    user.DelEndParams()
                    NewProject.SelectionProject(bot, update)
            else:
                user.DelEndParams()
                NewProject.NewProject(bot, update)
        elif 'ProjectManager' in func:
            if 'Bots' in func:
                if re.match('/PersonalArea/ProjectManager/Bots/(\d+)$', user.params):
                    update.callback_query.data = 'MenProgGroup' + \
                                                 re.findall('/PersonalArea/ProjectManager/Bots/(\d+)', user.params)[
                                                     0]
                    user.DelEndParams()
                    ManagerBot.ManagerBot(bot, update)
                elif '/Manage' in func:
                    user.DelEndParams()
                    Update_Bots.Manager(bot, update)
                elif '/MatualPR' in func:
                    if '/Edit' in func:
                        user.DelEndParams()
                        data = CallbackQuery
                        data.from_user = user_telegram
                        data.from_user.id = user.telegram_id
                        update.callback_query = data
                        MutualPR_Bots.Edit(bot, update)
                    elif '/Description' in func:
                        user.DelEndParams()
                        project = Bots.objects.filter(user=user, community_type__mutual_pr__min_count_followers=0)
                        project.delete()
                        data = CallbackQuery
                        data.from_user = user_telegram
                        data.from_user.id = user.telegram_id
                        update.callback_query = data
                        MutualPR_Bots.Continue(bot, update)
                    else:
                        a = re.findall('/PersonalArea/ProjectManager/Bots/(\d+)/MatualPR', user.params)[0]
                        data = CallbackQuery
                        data.data= 'MenProgBot'+a
                        data.from_user = user_telegram
                        data.from_user.id=user.telegram_id
                        update.callback_query = data
                        user.DelEndParams(2)
                        ManagerBot.ManagerBot(bot, update)
                else:
                    user.DelEndParams()
                    ProjectManager.ProjectManager(bot, update)
            elif 'Channels' in func:
                if re.match('/PersonalArea/ProjectManager/Channels/(\d+)$', user.params):
                    update.callback_query.data = 'MenProgChannel' + \
                                                 re.findall('/PersonalArea/ProjectManager/Channels/(\d+)', user.params)[
                                                     0]
                    user.DelEndParams()
                    ManagerChannel.ManagerChannel(bot, update)
                elif '/Manage' in func:
                    user.DelEndParams()
                    Update_Channels.Manager(bot, update)
                elif '/MatualPR' in func:
                    if '/Edit' in func:
                        user.DelEndParams()
                        data = CallbackQuery
                        data.from_user = user_telegram
                        data.from_user.id = user.telegram_id
                        update.callback_query = data
                        MutualPR_Channels.Edit(bot, update)
                    elif '/Description' in func:
                        user.DelEndParams()
                        Channels_ = Channels.objects.filter(user=user, community_type__mutual_pr__min_count_followers=0)
                        Channels_.delete()
                        data = CallbackQuery
                        data.from_user = user_telegram
                        data.from_user.id = user.telegram_id
                        update.callback_query = data
                        MutualPR_Channels.Continue(bot, update)
                    else:
                        a = re.findall('/PersonalArea/ProjectManager/Channels/(\d+)/MatualPR', user.params)[0]
                        data = CallbackQuery
                        data.data= 'MenProgChannel'+a
                        data.from_user = user_telegram
                        data.from_user.id=user.telegram_id
                        update.callback_query = data
                        user.DelEndParams(2)
                        ManagerChannel.ManagerChannel(bot, update)
                else:
                    user.DelEndParams()
                    Channels_Manager.Channels(bot, update)
            elif 'Groups' in func:
                if re.match('/PersonalArea/ProjectManager/Groups/(\d+)$', user.params):
                    update.callback_query.data = 'MenProgGroup' + \
                                                 re.findall('/PersonalArea/ProjectManager/Groups/(\d+)', user.params)[
                                                     0]
                    user.DelEndParams()
                    ManagerGroup.ManagerGroup(bot, update)
                elif '/Manage' in func:
                    user.DelEndParams()
                    Update_Groups.Manager(bot, update)
                elif '/MatualPR' in func:
                    if '/Edit' in func:
                        user.DelEndParams()
                        data = CallbackQuery
                        data.from_user = user_telegram
                        data.from_user.id = user.telegram_id
                        update.callback_query = data
                        MutualPR_Groups.Edit(bot, update)
                    elif '/Description' in func:
                        user.DelEndParams()
                        project = Groups.objects.filter(user=user, community_type__mutual_pr__min_count_followers=0)
                        project.delete()
                        data = CallbackQuery
                        data.from_user = user_telegram
                        data.from_user.id = user.telegram_id
                        update.callback_query = data
                        MutualPR_Groups.Continue(bot, update)
                    else:
                        a = re.findall('/PersonalArea/ProjectManager/Groups/(\d+)/MatualPR', user.params)[0]
                        data = CallbackQuery
                        data.data= 'MenProgGroup'+a
                        data.from_user = user_telegram
                        data.from_user.id=user.telegram_id
                        update.callback_query = data
                        user.DelEndParams(2)
                        ManagerGroup.ManagerGroup(bot, update)
                else:
                    user.DelEndParams()
                    ProjectManager.ProjectManager(bot, update)
            elif 'Services' in func:
                if '' in func:
                    print('ass')
                else:
                    user.DelEndParams()
                    ProjectManager.ProjectManager(bot, update)
            else:
                user.DelEndParams()
                ProjectManager.ProjectManager(bot, update)
        else:
            user.DelEndParams()
            PersonalArea(bot, update)
    elif func.startswith('/Mutual'):
        if '/CreateShop' in func:
            if '/Name' in func:
                if '/About' in func:
                    if '/Reviews' in func:
                        if '/Comment' in func:
                            if '/CheckingInfo' in func:
                                user.DelEndParams()
                                create_shop.create_shop_check(bot, update)
                            else:
                                user.DelEndParams()
                                create_shop.create_shop_comment(bot, update)
                        else:
                            user.DelEndParams()
                            create_shop.create_shop_reviews(bot, update)
                    else:
                        user.DelEndParams()
                        create_shop.create_shop_about(bot, update)
                else:
                    user.DelEndParams()
                    create_shop.create_shop_name(bot, update)
            else:
                user.DelEndParams()
                create_shop.create_shop(bot, update)
        else:
            user.DelEndParams()
            create_shop.create_shop(bot, update)
"""


def back_inline(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.DelEndParams()
    func = user.params
    if func.startswith('/PersonalArea'):
        if 'Ads' in func:
            if '/PersonalArea/Ads/CreateAd' in func:
                my_ads(bot, update)
        elif 'Feedback' in func:
            pass
        elif 'Support' in func:
            pass
        else:
            personal_area(bot, update)




"""
def back_inline(bot, update):
    user = Users.objects.get(telegram_id=update.callback_query.from_user.id)
    user.DelEndParams()
    func = user.params
    if func.startswith('/DigitalShop'):
        if '/CreateShop' in func:
            if '/Name' in func:
                if '/About' in func:
                    if '/Reviews' in func:
                        if '/Comment' in func:
                            user.DelEndParams()
                            create_shop.create_shop_comment(bot, update)
                    else:
                        user.DelEndParams()
                        create_shop.create_shop_reviews(bot, update)
                else:
                    user.DelEndParams()
                    create_shop.create_shop_about(bot, update)
            else:
                user.DelEndParams()
                create_shop.create_shop(bot, update)
        else:
            user.DelEndParams()
            digital_shop.digital_shop(bot, update)
    elif func.startswith('/PersonalArea'):
        if '/Ads' in func:
        
            pass
        else:
            personal_area(bot,update


"""
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, RegexHandler
from bot.filters import BaseFilters
from bot.handlers.start import start
from bot.handlers import Rules
from bot.handlers import Language
from bot.handlers.PersonalArea import personal_area
from bot.handlers.PersonalArea.CreateAd import create_ad
from bot.handlers.PersonalArea.EditAd import edit_ads
from bot.handlers.PersonalArea.DeleteAd import delete_ad
from bot.handlers.Mutual_PR import mutual_pr
from bot.handlers.Mutual_PR.Telegram import categories
from bot.handlers.Mutual_PR.Instagram import categories_inst
from bot.handlers.Mutual_PR.Telegram.pr_menu import pr_menu
from bot.handlers.Mutual_PR.Instagram.pr_menu import pr_menu_inst
from bot.handlers.PersonalArea.SupportProject import support_project
from bot.handlers.PersonalArea.Feedback import feedback
from bot.handlers.Back import back_inline, back
from bot.handlers.Adminka.admin import (admin_menu, send_msg_menu, send_msg_text, send_msg, reply_to_admin,
                                        send_reply_to_admin, delete_ad_menu, delete_ad_reason, delete_ads,
                                        broadcast_menu, broadcast_text, broadcast, statistic)
from bot.handlers.MainMenu import MainMenu


API_TOKEN = '721609870:AAGBix6dGkIqjsA1nAY_4AtqAftYhTrN-Sc'
BOT = Bot(API_TOKEN)
DIS = Dispatcher(BOT, None, workers=0)
DIS.add_handler(CommandHandler('start', start))
Filter = Filters.text & Filters.private & BaseFilters.FilterBan() & BaseFilters.FilterRules()

# Adminka
DIS.add_handler(CommandHandler('admin', admin_menu))
DIS.add_handler(CallbackQueryHandler(send_msg_menu, pattern='^admin_send_msg$'))
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterAdminkaSendMsg(),
                               send_msg_text, pass_user_data=True))
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterAdminkaSendMsgText(),
                               send_msg, pass_user_data=True))
DIS.add_handler(CallbackQueryHandler(reply_to_admin, pattern='^admin_msg_reply$'))
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterAdminkaReplyToAmin(),
                               send_reply_to_admin))
DIS.add_handler(CallbackQueryHandler(delete_ad_menu, pattern='^admin_delete_ad$'))
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterAdminkaDeleteAd(),
                               delete_ad_reason, pass_user_data=True))
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterAdminkaReason(),
                               delete_ads, pass_user_data=True))
DIS.add_handler(CallbackQueryHandler(broadcast_menu, pattern='^admin_broadcast$'))
DIS.add_handler(CallbackQueryHandler(broadcast_text, pattern=r'^broadcast_(.*)$',
                                     pass_user_data=True))
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterAdminkaBroadcastText(),
                               broadcast, pass_user_data=True))
DIS.add_handler(CallbackQueryHandler(statistic, pattern='^admin_statistic$'))
DIS.add_handler(MessageHandler(
    Filter & BaseFilters.FilterBack(),
    back, pass_user_data=True))

DIS.add_handler(MessageHandler(Filters.text & Filters.private & BaseFilters.FilterLang() & BaseFilters.FilterBan(),
                               Language.SelectLang))
DIS.add_handler(
    MessageHandler(Filters.text & Filters.private & BaseFilters.FilterBan() & BaseFilters.FilterSelectRules(),
                   Rules.Result))
DIS.add_handler(
    MessageHandler(Filters.text & Filters.private & BaseFilters.FilterBan() & BaseFilters.FilterSelectRules(),
                   Rules.Result))
"""
DIS.add_handler(MessageHandler(
    Filter & BaseFilters.FilterMainMenu() & BaseFilters.FilterButtonPersonalArea(),
    personal_area.personal_area))
"""
DIS.add_handler(RegexHandler("^(🗂 Список ВП|🗂 List of MP|🗂 Ro'yxat Cross PR)$", mutual_pr.mutual_menu))
DIS.add_handler(RegexHandler('^(💻 Личный кабинет|💻 Personal Area|💻 Shaxsiy kabinet)$', personal_area.personal_area))
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterComment(),
                               create_ad.set_comment))


DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterMinCount(),
                               create_ad.set_min_count))

DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterChannelName(),
                               create_ad.set_channel_name))


"""
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterCreateAdSubcategory(),
                               create_ad.set_ad_category))
"""
# EditAds

DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterEditChannelName(),
                               edit_ads.set_channel_name, pass_user_data=True))

DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterEditAdMinCount(),
                               edit_ads.set_min_count, pass_user_data=True))

DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterEditAdComment(),
                               edit_ads.set_comment, pass_user_data=True))
# Feedback
DIS.add_handler(MessageHandler(Filter & BaseFilters.FilterFeedbackSendMsg(),
                               feedback.send_message))


#####################
# Callback handlers #
#####################
DIS.add_handler(CallbackQueryHandler(personal_area.my_ads, pattern='^PA_my_ads$'))
DIS.add_handler(CallbackQueryHandler(create_ad.ad_category, pattern='^PA_create_ad$'))
DIS.add_handler(CallbackQueryHandler(create_ad.set_ad_category, pattern=r'^PA_create_ad_category_(.*)$'))
DIS.add_handler(CallbackQueryHandler(create_ad.set_ad_cat_subcat, pattern=r'^Pa_subcategory_(.*)$'))
# EditAds
DIS.add_handler(CallbackQueryHandler(edit_ads.edit_ads_menu, pattern='^PA_edit_ad$'))
DIS.add_handler(CallbackQueryHandler(edit_ads.edit, pattern='^PA_edit_ad(.*)$',
                                     pass_user_data=True))
DIS.add_handler(CallbackQueryHandler(edit_ads.edit_subcategory, pattern=r'^pa_edit_ad_subcategory(.*)$'))
DIS.add_handler(CallbackQueryHandler(edit_ads.edit_channel_name, pattern='^pa_edit_ad_channel_name$'))
DIS.add_handler(CallbackQueryHandler(edit_ads.edit_min_count, pattern='^pa_edit_ad_min_count$'))
DIS.add_handler(CallbackQueryHandler(edit_ads.edit_comment, pattern='^pa_edit_ad_comment$'))
DIS.add_handler(CallbackQueryHandler(edit_ads.set_subcategory, pattern=r'^pa_edit_subcat_(.*)$',
                                     pass_user_data=True))
DIS.add_handler(CallbackQueryHandler(edit_ads.save, pattern='^pa_edit_ad_save$'))
DIS.add_handler(CallbackQueryHandler(edit_ads.edit_ads_menu, pattern='^pa_edit_ad_cancel$'))
# DeleteAd
DIS.add_handler(CallbackQueryHandler(delete_ad.delete_ad_menu, pattern='^PA_delete_ad$'))
DIS.add_handler(CallbackQueryHandler(delete_ad.delete_ad_confirm, pattern='^PA_delete_ad(.*)$'))
DIS.add_handler(CallbackQueryHandler(delete_ad.delete_ad, pattern=r'^pa_delete_ad_(.*)$'))
# Mutual PR
DIS.add_handler(CallbackQueryHandler(categories.categories_menu, pattern='^MP_telegram$',
                                     pass_user_data=True))
DIS.add_handler(CallbackQueryHandler(categories_inst.categories_menu, pattern='^MP_instagram$',
                                     pass_user_data=True))

DIS.add_handler(CallbackQueryHandler(pr_menu.pr_menu_sort, pattern=r'^mp_subcategory(.*)$',
                                     pass_user_data=True))
DIS.add_handler(CallbackQueryHandler(pr_menu.pr_menu, pattern=r'^mp_sorting_(.*)$',
                                     pass_user_data=True))
DIS.add_handler(CallbackQueryHandler(pr_menu.view_ad, pattern=r'^mp_ad_(\d+)$'))

DIS.add_handler(CallbackQueryHandler(pr_menu_inst.pr_menu_sort, pattern=r'^i_subcategory(.*)$',
                                     pass_user_data=True))

DIS.add_handler(CallbackQueryHandler(pr_menu_inst.pr_menu, pattern=r'^inst_sorting_(.*)$',
                                     pass_user_data=True))
# Support project
DIS.add_handler(CallbackQueryHandler(support_project.support, pattern='^PA_support$'))
# Feedback
DIS.add_handler(CallbackQueryHandler(feedback.feedback, pattern='^PA_feedback$'))
DIS.add_handler(CallbackQueryHandler(feedback.write_message, pattern='^pa_feedback_create$'))


DIS.add_handler(CallbackQueryHandler(back_inline, pattern='^back_inline$',
                                     pass_user_data=True))

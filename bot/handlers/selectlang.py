from bot.models import Users, Lang as Language
from django.template import loader
from telegram import ReplyKeyboardMarkup

Lang = {'🇷🇺 Русский': 'Rus',
        '🇺🇸 English': 'Eng',
        "🇺🇿 O'zbek": "Uzb"}


def selectlang(bot, update):
    user = Users.objects.get(telegram_id=update.message.chat.id)
    lang = Language.objects.all()
    try:
        lang = lang.get(lang=Lang[update.message.text])
    except:
        lang = ReplyKeyboardMarkup([['🇷🇺 Русский', '🇺🇸 English']],
                                   resize_keyboard=True)
        msg = loader.get_template('bot/language.html').render()
        update.message.reply_text(msg, parse_mode='HTML',
                                  disable_web_page_preview=True, reply_markup=lang)
        return
    user.lang=lang
    if user.params =='/Start/SelectLang':
        user.params += '/Rules'
        context = {'Lang': user.lang}
        msg = loader.get_template('bot/rules.html').render(context)
        lang = ReplyKeyboardMarkup([[user.GetButtons('✅ I totally agree'), '❌ Disagree']], resize_keyboard=True)
        update.message.reply_text(msg, parse_mode='HTML', disable_web_page_preview=True, reply_markup=lang)
    elif user.params.endswith('SelectLang'):
        user.DelEndParams()
    user.save()

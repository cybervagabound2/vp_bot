from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def paginate(ads, per_page=10):
    items = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6',
             'item7', 'item8', 'item9', 'item10', 'item11', 'item12',
             'item13', 'item14', 'item15', 'item16']
    keyboard = []
    for item in items:
        for item in range(0, per_page):
            keyboard.append(InlineKeyboardButton(item, callback_data='test'))
    keyboard.append(InlineKeyboardButton('<<', callback_data='<<'))
    keyboard.append(InlineKeyboardButton('cancel', callback_data='cancel'))
    keyboard.append(InlineKeyboardButton('>>', callback_data='next_10'))
    return keyboard

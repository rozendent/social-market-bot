from aiogram import types

from setup import texts

legal_keyboard = types.InlineKeyboardMarkup(row_width=1)
legal_keyboard.add(types.InlineKeyboardButton(text=texts['legal_accept_btn'], callback_data='legal_accept'))
legal_keyboard.add(types.InlineKeyboardButton(text=texts['legal_deny_btn'], callback_data='legal_deny'))

start_keyboard = types.InlineKeyboardMarkup(row_width=1)
start_keyboard.add(types.InlineKeyboardButton(text=texts['welcome_btn'], callback_data='start'))

format_keyboard = types.InlineKeyboardMarkup(row_width=1)
format_keyboard.add(types.InlineKeyboardButton(text=texts['format_online'], callback_data='format_online'))
format_keyboard.add(types.InlineKeyboardButton(text=texts['format_offline'], callback_data='format_offline'))
format_keyboard.add(types.InlineKeyboardButton(text=texts['format_any'], callback_data='format_any'))


# sphere_keyboard = types.InlineKeyboardMarkup(row_width=1)
# sphere_poll = []
# for i in range(1, 16):
#     sphere_keyboard.add(types.InlineKeyboardButton(text=texts[f'sphere_{str(i)}'], callback_data=f'sphere_{str(i)}'))
#     sphere_poll.append(texts[f'sphere_{str(i)}'])


def get_sphere_keyboard(page, spheres_dict):
    sphere_keyboard = types.InlineKeyboardMarkup(row_width=1)
    pages = {1: range(1, 8), 2: range(9, 16)}
    if page == 1:
        sphere_keyboard.row(types.InlineKeyboardButton(text=f'{page}/2', callback_data=f'do_nthng'),
                            types.InlineKeyboardButton(text='→', callback_data=f'turn_page_2'))
    elif page == 2:
        sphere_keyboard.row(types.InlineKeyboardButton(text='←', callback_data=f'turn_page_1'),
                            types.InlineKeyboardButton(text=f'{page}/2', callback_data=f'do_nthng'))
    for i in pages[page]:
        if spheres_dict[i]:
            sphere_keyboard.add(types.InlineKeyboardButton(text='✓' + texts[f'sphere_{str(i)}'], callback_data=f'check_sphere_{i}'))
        else:
            sphere_keyboard.add(types.InlineKeyboardButton(text=texts[f'sphere_{str(i)}'], callback_data=f'check_sphere_{i}'))
    sphere_keyboard.add(types.InlineKeyboardButton(text='Готово', callback_data='done'))
    return sphere_keyboard


menu_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
menu_keyboard.add(texts['edit_btn'])
menu_keyboard.add(texts['view_users_btn'])


def get_user_keyboard(user_id):
    user_keyboard = types.InlineKeyboardMarkup(row_width=1)
    user_keyboard.add(types.InlineKeyboardButton(text=texts['contacts_btn'], callback_data=f'contact_{user_id}'))
    user_keyboard.add(types.InlineKeyboardButton(text=texts['pass_btn'], callback_data='pass'))
    return user_keyboard

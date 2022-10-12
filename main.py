# Хэндлер на команду /start
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils import executor

from data import db_session
from data.users import User
from keyboards import *
from setup import texts, dp, session, bot
from tools import make_user_message, get_relevant_user, get_empty_spheres_dict, get_list_from_spheres_dict

poll_storage = dict()


class Form(StatesGroup):
    name = State()
    age = State()
    format = State()
    city = State()
    sphere = State()
    role = State()
    skills = State()
    achievements = State()
    experience = State()
    requirements = State()


@dp.message_handler(commands="start", state='*')
async def start(message: types.Message):
    await message.answer_photo('AgACAgIAAxkBAAIE3mI1tEzyZoc9MVjB0L9vbtkWW_sYAAJ8uDEbcEWxSfcGDtnLxZwVAQADAgADeAADIwQ',
                               caption=texts['start'].format(message.from_user.first_name))
    await message.answer(texts['legal'], reply_markup=legal_keyboard)


@dp.callback_query_handler(text="legal_deny", state='*')
async def deny_legal(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer_photo(
        'AgACAgIAAxkBAAIE4GI1tGyGsiy2wHnmv_9HfzVS1uweAAJ9uDEbcEWxSXBPAtRK1CDLAQADAgADeAADIwQ',
        caption=texts['legal_denied'])


@dp.callback_query_handler(text="legal_accept", state='*')
async def accept_legal(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(texts['welcome'], reply_markup=start_keyboard)


@dp.callback_query_handler(text="start", state='*')
async def ask_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(texts['ask_name'])
    await Form.name.set()


@dp.message_handler(state=Form.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(texts['ask_age'])
    await Form.age.set()


@dp.message_handler(state=Form.age)
async def name(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(texts['age_error'])
        return
    await state.update_data(age=int(message.text))
    await message.answer(texts['ask_format'], reply_markup=format_keyboard)
    await Form.format.set()


@dp.callback_query_handler(text="format_online", state=Form.format)
async def format_online(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(format=1)  # online
    await call.answer()
    await state.update_data(page=1)
    await state.update_data(sphere_dict=get_empty_spheres_dict())
    data = await state.get_data()
    msg = await call.message.answer(texts['ask_sphere'], reply_markup=get_sphere_keyboard(data['page'], data['sphere_dict']))
    await state.update_data(msg=msg)
    await Form.sphere.set()


@dp.callback_query_handler(text="format_offline", state=Form.format)
async def format_offline(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(format=2)  # offline
    await call.answer()
    await call.message.answer(texts['ask_city'])
    await Form.city.set()


@dp.callback_query_handler(text="format_any", state=Form.format)
async def format_any(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(format=12)  # any
    await call.answer()
    await call.message.answer(texts['ask_city'])
    await Form.city.set()


@dp.callback_query_handler(Text(startswith='turn_page'), state='*')
async def turn_page(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    data['page'] = int(call.data.split('_')[-1])
    await state.update_data(**data)
    msg = data.get('msg')
    await msg.edit_reply_markup(reply_markup=get_sphere_keyboard(data['page'], data['sphere_dict']))
    await Form.sphere.set()


@dp.callback_query_handler(Text(startswith='check_sphere'), state='*')
async def check_sphere(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    sphere_id = int(call.data.split('_')[-1])
    data['sphere_dict'][sphere_id] = not data['sphere_dict'][sphere_id]
    await state.update_data(**data)
    msg = data.get('msg')
    await msg.edit_reply_markup(reply_markup=get_sphere_keyboard(data['page'], data['sphere_dict']))


@dp.message_handler(state=Form.city)
async def city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.update_data(page=1)
    await state.update_data(sphere_dict=get_empty_spheres_dict())
    data = await state.get_data()
    msg = await message.answer(texts['ask_sphere'],
                                    reply_markup=get_sphere_keyboard(data['page'], data['sphere_dict']))
    await state.update_data(msg=msg)
    await Form.sphere.set()


@dp.callback_query_handler(Text(equals='done'), state='*')
async def done(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    db_sess = db_session.create_session()
    await call.message.answer(texts['ask_role'])
    await Form.role.set()


# @dp.poll_answer_handler()
# async def poll_handler(quiz_answer: types.PollAnswer):
#     db_sess = db_session.create_session()
#     user = db_sess.query(User).filter(User.user_id == quiz_answer.user.id).first()
#     print(quiz_answer)
#     if quiz_answer.user.id in poll_storage or (user and user.sphere):
#         if user and user.sphere:
#             poll_storage[quiz_answer.user.id] = str(quiz_answer.option_ids)[1:-2]
#         else:
#             poll_storage[quiz_answer.user.id] = poll_storage[quiz_answer.user.id] + str(quiz_answer.option_ids)[1:-2]
#         await bot.send_message(quiz_answer.user.id, texts['ask_role'])
#         await Form.role.set()
#     else:
#         poll_storage[quiz_answer.user.id] = str(quiz_answer.option_ids)[1:-2]
#         await bot.send_message(quiz_answer.user.id, '111')
#     db_sess.commit()


@dp.callback_query_handler(Text(startswith='sphere_'), state=Form.sphere)
async def sphere(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(sphere=int(call.data.replace('sphere_', '')))
    await call.answer()
    await call.message.answer(texts['ask_role'])
    await Form.role.set()


@dp.message_handler(state=Form.role)
async def role(message: types.Message, state: FSMContext):
    await state.update_data(role=message.text)
    await message.answer(texts['ask_skills'])
    await Form.skills.set()


@dp.message_handler(state=Form.skills)
async def skills(message: types.Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await message.answer(texts['ask_achievements'])
    await Form.achievements.set()


@dp.message_handler(state=Form.achievements)
async def achievements(message: types.Message, state: FSMContext):
    await state.update_data(achievements=message.text)
    await message.answer(texts['ask_experience'])
    await Form.experience.set()


@dp.message_handler(state=Form.experience)
async def experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer(texts['ask_requirements'])
    await Form.requirements.set()


@dp.message_handler(state=Form.requirements)
async def requirements(message: types.Message, state: FSMContext):
    await message.answer(texts['done'], reply_markup=menu_keyboard)
    u = session.query(User).filter(User.user_id == message.from_user.id).first()
    if not u:
        u = User()
    d = await state.get_data()
    u.name = d['name']
    u.username = message.from_user.username
    u.user_id = message.from_user.id
    u.age = d['age']
    u.format = d.get('format')
    u.city = d.get('city')
    u.sphere = get_list_from_spheres_dict(d.get('sphere_dict'))
    u.role = d.get('role')
    u.skills = d.get('skills')
    u.achievements = d.get('achievements')
    u.experience = d.get('experience')
    u.requirements = message.text
    session.add(u)
    session.commit()
    await message.answer(make_user_message(u))
    await state.reset_state()


@dp.message_handler(lambda message: message.text == texts['edit_btn'], state='*')
async def edit(message: types.Message, state: FSMContext):
    await message.answer(texts['ask_name'])
    await Form.name.set()


@dp.message_handler(lambda message: message.text == texts['view_users_btn'], state='*')
async def edit(message: types.Message, state: FSMContext):
    user = get_relevant_user(message.from_user.id)
    print(user)
    if user:
        await message.answer(make_user_message(user), reply_markup=get_user_keyboard(user.id))
    else:
        await message.answer(texts['no_users'])


@dp.callback_query_handler(Text(startswith='contact_'))
async def show_contacts(call: types.CallbackQuery, state: FSMContext):
    u = session.query(User).get(int(call.data.replace('contact_', '')))
    await call.answer()
    await call.message.answer(f'Аккаунт пользователя — @{u.username}')


@dp.callback_query_handler(Text(startswith='pass'))
async def pass_user(call: types.CallbackQuery, state: FSMContext):
    user = get_relevant_user(call.from_user.id)
    if user:
        await call.message.answer(make_user_message(user), reply_markup=get_user_keyboard(user.id))
    else:
        await call.message.answer(texts['no_users'])


@dp.message_handler(Text(equals='photo'), content_types=types.ContentType.all())
async def get_photo_id(message: types.Message, state: FSMContext):
    print(message)
    await message.answer(message.photo[-1].file_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

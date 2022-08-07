import json
import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import db_session

TOKEN = '1084737102:AAGSfZBZ_KVb_BAW2QyMHPt0a2PmopsOWuM'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

bot = Bot(token=TOKEN, parse_mode='html')
# Диспетчер для бота
storage = MemoryStorage()  # TODO: поменять строрадж
dp = Dispatcher(bot, storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO, filename='logging.txt')
logging.basicConfig(level=logging.DEBUG)

with open('texts.json', encoding='utf-8') as texts_file:
    texts = json.load(texts_file)

db_session.global_init("db/main.db")
session = db_session.create_session()
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

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

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
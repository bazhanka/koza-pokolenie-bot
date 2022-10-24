import logging
import os
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = os.getenv('BOT_TOKEN')
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


@dp.callback_query_handler(text="unn")
async def unn(call: types.CallbackQuery):
    await call.message.answer("Обратись в профком студентов ННГУ или по телефону")


@dp.callback_query_handler(text="ngtu")
async def ngtu(call: types.CallbackQuery):
    await call.message.answer("Обратись в профком студентов НГТУ или по телефону")


@dp.callback_query_handler(text="no_uni")
async def no_uni(call: types.CallbackQuery):
    await call.message.answer("Обратись в Дом Актера (ул. Пискунова, д.10)\nили по телефону +79043997898")


uni_kb = InlineKeyboardMarkup(row_width=1)
unnButton = InlineKeyboardButton(text="Я учусь в ННГУ им. Лобачевского", callback_data='unn')
ngtuButton = InlineKeyboardButton(text='Я учусь в НГТУ им. Алексеева', callback_data='ngtu')
noneButton = InlineKeyboardButton(text='Я не учусь ни в одном из этих ВУЗов',  callback_data='no_uni')
uni_kb.add(unnButton, ngtuButton, noneButton)

@dp.callback_query_handler(text="uni")
async def uni(call: types.CallbackQuery):
    await call.message.reply("Выбери один из вариантов:", reply_markup=uni_kb)


@dp.callback_query_handler(text="onoff")
async def onoff(call: types.CallbackQuery):
    await call.message.reply("Выбери один из вариантов:", reply_markup=onoff_kb)

onoff_kb = InlineKeyboardMarkup(row_width=1)
onlineButton = InlineKeyboardButton(text="Я хочу билет онлайн", url='https://angagement.timepad.ru/event/2213874/')
offlineButton = InlineKeyboardButton (text='Я хочу бумажный билет', callback_data="uni")
onoff_kb.add(onlineButton, offlineButton)


async def get_ticket(message: types.Message):
    await message.reply("Выбери один из вариантов", reply_markup=onoff_kb)

urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Расскажу подробнее о фестивале', url='https://vk.com/club202678458')
ticket_Button = InlineKeyboardButton(text='Подарю билет на гала-концерт', callback_data="onoff")
urlkb.add(urlButton, ticket_Button)


@dp.message_handler(commands=['start'])  # Reply on start
async def send_welcome(message: types.Message):
    await message.reply("Привет!\n Я - бот фестиваля Веселая Коза. Поколение Ы.\n Вот что я могу!", reply_markup=urlkb)

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()

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
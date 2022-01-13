import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, admin
import keyboard as kb
import functions as func
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled
from anekdot import ANEKDOT 
import random 


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
connection = sqlite3.connect('data.db')
q = connection.cursor()

class st(StatesGroup):

	item = State()

@dp.message_handler(commands=['start'])

async def start(message: types.Message):

	func.join(chat_id=message.chat.id)
	if message.chat.id == admin:
		await message.answer('Добро пожаловать.', reply_markup=kb.menu)
	else:
		await message.answer('Привет!👋\nЯ-бот анекдот 😜, нажимай на клавиатуру и я скину анекдот.', reply_markup=kb.anek)



@dp.message_handler(content_types=['text'], text='Анекдот')

async def handfler(message: types.Message, state: FSMContext):

	func.join(chat_id=message.chat.id)
	await message.answer(random.choice(ANEKDOT))



@dp.message_handler(content_types=['text'], text='👑 Админка')

async def handfler(message: types.Message, state: FSMContext):

	func.join(chat_id=message.chat.id)

	if message.chat.id == admin:
		await message.answer('Добро пожаловать в админ-панель.', reply_markup=kb.adm)



@dp.message_handler(content_types=['text'], text='⏪ Назад')

async def handledr(message: types.Message, state: FSMContext):

	await message.answer('Добро пожаловать, Ублюдок.', reply_markup=kb.menu)




@dp.message_handler(content_types=['text'], text='💬 Рассылка')
async def hangdler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	if message.chat.id == admin:
		await message.answer('Введите текст для рассылки.\n\nДля отмены нажми блять на кнопку ниже', reply_markup=kb.back)
		await st.item.set()

@dp.message_handler(content_types=['text'])


@dp.message_handler(state=st.item)
async def process_name(message: types.Message, state: FSMContext):
	q.execute(f'SELECT user_id FROM users')
	row = q.fetchall()
	connection.commit()
	text = message.text
	if message.text == '⏪ Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		info = row
		await message.answer('Рассылка начата!', reply_markup=kb.adm)
		for i in range(len(info)):
			try:
				await bot.send_message(info[i][0], str(text))
			except:
				pass
		await message.answer('Рассылка завершена!', reply_markup=kb.adm)
		await state.finish()

	await self.reset_state(chat=chat, user=user, with_data=True)
	
executor.start_polling(dp, skip_updates=True)

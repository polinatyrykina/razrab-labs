import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv
import psycopg2
import requests
from datetime import datetime

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_db_connection():
    return psycopg2.connect(
        dbname="razrab-labs",
        user="polina_tyrykina_knowledge_base",
        password="123",
        host="localhost",
        port="5432",
        client_encoding="utf8"
    )

# Состояния FSM
class RegStates(StatesGroup):
    waiting_for_login = State()

class OperationStates(StatesGroup):
    waiting_for_operation_type = State()
    waiting_for_sum = State()
    waiting_for_date = State()

class ViewOperationsStates(StatesGroup):
    waiting_for_currency = State()
    waiting_for_operation_filter = State()

# Проверка регистрации
def is_registered(chat_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE chat_id = %s", (str(chat_id),))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я финансовый бот.\nКоманды:\n/reg — регистрация\n/add_operation — новая операция\n/operations — просмотр операций")

# Команда /reg
@dp.message(Command("reg"))
async def cmd_reg(message: types.Message, state: FSMContext):
    if is_registered(message.chat.id):
        await message.answer("Вы уже зарегистрированы.")
        return
    await message.answer("Введите логин:")
    await state.set_state(RegStates.waiting_for_login)

@dp.message(RegStates.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (chat_id, name) VALUES (%s, %s)", (str(message.chat.id), message.text))
    conn.commit()
    cur.close()
    conn.close()
    await message.answer("Регистрация успешна.")
    await state.clear()

# Команда /add_operation
@dp.message(Command("add_operation"))
async def cmd_add_operation(message: types.Message, state: FSMContext):
    if not is_registered(message.chat.id):
        await message.answer("Сначала зарегистрируйтесь с помощью /reg")
        return

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="РАСХОД"), KeyboardButton(text="ДОХОД")]
    ], resize_keyboard=True)

    await message.answer("Выберите тип операции:", reply_markup=keyboard)
    await state.set_state(OperationStates.waiting_for_operation_type)

@dp.message(OperationStates.waiting_for_operation_type)
async def process_operation_type(message: types.Message, state: FSMContext):
    if message.text not in ["РАСХОД", "ДОХОД"]:
        await message.answer("Выберите кнопку.")
        return
    await state.update_data(type_operation=message.text)
    await message.answer("Введите сумму операции (в рублях):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OperationStates.waiting_for_sum)

@dp.message(OperationStates.waiting_for_sum)
async def process_operation_sum(message: types.Message, state: FSMContext):
    try:
        sum_value = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return
    await state.update_data(sum=sum_value)
    await message.answer("Введите дату операции (ГГГГ-ММ-ДД):")
    await state.set_state(OperationStates.waiting_for_date)

@dp.message(OperationStates.waiting_for_date)
async def process_operation_date(message: types.Message, state: FSMContext):
    try:
        date_value = datetime.strptime(message.text, "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Формат даты: ГГГГ-ММ-ДД.")
        return

    data = await state.get_data()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO operations (date, sum, chat_id, type_operation)
        VALUES (%s, %s, %s, %s)
    """, (date_value, data["sum"], str(message.chat.id), data["type_operation"]))
    conn.commit()
    cur.close()
    conn.close()

    await message.answer("Операция успешно добавлена.")
    await state.clear()

# Команда /operations
@dp.message(Command("operations"))
async def cmd_operations(message: types.Message, state: FSMContext):
    if not is_registered(message.chat.id):
        await message.answer("Сначала зарегистрируйтесь с помощью /reg")
        return

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="RUB"), KeyboardButton(text="USD"), KeyboardButton(text="EUR")]
    ], resize_keyboard=True)

    await message.answer("Выберите валюту:", reply_markup=keyboard)
    await state.set_state(ViewOperationsStates.waiting_for_currency)

@dp.message(ViewOperationsStates.waiting_for_currency)
async def process_currency(message: types.Message, state: FSMContext):
    if message.text not in ["RUB", "USD", "EUR"]:
        await message.answer("Выберите валюту из кнопок.")
        return
    await state.update_data(currency=message.text)

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="РАСХОДНЫЕ ОПЕРАЦИИ"), KeyboardButton(text="ДОХОДНЫЕ ОПЕРАЦИИ")],
        [KeyboardButton(text="ВСЕ")]
    ], resize_keyboard=True)

    await message.answer("Какие операции вывести?", reply_markup=keyboard)
    await state.set_state(ViewOperationsStates.waiting_for_operation_filter)

@dp.message(ViewOperationsStates.waiting_for_operation_filter)
async def process_operation_filter(message: types.Message, state: FSMContext):
    if message.text not in ["РАСХОДНЫЕ ОПЕРАЦИИ", "ДОХОДНЫЕ ОПЕРАЦИИ", "ВСЕ"]:
        await message.answer("Выберите вариант.")
        return

    data = await state.get_data()
    currency = data["currency"]
    filter_type = message.text

    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT date, sum, type_operation FROM operations WHERE chat_id = %s"
    params = [str(message.chat.id)]

    type_mapping = {
        "РАСХОДНЫЕ ОПЕРАЦИИ": "РАСХОД",
        "ДОХОДНЫЕ ОПЕРАЦИИ": "ДОХОД"
}

    if filter_type != "ВСЕ":
        query += " AND type_operation = %s"
        params.append(type_mapping.get(filter_type))


    cur.execute(query, tuple(params))
    operations = cur.fetchall()
    cur.close()
    conn.close()

    if currency != "RUB":
        try:
            response = requests.get(f"http://localhost:5000/rate?currency={currency}")
            response.raise_for_status()
            rate = response.json()["rate"]
        except:
            await message.answer("Ошибка получения курса.")
            await state.clear()
            return
    else:
        rate = 1

    if not operations:
        await message.answer("Операций не найдено.")
    else:
        response = "Ваши операции:\n"
        for op in operations:
            converted_sum = float(op[1]) / rate
            response += f"{op[0]} | {op[2]} | {converted_sum:.2f} {currency}\n"
        await message.answer(response)

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

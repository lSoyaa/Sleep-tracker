import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
from db import get_last
from db import insert_sessions
from db import stat
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
state = {}

def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💤 Start sleep", callback_data="sleep"),
            InlineKeyboardButton(text="☀️ Wake up", callback_data="wake"),
        ],
        [
            InlineKeyboardButton(text="📝 Add note", callback_data="note"),
        ],
        [
            InlineKeyboardButton(text="📊 Stats", callback_data="stat"),
            InlineKeyboardButton(text="🕒 Last", callback_data="last"),
        ],
    ])

def start_sleep(state, user_id):
    if user_id not in state:
        state[user_id] = {"sleep_start": None, "note": None}

    if state[user_id]["sleep_start"] is not None:
        return "You're sleep now" 
    else:
        state[user_id]["sleep_start"] = datetime.now()
        return "Sleep started"

def wake_up(state, user_id):
    if user_id not in state or state[user_id]["sleep_start"] is None:
        return "You haven't started sleeping yet"
    
    note = state[user_id]["note"]
    start = state[user_id]["sleep_start"]
    end = datetime.now()

    delta = end - start
    hours = delta.seconds // 3600
    minutes =  (delta.seconds % 3600) // 60

    start_str = start.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end.strftime("%Y-%m-%d %H:%M:%S")
    duration_minutes = delta.seconds // 60

    insert_sessions(user_id, start_str, end_str, duration_minutes, note)
    state[user_id]["sleep_start"] = None
    state[user_id]["note"] = None

    message = f"Your sleep time {hours}h {minutes}m ☀️"

    if note:
        message += f"\nNote: {note} 📝"

    return message
    

@dp.message(Command("note"))
async def cmd_note(message: Message):
    user_id = message.from_user.id
    if user_id not in state:
        state[user_id] = {"sleep_start": None, "note": None}
    text = message.text.replace("/note", "", 1).strip()

    if not text:
        state[user_id]["waiting_note"] = True
        await message.answer("Write your note in the next message 📝", reply_markup=main_keyboard())
        return
    else:
        state[user_id]["note"] = text
        state[user_id]["waiting_note"] = False
        await message.answer("Note saved 📝", reply_markup=main_keyboard())

@dp.message(Command("last"))
async def cmd_last(message: Message):
    user_id = message.from_user.id
    last = get_last(user_id)
    if last is None:
        await message.answer("No data yet")
    else:
        start, end, duration, note = last
        hours = duration // 60
        minutes = duration % 60
        if note:
            await message.answer(f"The last session \nStart: {start} \nEnd: {end} \nDuration: {hours}h {minutes}m \nNote: {note}")
        else:
            await message.answer(f"The last session \nStart: {start} \nEnd: {end} \nDuration: {hours}h {minutes}m")

@dp.message(Command("stat"))
async def cmd_stat(message: Message):
    user_id = message.from_user.id
    result = stat(user_id)
    total, avarage, minimum, maximum = result
    if total == 0:
        await message.answer("No data yet")
    else:
        avarage = int(avarage)
        av_h = avarage // 60
        av_m = avarage % 60
        min_h = minimum // 60
        min_m = minimum % 60
        max_h = maximum // 60
        max_m = maximum % 60
        await message.answer(f"Statistic \nTotal sessions: {total} \nAvarage duration of sleep: {av_h}h {av_m}m \nMinimum duration: {min_h}h {min_m}m \nMaximum duration: {max_h}h {max_m}m")



#cmd command 
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hi! 👋\nUse /sleep to start sleeping and /wake to wake up ☀️",
    reply_markup=main_keyboard()
    )

@dp.message(Command("sleep"))
async def cmd_sleep(message: Message):
    user_id = message.from_user.id
    result = start_sleep(state, user_id)
    await message.answer(result)
    
@dp.message(Command("wake"))
async def cmd_wake(message: Message):
    user_id = message.from_user.id
    result = wake_up(state, user_id)
    await message.answer(result)

#knopki

@dp.callback_query(lambda c: c.data == "sleep")
async def cb_sleep(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = start_sleep(state, user_id)
    await callback.message.answer(result, reply_markup=main_keyboard())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "wake")
async def cb_wake(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = wake_up(state, user_id)
    await callback.message.answer(result, reply_markup=main_keyboard())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "last")
async def cb_last(callback: CallbackQuery):
    user_id = callback.from_user.id
    last = get_last(user_id)

    if last is None:
        await callback.message.answer("No data yet", reply_markup=main_keyboard())
    else:
        start, end, duration, note = last
        hour = duration // 60
        minutes = duration % 60

        text = f"The last session \nStart: {start} \nEnd: {end} \nDuration: {hour}h {minutes}m"
        if note:
            text += f"\nNote: {note} 📝"
        await callback.message.answer(text, reply_markup=main_keyboard())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "stat")
async def cb_stat(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = stat(user_id)
    total, avarage, minimum, maximum = result
    
    if total == 0:
        await callback.message.answer("No data yet", reply_markup=main_keyboard())
    else:
        avarage = int(avarage)
        av_h = avarage // 60
        av_m = avarage % 60
        min_h = minimum // 60
        min_m = minimum % 60
        max_h = maximum // 60
        max_m = maximum % 60

        await callback.message.answer(f"Statistic \nTotal sessions: {total} \nAvarage duration of sleep: {av_h}h {av_m}m \nMinimum duration: {min_h}h {min_m}m \nMaximum duration: {max_h}h {max_m}m", reply_markup=main_keyboard())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "note")
async def cb_note(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in state:
        state[user_id] = {"sleep_start": None, "note": None}
    state[user_id]["waiting_note"] = True

    await callback.message.answer("Write your note in the next message 📝", reply_markup=main_keyboard())
    await callback.answer()

@dp.message()
async def catch_note(message: Message):
    if message.text and message.text.startswith("/"):
        return
    user_id = message.from_user.id

    if user_id not in state:
        return
    if not state[user_id].get("waiting_note"):
        return
    text = message.text.strip()
    if not text:
        await message.answer("Empty note. Try again 📝", reply_markup=main_keyboard())
        return
    state[user_id]["note"] = text
    state[user_id]["waiting_note"] = False
    await message.answer("Note saved 📝", reply_markup=main_keyboard())

    
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
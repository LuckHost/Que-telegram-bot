import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import bot_token
bot = Bot(token=bot_token)

dp = Dispatcher()

users = {}
op = []
informatics = []
vvpd = []

class Dialog(StatesGroup):
    waiting_for_name = State()
    queue_entry = State()
    task_await = State()
    talk = State()

@dp.message(StateFilter(None), Command("start"))
async def start_message(messege: types.Message, state: FSMContext):
    """
    
        Main opening function.
        Asks the username if it is not in dict.
        
    """
    if messege.from_user.id not in users:
        await messege.answer("Напиши имя и фамилию")
        await state.set_state(Dialog.waiting_for_name)
        return
    await messege.answer("C возвращением!")
    await state.set_state(Dialog.task_await)
    
@dp.message(Dialog.task_await)
async def task_await(messege: types.Message, state: FSMContext):
    """
    
    Gives a keayborad with the based commands.
    
    """
    reply_keyboard = [
            [
                KeyboardButton(text="/sign_up"), 
                KeyboardButton(text="/info"),
                KeyboardButton(text="/sign_out")
            ]
            ]
    base_commands_keyboard = ReplyKeyboardMarkup(keyboard=reply_keyboard,
                                                     resize_keyboard=True,
                                                     one_time_keyboard=True)
        
    await messege.answer(text="Выберете опцию...",
                             reply_markup = base_commands_keyboard)
    await state.set_state(None)
    
@dp.message(StateFilter(None), Command("info"))
async def show_base(messege: types.Message, state: FSMContext):
    """
    
    Returns the base of all users to the user.
    
    """
    if len(users) == 0:
        await messege.answer("Список пуст.. Скорее всего сервер перезапускался")
        return
    
    #answer = "Пользователей:\n"
    #for i in users:
    #    answer += f"{users[i]}, \n"
    #
    
    answer = "Информатика:\n"
    for i in informatics:
        answer += f"{users[i]}, \n"
    await messege.answer(answer)
        
    answer = "\nВВПД:\n"
    for i in vvpd:
        answer += f"{users[i]}, \n"
    await messege.answer(answer)
    
    answer = "\nОП:\n"
    for i in op:
        answer += f"{users[i]}, \n"
    await messege.answer(answer)
    
@dp.callback_query(F.data.startswith("que_entry_"))
async def sign_up_function(callback: types.CallbackQuery, state: FSMContext):
    """

    Inline buttons implementation.

    """
    action = callback.data.split("_")[2]
    if action == "inform":
        if callback.from_user.id not in informatics:
            informatics.append(callback.from_user.id)
            await callback.message.answer("Вы записались на инфу")
        else:
            await callback.message.answer("Вы уже записаны на инфу")
            
    elif action == "vvpd":
        if callback.from_user.id not in vvpd:
            vvpd.append(callback.from_user.id)
            await callback.message.answer("Вы записались на на ввпд")
        else:
            await callback.message.answer("Вы уже записаны на ввпд")
            
    elif action == "op":
        if callback.from_user.id not in op:
            op.append(callback.from_user.id)
            await callback.message.answer("Вы записались на на ОП")
        else:
            await callback.message.answer("Вы уже записаны на ОП")
        
            

    await state.set_state(None)
    await callback.answer()
    
@dp.message(StateFilter(None), Command("sign_up"))
async def sign_up_keyboard(messege: types.Message, state: FSMContext):
    """
    
    Message with the inline keyboard
    
    """
    if messege.from_user.id not in users:
        await messege.answer("Тебя нет в базе.. Введи /start")
        return
    await state.set_state(Dialog.queue_entry)
    iform_but = InlineKeyboardButton(text = "Информатика", callback_data="que_entry_inform")
    vvpd_but = InlineKeyboardButton(text = "ВВПД", callback_data="que_entry_vvpd")
    op_but = InlineKeyboardButton(text = "ОП", callback_data="que_entry_op")
    queue_keyboard = InlineKeyboardBuilder().add(iform_but, vvpd_but, op_but)
    await messege.answer("Выбери предмет", reply_markup=queue_keyboard.as_markup())
    
@dp.callback_query(F.data.startswith("que_leave_"))
async def sign_up_function(callback: types.CallbackQuery, state: FSMContext):
    """

    Inline buttons implementation.

    """
    action = callback.data.split("_")[2]
    if action == "inform":
        if callback.from_user.id in informatics:
            informatics.remove(callback.from_user.id)
            await callback.message.answer("Вы покинули очередь на инфу")
        else:
            await callback.message.answer("Вас нет в очереди на инфу")
            
    elif action == "vvpd":
        if callback.from_user.id in vvpd:
            vvpd.remove(callback.from_user.id)
            await callback.message.answer("Вы покинули очередь на ввпд")
        else:
            await callback.message.answer("Вас нет в очереди на ввпд")
            
    elif action == "op":
        if callback.from_user.id in op:
            op.remove(callback.from_user.id)
            await callback.message.answer("Вы покинули очередь на на ОП")
        else:
            await callback.message.answer("Вас нет в очереди на ОП")
        
            

    await state.set_state(None)
    await callback.answer()
    
@dp.message(StateFilter(None), Command("sign_out"))
async def sign_up_keyboard(messege: types.Message, state: FSMContext):
    """
    
    Message with the inline keyboard
    
    """
    if messege.from_user.id not in users:
        await messege.answer("Тебя нет в базе.. Введи /start")
        return
    await state.set_state(Dialog.queue_entry)
    iform_but = InlineKeyboardButton(text = "Информатика", callback_data="que_leave_inform")
    vvpd_but = InlineKeyboardButton(text = "ВВПД", callback_data="que_leave_vvpd")
    op_but = InlineKeyboardButton(text = "ОП", callback_data="que_leave_op")
    queue_keyboard = InlineKeyboardBuilder().add(iform_but, vvpd_but, op_but)
    await messege.answer("Выбери предмет", reply_markup=queue_keyboard.as_markup())

@dp.message(Dialog.waiting_for_name, F.text)
async def import_name(message: types.Message, state: FSMContext):
    """

    Takes the name of user if it is not in base.
    Users base structure: 
    User id : username from message, account username 
    
    """
    await message.answer(f"Добро пожаловать, {message.text}!")
    users.update({message.from_user.id: f"{message.text}, ({message.from_user.full_name})"})
    await state.set_state(Dialog.task_await)
    await task_await(message, state)

@dp.message(F.text)
async def echo_message(message: types.Message, state: FSMContext):
    """
    
    Echo function. 
    Returns the same message that the user sent.
    
    """
    await message.answer(text=message.text)
    await message.answer(f"{message.from_user.id}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
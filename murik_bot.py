import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web  # Добавили для обхода ограничений бесплатного Render

# Токен вашего бота
TOKEN = "9162038190:AAGNlXWfpFeniIZjokfBc1JBUHs5umBv9KY"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class BotStates(StatesGroup):
    choosing_friend = State()
    answering_mode = State()


friends_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="осётр")],
        [KeyboardButton(text="диня")],
        [KeyboardButton(text="димка")]
    ],
    resize_keyboard=True
)


@dp.message(F.text.in_({"/start", "/menu", "меню", "Меню"}))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BotStates.choosing_friend)
    await message.answer(
        "Выбери друга Мурика из меню:\n(Чтобы сменить друга позже, просто напиши слово *меню*)",
        reply_markup=friends_menu,
        parse_mode="Markdown"
    )


@dp.message(BotStates.choosing_friend, F.text.in_({"осётр", "диня", "димка"}))
async def friend_chosen(message: Message, state: FSMContext):
    choice = message.text
    await state.update_data(chosen_friend=choice)
    await state.set_state(BotStates.answering_mode)
    await message.answer(
        f"Вы выбрали: {choice}. Теперь пишите ему что угодно.\n"
        f"Если захотите выбрать другого друга, напишите слово *меню*.",
        parse_mode="Markdown"
    )


@dp.message(BotStates.choosing_friend)
async def wrong_choice(message: Message):
    await message.answer("Кнопку нажми из меню!", reply_markup=friends_menu)


@dp.message(BotStates.answering_mode)
async def echo_friend(message: Message, state: FSMContext):
    user_data = await state.get_data()
    chosen_friend = user_data.get("chosen_friend")

    if chosen_friend == "осётр":
        await message.answer_sticker(sticker="CAACAgIAAxkBAAEILnxq8HPXg616RnUZJKh5L2oW8n1gHQACxH8AAvIAAblJHSv85qCxZmA9BA")
    elif chosen_friend == "диня":
        await message.answer("я ебал твою мать. я все сказал")
    elif chosen_friend == "димка":
        await message.answer("заебала меня хуйня твоя")


# Микро-веб-сервер для заглушки Render
async def handle(request):
    return web.Response(text="Bot is running!")


async def main():
    print("Бот Друзей Мурика успешно обновлен и запущен...")

    # Запускаем фоновый опрос Телеграма
    asyncio.create_task(dp.start_polling(bot))

    # Запускаем веб-сервер на порту, который требует Render
    app = web.Application()
    app.router.add_get('/', handle)

    # Render автоматически передает нужный порт в переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    # Держим бота запущенным бесконечно
    while True:
        await asyncio.sleep(3600)


if __name__ == '__main__':
    asyncio.run(main())

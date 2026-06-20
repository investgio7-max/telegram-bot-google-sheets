import logging
import os
from datetime import datetime
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

from google_sheets import GoogleSheetsManager
from excel_generator import ExcelGenerator

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

google_sheets = GoogleSheetsManager()
excel_generator = ExcelGenerator()


class ClientStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_percentage = State()


def get_main_menu() -> ReplyKeyboardMarkup:
    """Create main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить клиента")],
            [KeyboardButton(text="📊 Скачать Excel")]
        ],
        resize_keyboard=True
    )
    return keyboard


@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Handle /start command."""
    try:
        await message.answer(
            "👋 Добро пожаловать!\n\n"
            "Выберите действие:",
            reply_markup=get_main_menu()
        )
        logger.info(f"User {message.from_user.id} started bot")
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")


@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Handle /help command."""
    try:
        help_text = (
            "📖 <b>Справка по командам:</b>\n\n"
            "/start - Главное меню\n"
            "/help - Эта справка\n\n"
            "<b>Доступные функции:</b>\n"
            "➕ Добавить клиента - Добавить нового клиента в таблицу\n"
            "📊 Скачать Excel - Загрузить Excel-файл с данными"
        )
        await message.answer(help_text, reply_markup=get_main_menu())
        logger.info(f"User {message.from_user.id} requested help")
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await message.answer("❌ Произошла ошибка.")


@dp.message(lambda message: message.text == "➕ Добавить клиента")
async def add_client_start(message: types.Message, state: FSMContext):
    """Start adding new client."""
    try:
        await state.set_state(ClientStates.waiting_for_phone)
        await message.answer(
            "📱 Введите телефон клиента:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отмена")]],
                resize_keyboard=True
            )
        )
        logger.info(f"User {message.from_user.id} started adding client")
    except Exception as e:
        logger.error(f"Error in add_client_start: {e}")
        await message.answer("❌ Произошла ошибка.")


@dp.message(ClientStates.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    """Process phone input."""
    try:
        if message.text == "❌ Отмена":
            await state.clear()
            await message.answer("❌ Отменено.", reply_markup=get_main_menu())
            return

        phone = message.text.strip()

        if not phone or len(phone) < 5:
            await message.answer("⚠️ Пожалуйста, введите корректный телефон:")
            return

        await state.update_data(phone=phone)
        await state.set_state(ClientStates.waiting_for_email)
        await message.answer("📧 Введите email клиента:")
        logger.info(f"User {message.from_user.id} entered phone: {phone}")
    except Exception as e:
        logger.error(f"Error in process_phone: {e}")
        await message.answer("❌ Произошла ошибка при обработке телефона.")


@dp.message(ClientStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    """Process email input."""
    try:
        if message.text == "❌ Отмена":
            await state.clear()
            await message.answer("❌ Отменено.", reply_markup=get_main_menu())
            return

        email = message.text.strip()

        if "@" not in email or "." not in email:
            await message.answer("⚠️ Пожалуйста, введите корректный email:")
            return

        await state.update_data(email=email)
        await state.set_state(ClientStates.waiting_for_percentage)
        await message.answer("📊 Введите процент (число):")
        logger.info(f"User {message.from_user.id} entered email: {email}")
    except Exception as e:
        logger.error(f"Error in process_email: {e}")
        await message.answer("❌ Произошла ошибка при обработке email.")


@dp.message(ClientStates.waiting_for_percentage)
async def process_percentage(message: types.Message, state: FSMContext):
    """Process percentage input and save to Google Sheets."""
    try:
        if message.text == "❌ Отмена":
            await state.clear()
            await message.answer("❌ Отменено.", reply_markup=get_main_menu())
            return

        percentage_text = message.text.strip()

        try:
            percentage = float(percentage_text)
            if percentage < 0 or percentage > 100:
                await message.answer("⚠️ Процент должен быть от 0 до 100:")
                return
        except ValueError:
            await message.answer("⚠️ Пожалуйста, введите число:")
            return

        data = await state.get_data()
        phone = data['phone']
        email = data['email']

        await state.clear()

        await message.answer("⏳ Сохраняю данные...", reply_markup=get_main_menu())

        date = datetime.now().strftime("%d.%m.%Y %H:%M")
        success = await google_sheets.add_client(
            date=date,
            phone=phone,
            email=email,
            percentage=percentage
        )

        if success:
            await message.answer(
                f"✅ <b>Клиент успешно добавлен!</b>\n\n"
                f"📱 Телефон: {phone}\n"
                f"📧 Email: {email}\n"
                f"📊 Процент: {percentage}%\n"
                f"📅 Дата: {date}",
                reply_markup=get_main_menu()
            )
            logger.info(f"User {message.from_user.id} added client: {phone}, {email}, {percentage}%")
        else:
            await message.answer(
                "❌ Ошибка при сохранении в Google Sheets.\n"
                "Проверьте логи и настройки доступа.",
                reply_markup=get_main_menu()
            )
            logger.error(f"Failed to add client for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in process_percentage: {e}")
        await state.clear()
        await message.answer(
            f"❌ Произошла ошибка: {str(e)}",
            reply_markup=get_main_menu()
        )


@dp.message(lambda message: message.text == "📊 Скачать Excel")
async def download_excel(message: types.Message):
    """Download data as Excel file."""
    try:
        await message.answer("⏳ Загружаю данные и готовлю файл...")

        data = await google_sheets.get_all_data()

        if not data:
            await message.answer(
                "📭 В таблице нет данных.",
                reply_markup=get_main_menu()
            )
            logger.info(f"User {message.from_user.id} tried to download empty data")
            return

        file_path = await excel_generator.create_excel(data)

        if not file_path or not os.path.exists(file_path):
            await message.answer(
                "❌ Ошибка при создании Excel файла.",
                reply_markup=get_main_menu()
            )
            logger.error(f"Failed to create Excel file for user {message.from_user.id}")
            return

        with open(file_path, 'rb') as file:
            await bot.send_document(
                chat_id=message.chat.id,
                document=file,
                caption="📊 Данные клиентов"
            )

        os.remove(file_path)
        logger.info(f"User {message.from_user.id} downloaded Excel file")

        await message.answer(
            "✅ Файл отправлен!",
            reply_markup=get_main_menu()
        )
    except Exception as e:
        logger.error(f"Error in download_excel: {e}")
        await message.answer(
            f"❌ Ошибка при загрузке: {str(e)}",
            reply_markup=get_main_menu()
        )


@dp.message()
async def echo_handler(message: types.Message, state: FSMContext):
    """Handle any other message."""
    try:
        current_state = await state.get_state()

        if current_state:
            await message.answer("⚠️ Пожалуйста, используйте кнопки меню или завершите текущее действие.")
        else:
            await message.answer(
                "❓ Неизвестная команда.\n\n"
                "Используйте меню для выбора действия.",
                reply_markup=get_main_menu()
            )
    except Exception as e:
        logger.error(f"Error in echo_handler: {e}")
        await message.answer("❌ Произошла ошибка.")


async def main():
    """Start the bot."""
    try:
        logger.info("Bot starting...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")

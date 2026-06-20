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
    waiting_for_client_data = State()
    waiting_for_search_email = State()


def parse_client_data(text: str) -> tuple[bool, str, str, float]:
    """
    Parse client data from message in format:
    email
    phone
    percentage

    Returns:
        Tuple of (success, email, phone, percentage)
    """
    lines = text.strip().split('\n')

    if len(lines) != 3:
        return False, '', '', 0.0

    email = lines[0].strip()
    phone = lines[1].strip()
    percentage_text = lines[2].strip()

    # Validate email
    if '@' not in email or '.' not in email:
        return False, '', '', 0.0

    # Validate phone (not empty)
    if not phone:
        return False, '', '', 0.0

    # Parse percentage - handle various formats: 3%, 3, 3.0%, 3,0%
    try:
        # Remove % and replace comma with dot
        percentage_text = percentage_text.rstrip('%').replace(',', '.')
        percentage = float(percentage_text)

        if percentage < 0 or percentage > 100:
            return False, '', '', 0.0

        return True, email, phone, percentage
    except ValueError:
        return False, '', '', 0.0


def get_main_menu() -> ReplyKeyboardMarkup:
    """Create main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить клиента")],
            [KeyboardButton(text="🔍 Найти клиента")],
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
        await state.set_state(ClientStates.waiting_for_client_data)
        await message.answer(
            "📋 Отправьте данные в формате:\n\n"
            "<code>email\n"
            "телефон\n"
            "процент</code>\n\n"
            "<b>Пример:</b>\n"
            "<code>user@gmail.com\n"
            "+33 7 59 87 03 18\n"
            "3%</code>\n\n"
            "Процент можно указать как: 3%, 3, 3.0%, 3,0%",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отмена")]],
                resize_keyboard=True
            ),
            parse_mode=ParseMode.HTML
        )
        logger.info(f"User {message.from_user.id} started adding client")
    except Exception as e:
        logger.error(f"Error in add_client_start: {e}")
        await message.answer("❌ Произошла ошибка.")


@dp.message(ClientStates.waiting_for_client_data)
async def process_client_data(message: types.Message, state: FSMContext):
    """Process client data input."""
    try:
        if message.text == "❌ Отмена":
            await state.clear()
            await message.answer("❌ Отменено.", reply_markup=get_main_menu())
            return

        # Parse input
        success, email, phone, percentage = parse_client_data(message.text)

        if not success:
            await message.answer(
                "❌ Неверный формат.\n\n"
                "Отправьте данные в формате:\n\n"
                "<code>email\n"
                "телефон\n"
                "процент</code>\n\n"
                "<b>Пример:</b>\n"
                "<code>user@gmail.com\n"
                "+33 7 59 87 03 18\n"
                "3%</code>",
                parse_mode=ParseMode.HTML
            )
            return

        await state.clear()

        await message.answer("⏳ Сохраняю данные...", reply_markup=get_main_menu())

        success, message_type, existing_record = await google_sheets.add_client(
            phone=phone,
            email=email,
            percentage=percentage
        )

        if success:
            # Get the added client info
            client = await google_sheets.find_client_by_email(email)
            if client:
                await message.answer(
                    f"✅ <b>Пользователь успешно добавлен.</b>\n\n"
                    f"🆔 ID: {client.get('ID', 'N/A')}\n"
                    f"📧 Email: {client.get('Email', 'N/A')}\n"
                    f"📱 Телефон: {client.get('Телефон', 'N/A')}\n"
                    f"📊 Процент: {client.get('Процент', 'N/A')}%\n"
                    f"📅 Дата регистрации: {client.get('Дата регистрации', 'N/A')}",
                    reply_markup=get_main_menu()
                )
            else:
                await message.answer(
                    f"✅ <b>Пользователь успешно добавлен.</b>\n\n"
                    f"📧 Email: {email}\n"
                    f"📱 Телефон: {phone}\n"
                    f"📊 Процент: {percentage}%",
                    reply_markup=get_main_menu()
                )
            logger.info(f"User {message.from_user.id} added client: {email}, {phone}, {percentage}%")
        elif message_type == "exists":
            await message.answer(
                f"⚠️ <b>Пользователь с таким Email уже зарегистрирован.</b>\n\n"
                f"📅 Дата регистрации: {existing_record.get('Дата регистрации', 'N/A')}\n"
                f"📱 Телефон: {existing_record.get('Телефон', 'N/A')}\n"
                f"📊 Процент: {existing_record.get('Процент', 'N/A')}%",
                reply_markup=get_main_menu()
            )
            logger.info(f"User {message.from_user.id} tried to add existing email: {email}")
        else:
            await message.answer(
                "❌ Ошибка при сохранении в Google Sheets.\n"
                "Проверьте логи и настройки доступа.",
                reply_markup=get_main_menu()
            )
            logger.error(f"Failed to add client for user {message.from_user.id}: {message_type}")
    except Exception as e:
        logger.error(f"Error in process_client_data: {e}")
        await state.clear()
        await message.answer(
            f"❌ Произошла ошибка: {str(e)}",
            reply_markup=get_main_menu()
        )


@dp.message(lambda message: message.text == "🔍 Найти клиента")
async def search_client_start(message: types.Message, state: FSMContext):
    """Start searching for client by email."""
    try:
        await state.set_state(ClientStates.waiting_for_search_email)
        await message.answer(
            "📧 Введите Email клиента для поиска:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отмена")]],
                resize_keyboard=True
            )
        )
        logger.info(f"User {message.from_user.id} started searching client")
    except Exception as e:
        logger.error(f"Error in search_client_start: {e}")
        await message.answer("❌ Произошла ошибка.", reply_markup=get_main_menu())


@dp.message(ClientStates.waiting_for_search_email)
async def process_search_email(message: types.Message, state: FSMContext):
    """Process search email input."""
    try:
        if message.text == "❌ Отмена":
            await state.clear()
            await message.answer("❌ Отменено.", reply_markup=get_main_menu())
            return

        email = message.text.strip()

        if "@" not in email or "." not in email:
            await message.answer("⚠️ Пожалуйста, введите корректный email:")
            return

        await state.clear()

        await message.answer("⏳ Ищу клиента...", reply_markup=get_main_menu())

        client = await google_sheets.find_client_by_email(email)

        if client:
            await message.answer(
                f"✅ <b>Клиент найден!</b>\n\n"
                f"🆔 ID: {client.get('ID', 'N/A')}\n"
                f"📅 Дата регистрации: {client.get('Дата регистрации', 'N/A')}\n"
                f"📱 Телефон: {client.get('Телефон', 'N/A')}\n"
                f"📧 Email: {client.get('Email', 'N/A')}\n"
                f"📊 Процент: {client.get('Процент', 'N/A')}%",
                reply_markup=get_main_menu()
            )
            logger.info(f"User {message.from_user.id} found client: {email}")
        else:
            await message.answer(
                f"❌ Клиент с email <b>{email}</b> не найден.",
                reply_markup=get_main_menu()
            )
            logger.info(f"User {message.from_user.id} searched for non-existent email: {email}")

    except Exception as e:
        logger.error(f"Error in process_search_email: {e}")
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

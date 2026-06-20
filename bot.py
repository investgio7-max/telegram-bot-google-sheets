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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.dispatcher.middlewares.base import BaseMiddleware
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

ACCESS_PASSWORD = os.getenv('ACCESS_PASSWORD', 'password123')

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class AuthorizationMiddleware(BaseMiddleware):
    """Middleware to check user authorization."""

    async def __call__(self, handler, event: types.Message, data):
        # Skip password state - it's handled separately
        if hasattr(event, "text") and event.text == "❌ Отмена":
            return await handler(event, data)

        # Allow /start command without authorization check
        if hasattr(event, "text") and event.text.startswith("/start"):
            return await handler(event, data)

        # Get state from data
        state = data.get("state")

        # Allow password input when waiting for password
        if state:
            current_state = await state.get_state()
            if current_state == ClientStates.waiting_for_password:
                return await handler(event, data)

        # Check if user is authorized for other commands
        user_id = event.from_user.id
        is_authorized = await check_authorization(user_id)

        if not is_authorized:
            await event.answer(
                "❌ Доступ запрещён.\n\n🔐 Введите пароль доступа.",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="❌ Отмена")]],
                    resize_keyboard=True
                )
            )
            logger.warning(f"Unauthorized access attempt by user {user_id}")
            return

        return await handler(event, data)


# Add middleware
dp.message.middleware(AuthorizationMiddleware())

google_sheets = GoogleSheetsManager()
excel_generator = ExcelGenerator()


class ClientStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_client_data = State()
    waiting_for_search_email = State()
    waiting_for_search_agent = State()


async def log_action(user_id: int, username: str, action: str) -> None:
    """Log user action."""
    try:
        await google_sheets.add_log(user_id, username or "unknown", action)
    except Exception as e:
        logger.error(f"Error logging action: {e}")


async def check_authorization(user_id: int) -> bool:
    """Check if user is authorized."""
    try:
        return await google_sheets.is_user_authorized(user_id)
    except Exception as e:
        logger.error(f"Error checking authorization: {e}")
        return False


def parse_user_data(text: str) -> tuple[bool, str, str, float, str]:
    """
    Parse user data from message in format:
    email
    phone
    percentage
    [agent_email]  (optional)

    Returns:
        Tuple of (success, email, phone, percentage, agent_email)
    """
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

    if len(lines) < 3 or len(lines) > 4:
        return False, '', '', 0.0, ''

    email = lines[0].strip()
    phone = lines[1].strip()
    percentage_text = lines[2].strip()
    agent_email = lines[3].strip() if len(lines) == 4 else ''

    # Validate email
    if '@' not in email or '.' not in email:
        return False, '', '', 0.0, ''

    # Validate phone (not empty)
    if not phone:
        return False, '', '', 0.0, ''

    # Parse percentage - handle various formats: 3%, 3, 3.0%, 3,0%
    try:
        percentage_text = percentage_text.rstrip('%').replace(',', '.')
        percentage = float(percentage_text)

        if percentage < 0 or percentage > 100:
            return False, '', '', 0.0, ''
    except ValueError:
        return False, '', '', 0.0, ''

    return True, email, phone, percentage, agent_email


def get_main_menu() -> ReplyKeyboardMarkup:
    """Create main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить пользователя")],
            [KeyboardButton(text="🔍 Найти пользователя")],
            [KeyboardButton(text="📊 Структура")],
            [KeyboardButton(text="📥 Скачать Excel")]
        ],
        resize_keyboard=True
    )
    return keyboard


@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    """Handle /start command."""
    try:
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name

        # Check if user is authorized
        is_authorized = await check_authorization(user_id)

        if is_authorized:
            await message.answer(
                "👋 Добро пожаловать!\n\n"
                "Выберите действие:",
                reply_markup=get_main_menu()
            )
            await log_action(user_id, username, "Вход в систему")
            logger.info(f"User {user_id} started bot (authorized)")
        else:
            # Request password
            await state.set_state(ClientStates.waiting_for_password)
            await message.answer(
                "🔐 Введите пароль доступа.",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="❌ Отмена")]],
                    resize_keyboard=True
                )
            )
            logger.info(f"User {user_id} requires password")

    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")


@dp.message(ClientStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    """Process password input."""
    try:
        if message.text == "❌ Отмена":
            await state.clear()
            await message.answer("❌ Отменено.")
            return

        if message.text == ACCESS_PASSWORD:
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name

            # Add user to authorized list
            await google_sheets.add_authorized_user(user_id, username)
            await state.clear()

            await message.answer(
                "✅ Доступ разрешён!\n\n"
                "Добро пожаловать!\n\n"
                "Выберите действие:",
                reply_markup=get_main_menu()
            )
            await log_action(user_id, username, "Успешная авторизация")
            logger.info(f"User {user_id} authorized successfully")
        else:
            await message.answer("❌ Неверный пароль. Попробуйте снова.\n\n🔐 Введите пароль доступа.")
            logger.warning(f"Failed authorization attempt for user {message.from_user.id}")

    except Exception as e:
        logger.error(f"Error in process_password: {e}")
        await message.answer("❌ Произошла ошибка.")


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


@dp.message(lambda message: message.text == "➕ Добавить пользователя")
async def add_user_start(message: types.Message, state: FSMContext):
    """Start adding new user."""
    try:
        await state.set_state(ClientStates.waiting_for_client_data)
        await message.answer(
            "📋 Отправьте данные в формате:\n\n"
            "<b>Без родителя:</b>\n"
            "<code>email\n"
            "телефон\n"
            "процент</code>\n\n"
            "<b>С родителем:</b>\n"
            "<code>email\n"
            "телефон\n"
            "процент\n"
            "email_родителя</code>\n\n"
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
        logger.info(f"User {message.from_user.id} started adding user")
    except Exception as e:
        logger.error(f"Error in add_user_start: {e}")
        await message.answer("❌ Произошла ошибка.")


@dp.message(ClientStates.waiting_for_client_data)
async def process_user_data(message: types.Message, state: FSMContext):
    """Process user data input."""
    try:
        if message.text == "❌ Отмена":
            await state.clear()
            await message.answer("❌ Отменено.", reply_markup=get_main_menu())
            return

        # Parse input
        success, email, phone, percentage, agent_email = parse_user_data(message.text)

        if not success:
            await message.answer(
                "❌ Неверный формат.\n\n"
                "Без агента:\n"
                "<code>email\n"
                "телефон\n"
                "процент</code>\n\n"
                "С агентом:\n"
                "<code>email\n"
                "телефон\n"
                "процент\n"
                "email_агента</code>",
                parse_mode=ParseMode.HTML
            )
            return

        await state.clear()

        await message.answer("⏳ Сохраняю данные...", reply_markup=get_main_menu())

        success, message_type, existing_record = await google_sheets.add_user(
            phone=phone,
            email=email,
            percentage=percentage,
            agent_email=agent_email
        )

        if success:
            # Get the added user info
            record = await google_sheets.find_user_by_email(email)
            if record:
                agent_info = f"\n👤 Агент: {record.get('Агент', 'нет')}" if record.get('Агент') else "\n👤 Агент: нет"

                await message.answer(
                    f"✅ <b>Пользователь успешно добавлен.</b>\n\n"
                    f"🆔 ID: {record.get('ID', 'N/A')}\n"
                    f"📧 Email: {record.get('Email', 'N/A')}\n"
                    f"📱 Телефон: {record.get('Телефон', 'N/A')}\n"
                    f"📊 Процент: {record.get('Процент', 'N/A')}%"
                    f"{agent_info}\n"
                    f"📅 Дата регистрации: {record.get('Дата регистрации', 'N/A')}",
                    reply_markup=get_main_menu()
                )
            logger.info(f"User {message.from_user.id} added: {email}")
        elif message_type == "exists":
            await message.answer(
                f"⚠️ <b>Email уже зарегистрирован.</b>\n\n"
                f"📅 Дата регистрации: {existing_record.get('Дата регистрации', 'N/A')}\n"
                f"📱 Телефон: {existing_record.get('Телефон', 'N/A')}\n"
                f"📊 Процент: {existing_record.get('Процент', 'N/A')}%",
                reply_markup=get_main_menu()
            )
        elif message_type == "agent_not_found":
            await message.answer(
                f"❌ <b>Указанный агент не существует.</b>\n\n"
                f"Email агента: {agent_email}",
                reply_markup=get_main_menu()
            )
        else:
            await message.answer(
                "❌ Ошибка при сохранении в Google Sheets.\n"
                f"Детали: {message_type}",
                reply_markup=get_main_menu()
            )
            logger.error(f"Failed to add for user {message.from_user.id}: {message_type}")
    except Exception as e:
        logger.error(f"Error in process_user_data: {e}")
        await state.clear()
        await message.answer(
            f"❌ Произошла ошибка: {str(e)}",
            reply_markup=get_main_menu()
        )


@dp.message(lambda message: message.text == "🔍 Найти пользователя")
async def search_user_start(message: types.Message, state: FSMContext):
    """Start searching for user by email."""
    try:
        await state.set_state(ClientStates.waiting_for_search_email)
        await message.answer(
            "📧 Введите Email пользователя для поиска:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отмена")]],
                resize_keyboard=True
            )
        )
        logger.info(f"User {message.from_user.id} started searching user")
    except Exception as e:
        logger.error(f"Error in search_user_start: {e}")
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

        await message.answer("⏳ Ищу пользователя...", reply_markup=get_main_menu())

        user_info = await google_sheets.get_user_info(email)

        if user_info:
            agent_info = f"\n👤 Агент: {user_info.get('Агент', 'нет')}" if user_info.get('Агент') else "\n👤 Агент: нет"

            await message.answer(
                f"✅ <b>Пользователь найден!</b>\n\n"
                f"📧 Email: {user_info.get('Email', 'N/A')}\n"
                f"📱 Телефон: {user_info.get('Телефон', 'N/A')}\n"
                f"📊 Процент: {user_info.get('Процент', 'N/A')}%\n"
                f"📅 Дата регистрации: {user_info.get('Дата регистрации', 'N/A')}\n"
                f"👥 Рефералов: {user_info.get('Количество рефералов', 0)}"
                f"{agent_info}",
                reply_markup=get_main_menu()
            )
            logger.info(f"User {message.from_user.id} found user: {email}")
        else:
            await message.answer(
                f"❌ Пользователь с email <b>{email}</b> не найден.",
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


@dp.message(lambda message: message.text == "📊 Структура")
async def show_structure(message: types.Message, state: FSMContext):
    """Start showing structure by user email."""
    try:
        await state.set_state(ClientStates.waiting_for_search_agent)
        await message.answer(
            "📊 Введите Email пользователя для просмотра его структуры:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отмена")]],
                resize_keyboard=True
            )
        )
        logger.info(f"User {message.from_user.id} started viewing structure")
    except Exception as e:
        logger.error(f"Error in show_structure: {e}")
        await message.answer("❌ Произошла ошибка.", reply_markup=get_main_menu())


@dp.message(ClientStates.waiting_for_search_agent)
async def process_show_structure(message: types.Message, state: FSMContext):
    """Process structure request."""
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

        await message.answer("⏳ Строю структуру...", reply_markup=get_main_menu())

        # Get user tree
        tree = await google_sheets.get_user_tree(email)

        if tree:
            await message.answer(
                f"<b>📊 Структура пользователя:</b>\n\n"
                f"<code>{tree}</code>",
                reply_markup=get_main_menu(),
                parse_mode=ParseMode.HTML
            )
            logger.info(f"User {message.from_user.id} viewed structure for: {email}")
        else:
            await message.answer(
                f"❌ Пользователь с email <b>{email}</b> не найден.",
                reply_markup=get_main_menu()
            )
            logger.info(f"User {message.from_user.id} searched for non-existent user: {email}")

    except Exception as e:
        logger.error(f"Error in process_show_structure: {e}")
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

        try:
            # Use FSInputFile for aiogram 3.x compatibility
            document = FSInputFile(file_path, filename="clients.xlsx")
            await bot.send_document(
                chat_id=message.chat.id,
                document=document,
                caption="📊 Данные клиентов"
            )
            logger.info(f"User {message.from_user.id} downloaded Excel file")
        finally:
            # Clean up temp file
            if os.path.exists(file_path):
                os.remove(file_path)

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

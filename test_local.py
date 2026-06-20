"""
Local testing script to verify bot functionality without running the actual bot.
Useful for debugging and validating configuration.
"""

import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


async def test_environment_variables():
    """Test if environment variables are properly set."""
    logger.info("=" * 50)
    logger.info("Testing Environment Variables")
    logger.info("=" * 50)

    bot_token = os.getenv('BOT_TOKEN')
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    credentials_base64 = os.getenv('CREDENTIALS_BASE64')

    tests_passed = 0
    tests_total = 2

    if bot_token:
        logger.info("✓ BOT_TOKEN is set")
        logger.info(f"  BOT_TOKEN: {bot_token[:10]}..." if len(bot_token) > 10 else f"  BOT_TOKEN: {bot_token}")
        tests_passed += 1
    else:
        logger.error("✗ BOT_TOKEN is not set - add to .env file")

    if spreadsheet_id:
        logger.info("✓ SPREADSHEET_ID is set")
        logger.info(f"  SPREADSHEET_ID: {spreadsheet_id}")
        tests_passed += 1
    else:
        logger.error("✗ SPREADSHEET_ID is not set - add to .env file")

    if credentials_base64:
        logger.info("✓ CREDENTIALS_BASE64 is set (from environment)")
        logger.info(f"  Length: {len(credentials_base64)} characters")
    else:
        logger.warning("⚠ CREDENTIALS_BASE64 not set - will try to use credentials.json file")

    logger.info(f"\nEnvironment Variables: {tests_passed}/{tests_total} passed\n")
    return tests_passed == tests_total


async def test_credentials_file():
    """Test if credentials.json file exists and is valid."""
    logger.info("=" * 50)
    logger.info("Testing Credentials File")
    logger.info("=" * 50)

    credentials_file = 'credentials.json'

    if not os.path.exists(credentials_file):
        logger.warning(f"⚠ {credentials_file} not found in current directory")
        logger.info("  This is OK if using CREDENTIALS_BASE64 environment variable")
        return True

    logger.info(f"✓ {credentials_file} found")

    try:
        import json
        with open(credentials_file, 'r') as f:
            data = json.load(f)
        logger.info("✓ Credentials file is valid JSON")

        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        missing_fields = [f for f in required_fields if f not in data]

        if missing_fields:
            logger.error(f"✗ Missing required fields: {', '.join(missing_fields)}")
            return False

        logger.info(f"✓ All required fields present")
        logger.info(f"  Type: {data.get('type')}")
        logger.info(f"  Project: {data.get('project_id')}")
        logger.info(f"  Client Email: {data.get('client_email')}")

        return True

    except json.JSONDecodeError as e:
        logger.error(f"✗ Invalid JSON in credentials file: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Error reading credentials file: {e}")
        return False


async def test_google_sheets_connection():
    """Test connection to Google Sheets."""
    logger.info("=" * 50)
    logger.info("Testing Google Sheets Connection")
    logger.info("=" * 50)

    try:
        from google_sheets import GoogleSheetsManager

        sheets = GoogleSheetsManager()

        if sheets.client is None:
            logger.error("✗ Failed to initialize Google Sheets")
            return False

        if sheets.spreadsheet is None:
            logger.error("✗ Failed to open spreadsheet")
            return False

        if sheets.worksheet is None:
            logger.error("✗ Failed to access worksheet")
            return False

        logger.info("✓ Google Sheets connection successful")
        logger.info(f"  Spreadsheet: {sheets.spreadsheet.title}")
        logger.info(f"  Worksheet: {sheets.worksheet.title}")

        all_data = await sheets.get_all_data()
        logger.info(f"  Records in sheet: {len(all_data)}")

        return True

    except Exception as e:
        logger.error(f"✗ Error connecting to Google Sheets: {e}")
        logger.info("  Check that:")
        logger.info("  1. credentials.json or CREDENTIALS_BASE64 is valid")
        logger.info("  2. SPREADSHEET_ID is correct")
        logger.info("  3. Service account has access to the sheet")
        return False


async def test_excel_generator():
    """Test Excel file generation."""
    logger.info("=" * 50)
    logger.info("Testing Excel Generator")
    logger.info("=" * 50)

    try:
        from excel_generator import ExcelGenerator

        generator = ExcelGenerator()

        test_data = [
            {
                'Дата': datetime.now().strftime("%d.%m.%Y %H:%M"),
                'Телефон': '+7 (123) 456-78-90',
                'Email': 'test@example.com',
                'Процент': '25'
            },
            {
                'Дата': datetime.now().strftime("%d.%m.%Y %H:%M"),
                'Телефон': '+7 (987) 654-32-10',
                'Email': 'client@example.com',
                'Процент': '50'
            }
        ]

        filepath = await generator.create_excel(test_data)

        if filepath and os.path.exists(filepath):
            logger.info("✓ Excel file created successfully")
            logger.info(f"  File path: {filepath}")
            logger.info(f"  File size: {os.path.getsize(filepath)} bytes")

            os.remove(filepath)
            logger.info("  Test file removed")

            return True
        else:
            logger.error("✗ Failed to create Excel file")
            return False

    except Exception as e:
        logger.error(f"✗ Error testing Excel generator: {e}")
        return False


async def test_bot_token():
    """Test if bot token is valid (basic check)."""
    logger.info("=" * 50)
    logger.info("Testing Bot Token")
    logger.info("=" * 50)

    bot_token = os.getenv('BOT_TOKEN')

    if not bot_token:
        logger.error("✗ BOT_TOKEN not set")
        return False

    if ':' not in bot_token:
        logger.error("✗ BOT_TOKEN format is invalid (should contain ':')")
        return False

    if len(bot_token) < 20:
        logger.error("✗ BOT_TOKEN is too short")
        return False

    logger.info("✓ BOT_TOKEN format looks valid")
    logger.info(f"  Length: {len(bot_token)} characters")
    logger.info(f"  Format: {'<ID>:<TOKEN>'}")

    try:
        import aiohttp
        from aiogram import Bot

        bot = Bot(token=bot_token)
        session = aiohttp.ClientSession()

        me = await bot.session.get(f"https://api.telegram.org/bot{bot_token}/getMe")

        if me.status == 200:
            logger.info("✓ Bot token is valid and Telegram is reachable")
            data = await me.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                logger.info(f"  Bot name: {bot_info.get('first_name')}")
                logger.info(f"  Bot username: @{bot_info.get('username')}")
            return True
        else:
            logger.error(f"✗ Telegram API returned status {me.status}")
            return False

    except Exception as e:
        logger.error(f"✗ Error validating bot token: {e}")
        logger.info("  This might indicate internet connectivity issues")
        return False


async def run_all_tests():
    """Run all tests and provide summary."""
    logger.info("\n")
    logger.info("╔" + "=" * 48 + "╗")
    logger.info("║" + " " * 10 + "TELEGRAM BOT LOCAL TESTS" + " " * 14 + "║")
    logger.info("╚" + "=" * 48 + "╝")
    logger.info("\n")

    results = {
        "Environment Variables": await test_environment_variables(),
        "Credentials File": await test_credentials_file(),
        "Bot Token": await test_bot_token(),
        "Google Sheets": await test_google_sheets_connection(),
        "Excel Generator": await test_excel_generator(),
    }

    logger.info("\n")
    logger.info("=" * 50)
    logger.info("TEST SUMMARY")
    logger.info("=" * 50)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")

    logger.info(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        logger.info("\n🎉 All tests passed! Bot is ready to run!")
        logger.info("Run 'python bot.py' to start the bot")
        return True
    else:
        logger.warning(f"\n⚠ {total - passed} test(s) failed. See above for details.")
        logger.warning("Fix the issues before running the bot.")
        return False


if __name__ == '__main__':
    try:
        success = asyncio.run(run_all_tests())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n\nTests interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"\n\nUnexpected error: {e}")
        exit(1)

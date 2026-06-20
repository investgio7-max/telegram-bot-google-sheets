import logging
import os
import json
import base64
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def validate_credentials_file(filepath: str = 'credentials.json') -> bool:
    """
    Validate that credentials file exists and is valid JSON.

    Args:
        filepath: Path to credentials file

    Returns:
        True if valid, False otherwise
    """
    try:
        if not os.path.exists(filepath):
            logger.error(f"Credentials file not found: {filepath}")
            return False

        with open(filepath, 'r') as f:
            data = json.load(f)

        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field in credentials: {field}")
                return False

        logger.info("Credentials file is valid")
        return True

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in credentials file: {e}")
        return False
    except Exception as e:
        logger.error(f"Error validating credentials file: {e}")
        return False


def encode_credentials_base64(filepath: str = 'credentials.json') -> Optional[str]:
    """
    Encode credentials file to Base64 for Railway environment variable.

    Args:
        filepath: Path to credentials file

    Returns:
        Base64 encoded string or None if error
    """
    try:
        if not os.path.exists(filepath):
            logger.error(f"Credentials file not found: {filepath}")
            return None

        with open(filepath, 'rb') as f:
            file_content = f.read()

        encoded = base64.b64encode(file_content).decode('utf-8')
        logger.info("Credentials encoded to Base64 successfully")
        return encoded

    except Exception as e:
        logger.error(f"Error encoding credentials: {e}")
        return None


def decode_credentials_base64(base64_str: str, output_filepath: str = 'credentials.json') -> bool:
    """
    Decode Base64 credentials to file.

    Args:
        base64_str: Base64 encoded credentials
        output_filepath: Path where to save decoded credentials

    Returns:
        True if successful, False otherwise
    """
    try:
        decoded = base64.b64decode(base64_str)

        with open(output_filepath, 'wb') as f:
            f.write(decoded)

        logger.info(f"Credentials decoded and saved to {output_filepath}")
        return True

    except Exception as e:
        logger.error(f"Error decoding credentials: {e}")
        return False


def validate_environment_variables() -> bool:
    """
    Validate that all required environment variables are set.

    Returns:
        True if all variables are set, False otherwise
    """
    required_vars = ['BOT_TOKEN', 'SPREADSHEET_ID']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            logger.warning(f"Environment variable not set: {var}")

    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False

    logger.info("All required environment variables are set")
    return True


def print_setup_instructions():
    """Print setup instructions to console."""
    instructions = """
╔════════════════════════════════════════════════════════════════╗
║              Telegram Bot Setup Instructions                   ║
╚════════════════════════════════════════════════════════════════╝

1. Ensure you have the following files:
   ✓ credentials.json (in project root)
   ✓ .env file with BOT_TOKEN and SPREADSHEET_ID

2. Install dependencies:
   pip install -r requirements.txt

3. Run the bot:
   python bot.py

4. To encode credentials for Railway:
   python -c "from utils import encode_credentials_base64; print(encode_credentials_base64())"

5. Then copy the output to CREDENTIALS_BASE64 in Railway environment.

For detailed setup guide, see SETUP_GUIDE.md
    """
    print(instructions)


def get_bot_info() -> Dict[str, str]:
    """
    Get information about bot configuration.

    Returns:
        Dictionary with configuration info
    """
    info = {
        'bot_token_set': bool(os.getenv('BOT_TOKEN')),
        'spreadsheet_id_set': bool(os.getenv('SPREADSHEET_ID')),
        'credentials_file_exists': os.path.exists('credentials.json'),
        'credentials_base64_set': bool(os.getenv('CREDENTIALS_BASE64')),
        'env_file_exists': os.path.exists('.env')
    }
    return info


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    print("\n=== Checking Bot Configuration ===\n")

    info = get_bot_info()
    for key, value in info.items():
        status = "✓" if value else "✗"
        print(f"{status} {key}: {value}")

    print("\n=== Validating Environment Variables ===\n")
    validate_environment_variables()

    print("\n=== Validating Credentials File ===\n")
    if info['credentials_file_exists']:
        validate_credentials_file()

    print_setup_instructions()

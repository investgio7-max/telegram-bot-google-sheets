import logging
import os
from typing import List, Dict, Optional
import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


class GoogleSheetsManager:
    """Manager for Google Sheets operations."""

    def __init__(self, credentials_file: str = 'credentials.json'):
        """
        Initialize Google Sheets Manager.

        Args:
            credentials_file: Path to credentials JSON file
        """
        self.credentials_file = credentials_file
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')

        self._initialize()

    def _initialize(self) -> bool:
        """Initialize Google Sheets connection."""
        try:
            credentials = None

            cred_base64 = os.getenv('CREDENTIALS_BASE64')
            if cred_base64:
                try:
                    import base64
                    import json

                    cred_json = base64.b64decode(cred_base64).decode('utf-8')
                    cred_dict = json.loads(cred_json)
                    credentials = Credentials.from_service_account_info(
                        cred_dict,
                        scopes=SCOPES
                    )
                    logger.info("Using credentials from CREDENTIALS_BASE64 environment variable")
                except Exception as e:
                    logger.error(f"Error decoding CREDENTIALS_BASE64: {e}")

            if not credentials:
                if not os.path.exists(self.credentials_file):
                    logger.warning(
                        f"Credentials file not found: {self.credentials_file}\n"
                        "Please follow the setup instructions in README.md"
                    )
                    return False

                credentials = Credentials.from_service_account_file(
                    self.credentials_file,
                    scopes=SCOPES
                )
                logger.info("Using credentials from file")

            self.client = gspread.authorize(credentials)

            if not self.spreadsheet_id:
                logger.error("SPREADSHEET_ID environment variable not set")
                return False

            try:
                self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
                logger.info(f"Spreadsheet opened: {self.spreadsheet.title}")
            except Exception as e:
                logger.error(f"Failed to open spreadsheet with ID {self.spreadsheet_id}: {str(e)}")
                return False

            try:
                # Try to get first worksheet
                worksheets = self.spreadsheet.worksheets()
                if not worksheets:
                    logger.error("No worksheets found in spreadsheet")
                    return False
                self.worksheet = worksheets[0]
                logger.info(f"Worksheet accessed: {self.worksheet.title}")
            except Exception as e:
                logger.error(f"Failed to access worksheet: {str(e)}")
                return False

            self._ensure_headers()

            logger.info("Google Sheets initialized successfully")
            return True

        except FileNotFoundError as e:
            logger.error(f"Credentials file not found: {e}")
            return False
        except Exception as e:
            logger.error(f"Error initializing Google Sheets: {type(e).__name__}: {str(e)}")
            return False

    def _ensure_headers(self) -> None:
        """Ensure spreadsheet has headers."""
        try:
            first_row = self.worksheet.row_values(1)

            headers = ['ID', 'Дата регистрации', 'Email', 'Телефон', 'Процент', 'Родитель']

            if not first_row or first_row != headers:
                if first_row:
                    self.worksheet.delete_rows(1, 1)

                self.worksheet.insert_row(headers, index=1)
                logger.info("Headers added to spreadsheet")

        except Exception as e:
            logger.error(f"Error ensuring headers: {e}")

    def _get_next_id(self) -> int:
        """Get next ID for new client."""
        try:
            all_records = self.worksheet.get_all_records()
            if not all_records:
                return 1

            # Get all IDs and find max
            ids = []
            for record in all_records:
                try:
                    id_val = int(record.get('ID', 0))
                    ids.append(id_val)
                except (ValueError, TypeError):
                    pass

            return max(ids) + 1 if ids else 1
        except Exception as e:
            logger.error(f"Error getting next ID: {e}")
            return 1

    async def email_exists(self, email: str) -> dict | None:
        """
        Check if email already exists (case-insensitive).

        Args:
            email: Client email to check

        Returns:
            Dictionary with client data if exists, None otherwise
        """
        try:
            if not self.worksheet:
                logger.error("Worksheet not initialized")
                return None

            all_records = await self.get_all_data()

            email_lower = email.lower()
            for record in all_records:
                record_email = record.get('Email', '')
                # Convert to string if not already
                if isinstance(record_email, (int, float)):
                    record_email = str(record_email)
                if str(record_email).lower() == email_lower:
                    return record

            return None

        except Exception as e:
            logger.error(f"Error checking email: {e}")
            return None

    async def add_user(
        self,
        phone: str,
        email: str,
        percentage: float,
        parent_email: str = ""
    ) -> tuple[bool, str, dict | None]:
        """
        Add new user to Google Sheets.

        Args:
            phone: Phone number
            email: Email
            percentage: Percentage value
            parent_email: Email of parent user (optional)

        Returns:
            Tuple of (success: bool, message: str, existing_record: dict or None)
        """
        try:
            if not self.worksheet:
                logger.error("Worksheet not initialized")
                return False, "Worksheet not initialized", None

            # Check if email already exists
            existing = await self.email_exists(email)
            if existing:
                logger.info(f"Email already exists: {email}")
                return False, "exists", existing

            # If parent_email specified, verify parent exists
            if parent_email:
                parent = await self.find_user_by_email(parent_email)
                if not parent:
                    logger.error(f"Parent not found: {parent_email}")
                    return False, "parent_not_found", None

            # Get next ID
            next_id = self._get_next_id()

            # Get current date and time
            from datetime import datetime
            date = datetime.now().strftime("%d.%m.%Y %H:%M")

            row_data = [
                next_id,
                date,
                str(email),
                str(phone),
                str(percentage),
                parent_email
            ]

            self.worksheet.append_row(row_data)

            logger.info(f"Added user: ID={next_id}, email={email}, parent={parent_email}")
            return True, "success", None

        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False, str(e), None

    async def get_children(self, parent_email: str) -> list[dict]:
        """
        Get all child users of a parent.

        Args:
            parent_email: Parent email

        Returns:
            List of child user records
        """
        try:
            all_records = await self.get_all_data()
            children = [r for r in all_records if r.get('Родитель', '').lower() == parent_email.lower()]
            return children
        except Exception as e:
            logger.error(f"Error getting children: {e}")
            return []

    async def get_user_tree(self, email: str, indent: str = "") -> str:
        """
        Get hierarchical tree of users starting from given email.

        Args:
            email: Root email
            indent: Indentation string

        Returns:
            Formatted tree string
        """
        try:
            user = await self.find_user_by_email(email)
            if not user:
                return ""

            tree = f"{indent}{user.get('Email', email)}\n"

            children = await self.get_children(email)
            for i, child in enumerate(children):
                is_last = i == len(children) - 1
                child_indent = indent + ("└── " if is_last else "├── ")
                next_indent = indent + ("    " if is_last else "│   ")
                child_tree = await self.get_user_tree(child.get('Email', ''), next_indent)
                tree += child_tree

            return tree
        except Exception as e:
            logger.error(f"Error building user tree: {e}")
            return ""

    async def add_log(self, telegram_id: int, username: str, action: str) -> bool:
        """
        Add log entry to Logs sheet.

        Args:
            telegram_id: Telegram user ID
            username: Telegram username
            action: Action description

        Returns:
            True if successful
        """
        try:
            from datetime import datetime

            # Get or create Logs worksheet
            worksheets = self.spreadsheet.worksheets()
            logs_sheet = None

            for ws in worksheets:
                if ws.title == "Logs":
                    logs_sheet = ws
                    break

            if not logs_sheet:
                logs_sheet = self.spreadsheet.add_worksheet("Logs", rows=1000, cols=4)
                # Add headers
                logs_sheet.insert_row(['Дата', 'Telegram ID', 'Имя пользователя', 'Действие'], index=1)

            # Add log entry
            date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            logs_sheet.append_row([date, telegram_id, username, action])

            logger.info(f"Log added: {telegram_id} ({username}) - {action}")
            return True

        except Exception as e:
            logger.error(f"Error adding log: {e}")
            return False

    async def is_user_authorized(self, telegram_id: int) -> bool:
        """
        Check if user is authorized.

        Args:
            telegram_id: Telegram user ID

        Returns:
            True if authorized
        """
        try:
            worksheets = self.spreadsheet.worksheets()
            users_sheet = None

            for ws in worksheets:
                if ws.title == "Users":
                    users_sheet = ws
                    break

            if not users_sheet:
                return False

            records = users_sheet.get_all_records()
            for record in records:
                if int(record.get('Telegram ID', 0)) == telegram_id:
                    return True

            return False

        except Exception as e:
            logger.error(f"Error checking authorization: {e}")
            return False

    async def add_authorized_user(self, telegram_id: int, username: str) -> bool:
        """
        Add authorized user.

        Args:
            telegram_id: Telegram user ID
            username: Telegram username

        Returns:
            True if successful
        """
        try:
            from datetime import datetime

            worksheets = self.spreadsheet.worksheets()
            users_sheet = None

            for ws in worksheets:
                if ws.title == "Users":
                    users_sheet = ws
                    break

            if not users_sheet:
                users_sheet = self.spreadsheet.add_worksheet("Users", rows=1000, cols=3)
                # Add headers
                users_sheet.insert_row(['Telegram ID', 'Имя пользователя', 'Дата авторизации'], index=1)

            # Check if already authorized
            records = users_sheet.get_all_records()
            for record in records:
                if int(record.get('Telegram ID', 0)) == telegram_id:
                    logger.info(f"User already authorized: {telegram_id}")
                    return True

            # Add new user
            date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            users_sheet.append_row([telegram_id, username, date])

            logger.info(f"User authorized: {telegram_id} ({username})")
            return True

        except Exception as e:
            logger.error(f"Error adding authorized user: {e}")
            return False

    async def get_user_info(self, user_email: str) -> dict | None:
        """
        Get user info with children count.

        Args:
            user_email: User email

        Returns:
            User record with children count
        """
        try:
            user = await self.find_user_by_email(user_email)
            if not user:
                return None

            children = await self.get_children(user_email)
            user['Количество приглашённых пользователей'] = len(children)

            return user
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None

    async def find_user_by_email(self, email: str) -> dict | None:
        """
        Find user by email (case-insensitive).

        Args:
            email: User email to search

        Returns:
            Dictionary with user data or None
        """
        try:
            return await self.email_exists(email)
        except Exception as e:
            logger.error(f"Error finding user: {e}")
            return None

    async def get_all_data(self) -> List[Dict[str, str]]:
        """
        Get all data from Google Sheets.

        Returns:
            List of dictionaries with client data
        """
        try:
            if not self.worksheet:
                logger.error("Worksheet not initialized")
                return []

            all_records = self.worksheet.get_all_records()

            if not all_records:
                logger.info("No data found in spreadsheet")
                return []

            logger.info(f"Retrieved {len(all_records)} records from spreadsheet")
            return all_records

        except Exception as e:
            logger.error(f"Error getting data from spreadsheet: {e}")
            return []

    def get_spreadsheet_link(self) -> Optional[str]:
        """
        Get link to Google Sheets.

        Returns:
            Spreadsheet URL or None
        """
        try:
            if self.spreadsheet_id:
                return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
            return None
        except Exception as e:
            logger.error(f"Error getting spreadsheet link: {e}")
            return None

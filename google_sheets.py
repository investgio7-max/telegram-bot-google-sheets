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
                self.worksheet = self.spreadsheet.worksheet(0)
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

            headers = ['Дата', 'Телефон', 'Email', 'Процент']

            if not first_row or first_row != headers:
                if first_row:
                    self.worksheet.delete_rows(1, 1)

                self.worksheet.insert_row(headers, index=1)
                logger.info("Headers added to spreadsheet")

        except Exception as e:
            logger.error(f"Error ensuring headers: {e}")

    async def add_client(
        self,
        date: str,
        phone: str,
        email: str,
        percentage: float
    ) -> bool:
        """
        Add new client to Google Sheets.

        Args:
            date: Date in format DD.MM.YYYY HH:MM
            phone: Client phone number
            email: Client email
            percentage: Percentage value

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.worksheet:
                logger.error("Worksheet not initialized")
                return False

            row_data = [
                date,
                str(phone),
                str(email),
                str(percentage)
            ]

            self.worksheet.append_row(row_data)

            logger.info(f"Client added: {phone}, {email}, {percentage}%")
            return True

        except Exception as e:
            logger.error(f"Error adding client: {e}")
            return False

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

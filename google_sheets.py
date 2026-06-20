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

            headers = ['ID', 'Дата регистрации', 'Email', 'Телефон', 'Процент', 'Роль', 'Агент']

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

    async def add_client(
        self,
        phone: str,
        email: str,
        percentage: float,
        role: str = "Клиент",
        agent_email: str = ""
    ) -> tuple[bool, str, dict | None]:
        """
        Add new client/agent to Google Sheets.

        Args:
            phone: Phone number
            email: Email
            percentage: Percentage value
            role: Role (Агент or Клиент)
            agent_email: Email of agent (for Клиент role)

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

            # If role is Клиент, verify agent exists
            if role == "Клиент" and agent_email:
                agent = await self.find_client_by_email(agent_email)
                if not agent:
                    logger.error(f"Agent not found: {agent_email}")
                    return False, "agent_not_found", None
                # Check that agent has role Агент
                if agent.get('Роль', '') != 'Агент':
                    logger.error(f"Email is not an agent: {agent_email}")
                    return False, "not_an_agent", None

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
                role,
                agent_email
            ]

            self.worksheet.append_row(row_data)

            logger.info(f"Added: ID={next_id}, email={email}, role={role}, agent={agent_email}")
            return True, "success", None

        except Exception as e:
            logger.error(f"Error adding client: {e}")
            return False, str(e), None

    async def get_agent_clients(self, agent_email: str) -> list[dict]:
        """
        Get all clients of an agent.

        Args:
            agent_email: Agent email

        Returns:
            List of client records
        """
        try:
            all_records = await self.get_all_data()
            clients = [r for r in all_records if r.get('Агент', '').lower() == agent_email.lower()]
            return clients
        except Exception as e:
            logger.error(f"Error getting agent clients: {e}")
            return []

    async def get_agent_info(self, agent_email: str) -> dict | None:
        """
        Get agent info with clients count.

        Args:
            agent_email: Agent email

        Returns:
            Agent record with clients info
        """
        try:
            agent = await self.find_client_by_email(agent_email)
            if not agent or agent.get('Роль', '') != 'Агент':
                return None

            clients = await self.get_agent_clients(agent_email)
            agent['Количество клиентов'] = len(clients)
            agent['Клиенты'] = clients

            return agent
        except Exception as e:
            logger.error(f"Error getting agent info: {e}")
            return None

    async def find_client_by_email(self, email: str) -> dict | None:
        """
        Find client by email (case-insensitive).

        Args:
            email: Client email to search

        Returns:
            Dictionary with client data or None
        """
        try:
            return await self.email_exists(email)
        except Exception as e:
            logger.error(f"Error finding client: {e}")
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

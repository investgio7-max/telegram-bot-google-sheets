# Структура проекта

Полное описание всех файлов и директорий проекта.

## 📁 Дерево проекта

```
telegram-bot-google-sheets/
│
├── 📄 bot.py                      # Основной файл бота
├── 📄 google_sheets.py            # Модуль работы с Google Sheets
├── 📄 excel_generator.py          # Модуль генерации Excel файлов
├── 📄 utils.py                    # Утилиты и вспомогательные функции
│
├── 📄 requirements.txt            # Список зависимостей Python
├── 📄 Dockerfile                  # Docker конфигурация
├── 📄 railway.json                # Конфигурация Railway
│
├── 📄 .env                        # Переменные окружения (НЕ КОММИТИТЬ)
├── 📄 .env.example                # Пример .env файла
├── 📄 .gitignore                  # Git исключения
│
├── 📄 README.md                   # Основная документация
├── 📄 QUICKSTART.md               # Быстрый старт (15 мин)
├── 📄 SETUP_GUIDE.md              # Подробная настройка
├── 📄 RAILWAY_DEPLOYMENT.md       # Инструкции по Railway
├── 📄 PROJECT_STRUCTURE.md        # Этот файл
│
├── 📄 test_local.py               # Скрипт для локального тестирования
│
├── 🔐 credentials.json            # Google API ключи (НЕ КОММИТИТЬ)
└── 📁 logs/                       # Директория логов (автоматическая)
    └── bot.log                    # Логи приложения
```

## 📋 Описание файлов

### Основной код (Python)

#### `bot.py` (430 строк)
**Основной файл приложения - сердце проекта**

Содержит:
- Инициализация бота через Telegram Bot API
- Finite State Machine (FSM) для управления состояниями пользователя
- Обработчики команд и сообщений:
  - `/start` - главное меню
  - `/help` - справка
  - Добавление клиента (многоэтапный процесс)
  - Загрузка Excel файла
- Логирование всех операций
- Обработка ошибок

**Зависимости:**
- `aiogram` - фреймворк для Telegram
- `dotenv` - загрузка переменных окружения

#### `google_sheets.py` (150+ строк)
**Интеграция с Google Sheets API**

Содержит класс `GoogleSheetsManager`:
- Аутентификация через сервис-аккаунт
- Подключение к Google Sheets
- Создание/проверка заголовков таблицы
- Добавление новых записей
- Получение всех данных
- Получение ссылки на таблицу

**Особенности:**
- Поддержка Base64 кодирования для Railway
- Полная обработка ошибок
- Подробное логирование

**Зависимости:**
- `gspread` - клиент Google Sheets
- `google-auth` - аутентификация Google

#### `excel_generator.py` (150+ строк)
**Генерация Excel файлов**

Содержит класс `ExcelGenerator`:
- Создание Excel файлов из данных
- Форматирование (цвета, границы, размеры колонок)
- Красивые заголовки и шрифты
- Управление временными файлами
- Очистка старых файлов

**Особенности:**
- Автоматический размер колонок
- Синий заголовок с белым текстом
- Тонкие границы для всех ячеек

**Зависимости:**
- `openpyxl` - работа с Excel файлами

#### `utils.py` (200+ строк)
**Утилиты и вспомогательные функции**

Содержит:
- Валидация файла credentials.json
- Кодирование credentials в Base64
- Декодирование Base64 обратно в файл
- Проверка переменных окружения
- Информация о конфигурации бота
- Вывод инструкций по настройке

**Используется для:**
- Проверки конфигурации перед запуском
- Подготовки к развертыванию на Railway
- Отладки проблем

### Конфигурация (Configuration)

#### `requirements.txt`
**Список зависимостей Python**

Версии:
```
aiogram==3.3.0              # Telegram Bot API
gspread==5.12.4            # Google Sheets API
google-auth==2.28.0        # Google аутентификация
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
openpyxl==3.10.10          # Excel файлы
python-dotenv==1.0.0       # Переменные окружения
aiohttp==3.9.1             # Async HTTP
```

#### `Dockerfile`
**Docker конфигурация для Railway**

- Базовый образ: Python 3.11-slim
- Установка зависимостей из requirements.txt
- Запуск: `python bot.py`

#### `railway.json`
**Конфигурация Railway**

Определяет:
- Способ сборки (Dockerfile)
- Команда для запуска
- Переменные окружения

#### `.env` (НЕ КОММИТИТЬ)
**Переменные окружения для локального запуска**

Содержит:
```
BOT_TOKEN=your_token_here
SPREADSHEET_ID=your_id_here
```

#### `.env.example`
**Пример .env файла**

Показывает структуру, которую нужно скопировать

#### `.gitignore`
**Правила для git**

Исключает:
- `__pycache__/` - Python кэш
- `*.pyc` - скомпилированные Python файлы
- `venv/` - виртуальное окружение
- `.env` - переменные окружения
- `credentials.json` - ключи Google
- `*.log` - логи
- `.DS_Store` - файлы macOS

#### `credentials.json` (НЕ КОММИТИТЬ)
**Google API ключи**

JSON файл со структурой:
```json
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  ...
}
```

**ВАЖНО:** Никогда не коммитьте этот файл!

### Документация (Documentation)

#### `README.md`
**Основная документация**

Содержит:
- Описание проекта
- Требования
- Инструкции по установке
- Настройка Google Sheets API
- Развертывание на Railway
- Решение проблем
- Безопасность

**Аудитория:** Разработчики, DevOps

#### `QUICKSTART.md`
**Быстрый старт за 15 минут**

8 простых шагов:
1. Создание бота в Telegram
2. Создание сервис-аккаунта Google
3. Создание Google Sheets
4. Выдача доступа
5. Настройка окружения
6. Установка зависимостей
7. Запуск бота
8. Проверка в Telegram

**Аудитория:** Новички, быстрый запуск

#### `SETUP_GUIDE.md`
**Подробное пошаговое руководство**

12 этапов с скриншотами:
- Telegram Bot (BotFather)
- Google Cloud Console
- Google APIs (Sheets, Drive)
- Service Account
- Получение ключей
- Google Sheets таблица
- Выдача доступа
- Локальное окружение
- Установка зависимостей
- Первый запуск
- Тестирование
- Railway развертывание

**Аудитория:** Пользователи, нуждающиеся в детальном руководстве

#### `RAILWAY_DEPLOYMENT.md`
**Полное руководство по Railway**

Содержит:
- Что такое Railway
- Подготовка GitHub репозитория
- Регистрация на Railway
- Создание проекта
- Настройка переменных
- Загрузка credentials
- Проверка развертывания
- Мониторинг
- Обновление кода
- Railway CLI
- Troubleshooting
- Плани затрат

**Аудитория:** DevOps, разработчики

### Тестирование (Testing)

#### `test_local.py`
**Скрипт для локального тестирования**

Тесты:
- Переменные окружения
- Файл credentials.json
- Подключение к Google Sheets
- Генерация Excel файлов
- Валидность BOT_TOKEN
- Доступ к Telegram API

Использование:
```bash
python test_local.py
```

Выводит:
```
✓ PASS: Environment Variables
✓ PASS: Credentials File
✓ PASS: Bot Token
✓ PASS: Google Sheets
✓ PASS: Excel Generator

Total: 5/5 tests passed
🎉 All tests passed! Bot is ready to run!
```

## 🔄 Поток данных

```
Пользователь (Telegram)
    ↓
    ├─→ Команда /start → Main Menu
    │
    ├─→ ➕ Добавить клиента
    │    ├→ Запрос телефона
    │    ├→ Запрос email
    │    ├→ Запрос процента
    │    └→ Сохранение в Google Sheets ← google_sheets.py
    │
    └─→ 📊 Скачать Excel
         ├→ Получение данных из Google Sheets ← google_sheets.py
         ├→ Генерация Excel файла ← excel_generator.py
         └→ Отправка файла в Telegram
```

## 📦 Классы и структура

### `GoogleSheetsManager`

```python
class GoogleSheetsManager:
    def __init__(credentials_file: str)
    def _initialize() → bool
    def _ensure_headers() → None
    async def add_client(date, phone, email, percentage) → bool
    async def get_all_data() → List[Dict]
    def get_spreadsheet_link() → Optional[str]
```

### `ExcelGenerator`

```python
class ExcelGenerator:
    def __init__(temp_dir: str)
    async def create_excel(data: List[Dict]) → Optional[str]
    def cleanup_temp_files(max_age_hours: int) → None
```

### `ClientStates` (FSM)

```python
class ClientStates:
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_percentage = State()
```

## 🔐 Переменные окружения

| Переменная | Обязательная | Описание |
|-----------|------------|---------|
| `BOT_TOKEN` | Да | Токен Telegram бота из @BotFather |
| `SPREADSHEET_ID` | Да | ID Google Sheets таблицы |
| `CREDENTIALS_BASE64` | Нет* | Base64 кодированный credentials.json |
| `GOOGLE_CREDENTIALS_FILE` | Нет | Путь к credentials.json (по умолчанию: ./credentials.json) |

*: Либо `credentials.json` файл, либо `CREDENTIALS_BASE64` переменная должны быть доступны

## 📊 Таблица в Google Sheets

Структура (4 колонки):

| Дата | Телефон | Email | Процент |
|------|---------|-------|---------|
| 20.06.2024 10:30 | +7 (123) 456-78-90 | test@example.com | 25 |
| 20.06.2024 11:45 | +7 (987) 654-32-10 | client@example.com | 50 |

## 📈 Размер проекта

```
bot.py                     ~430 строк кода
google_sheets.py           ~150 строк кода
excel_generator.py         ~150 строк кода
utils.py                   ~200 строк кода
test_local.py              ~300 строк кода
                          ----------
Всего кода:               ~1,230 строк

Документация:             ~2,000+ строк
```

## 🚀 Развертывание

### Локально

```bash
python bot.py
```

### На Railway

1. Создать GitHub репозиторий
2. Отправить код на GitHub
3. Подключить Railway к GitHub
4. Установить переменные окружения
5. Railway автоматически развернет

### Docker

```bash
docker build -t telegram-bot .
docker run -e BOT_TOKEN=... -e SPREADSHEET_ID=... telegram-bot
```

## 📚 Зависимости между модулями

```
bot.py
  ├─→ google_sheets.py (импорт GoogleSheetsManager)
  │    └─→ gspread
  │    └─→ google-auth
  │
  ├─→ excel_generator.py (импорт ExcelGenerator)
  │    └─→ openpyxl
  │
  ├─→ aiogram (импорт Bot, Dispatcher и т.д.)
  │    └─→ aiohttp
  │
  └─→ dotenv (импорт load_dotenv)

test_local.py
  ├─→ google_sheets.py
  ├─→ excel_generator.py
  ├─→ aiogram
  └─→ все прочие зависимости
```

## 🔍 Логирование

Логи идут в два места:

1. **Консоль** - вывод в реальном времени
2. **Файл** - `bot.log` в корне проекта

Формат:
```
2024-06-20 10:00:00,123 - bot - INFO - Bot starting...
```

Уровни логирования:
- `DEBUG` - детальная информация
- `INFO` - информационные сообщения
- `WARNING` - предупреждения
- `ERROR` - ошибки
- `CRITICAL` - критические ошибки

## ✅ Чек-лист для запуска

- [ ] Python 3.9+ установлен
- [ ] requirements.txt установлены
- [ ] .env файл создан
- [ ] BOT_TOKEN установлен и правильный
- [ ] SPREADSHEET_ID установлен и правильный
- [ ] credentials.json скачан из Google Cloud
- [ ] Сервис-аккаунт добавлен в Google Sheets с доступом "Редактор"
- [ ] `python test_local.py` проходит все тесты
- [ ] `python bot.py` запускается без ошибок
- [ ] Бот отвечает на /start в Telegram

## 🎯 Что дальше?

1. **Модифицировать** - добавьте новые поля и команды
2. **Масштабировать** - добавьте базу данных вместо Google Sheets
3. **Улучшить** - добавьте аналитику и статистику
4. **Развернуть** - используйте Railway для 24/7 работы

---

**Полная документация проекта готова к использованию! 🎉**

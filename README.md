# Telegram Bot для управления клиентами через Google Sheets

Бот для Telegram, который позволяет добавлять клиентов и скачивать данные в Excel-формате через интеграцию с Google Sheets.

## Возможности

- ✅ Добавление новых клиентов через Telegram
- ✅ Автоматическое сохранение данных в Google Sheets
- ✅ Загрузка всех данных в Excel-файл
- ✅ Красивое форматирование Excel-файла
- ✅ Логирование всех операций
- ✅ Полная обработка ошибок
- ✅ Готов к развертыванию на Railway

## Технологический стек

- **aiogram 3.x** - асинхронный фреймворк для Telegram Bot API
- **gspread** - Python библиотека для работы с Google Sheets API
- **google-auth** - аутентификация Google
- **openpyxl** - создание и форматирование Excel файлов
- **python-dotenv** - управление переменными окружения

## Предварительные требования

- Python 3.9+
- Аккаунт Telegram
- Аккаунт Google с доступом к Google Sheets API
- Аккаунт Railway (для развертывания)

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone <your-repo-url>
cd telegram-bot-google-sheets
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Создание Telegram бота

1. Откройте Telegram и найдите **@BotFather**
2. Напишите `/newbot`
3. Следуйте инструкциям для создания нового бота
4. Скопируйте **BOT_TOKEN** из ответа

### 5. Настройка Google Sheets API

#### Шаг 5.1: Создание проекта Google Cloud

1. Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект:
   - Нажмите на выпадающее меню проектов в верхней части
   - Выберите "Создать проект"
   - Введите имя проекта (например, "Telegram Bot Clients")
   - Нажмите "Создать"

#### Шаг 5.2: Включение Google Sheets API

1. В Google Cloud Console перейдите в "APIs & Services" → "Library"
2. Найдите "Google Sheets API"
3. Нажмите на неё и выберите "Включить"
4. Найдите "Google Drive API"
5. Нажмите на неё и выберите "Включить"

#### Шаг 5.3: Создание сервисного аккаунта

1. Перейдите в "APIs & Services" → "Credentials"
2. Нажмите "Создать учётные данные" → "Сервисный аккаунт"
3. Заполните детали:
   - **Service account name**: `telegram-bot`
   - **Service account ID**: будет заполнено автоматически
   - Нажмите "Создать и продолжить"
4. На этапе "Grant this service account access to project" нажмите "Создать и продолжить"
5. На этапе "Grant users access to this service account" нажмите "Готово"

#### Шаг 5.4: Получение ключей доступа

1. В "APIs & Services" → "Credentials" найдите созданный сервисный аккаунт
2. Нажмите на email сервисного аккаунта
3. Перейдите на вкладку "Ключи"
4. Нажмите "Добавить ключ" → "Создать новый ключ"
5. Выберите тип JSON
6. Нажмите "Создать"
7. Автоматически скачается файл `[project-name]-[hash].json`
8. Переименуйте этот файл в `credentials.json` и поместите его в корень проекта

#### Шаг 5.5: Создание Google Sheets

1. Откройте [Google Sheets](https://sheets.google.com)
2. Создайте новую таблицу
3. Скопируйте ID таблицы из URL:
   ```
   https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
   ```

#### Шаг 5.6: Выдача доступа сервисному аккаунту

1. В Google Sheets нажмите "Поделиться"
2. Скопируйте email сервисного аккаунта из `credentials.json` (поле `client_email`)
3. Вставьте email и дайте доступ "Редактор"
4. Отправьте приглашение

### 6. Создание файла .env

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_telegram_bot_token_here
SPREADSHEET_ID=your_google_sheets_id_here
```

Замените:
- `your_telegram_bot_token_here` - токен из @BotFather
- `your_google_sheets_id_here` - ID вашей Google Sheets

### 7. Локальный запуск

```bash
python bot.py
```

Вы должны увидеть в логах:
```
2024-06-20 10:00:00 - bot - INFO - Bot starting...
2024-06-20 10:00:01 - bot - INFO - Google Sheets initialized successfully
```

### 8. Проверка работы

1. Откройте Telegram
2. Найдите вашего бота по имени (который вы дали @BotFather)
3. Напишите `/start`
4. Вы должны увидеть меню с кнопками

## Развертывание на Railway

### Предварительные требования

- Аккаунт Railway
- Git с настроенным доступом к репозиторию

### Инструкции по развертыванию

1. **Создание репозитория GitHub**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/your-repo.git
   git push -u origin main
   ```

2. **Создание проекта в Railway**

   - Откройте [Railway](https://railway.app)
   - Нажмите "Create a new project"
   - Выберите "Deploy from GitHub repo"
   - Подключите ваш GitHub репозиторий
   - Выберите репозиторий с ботом

3. **Настройка переменных окружения в Railway**

   - В проекте Railway перейдите в "Variables"
   - Добавьте следующие переменные:
     - `BOT_TOKEN` - ваш токен Telegram бота
     - `SPREADSHEET_ID` - ID вашей Google Sheets

4. **Загрузка credentials.json**

   Railway не поддерживает прямую загрузку файлов, поэтому используется один из способов:

   **Способ 1: Через Base64 (рекомендуется)**

   ```bash
   base64 credentials.json | tr -d '\n'
   ```

   Скопируйте вывод и добавьте в Railway переменную:
   - `CREDENTIALS_BASE64` - закодированное содержимое credentials.json

   Затем обновите `google_sheets.py`:

   ```python
   def _initialize(self) -> bool:
       try:
           import base64
           import json

           cred_data = os.getenv('CREDENTIALS_BASE64')
           if cred_data:
               cred_json = base64.b64decode(cred_data).decode('utf-8')
               cred_dict = json.loads(cred_json)
               credentials = Credentials.from_service_account_info(
                   cred_dict,
                   scopes=SCOPES
               )
           else:
               credentials = Credentials.from_service_account_file(...)
   ```

   **Способ 2: Через GitHub Secrets**

   1. В GitHub репозитории перейдите в Settings → Secrets and variables → Actions
   2. Создайте новый secret `CREDENTIALS_JSON` с содержимым файла
   3. Создайте файл `.github/workflows/secrets.yml`:

   ```yaml
   name: Deploy Secrets
   on: [push]
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Create credentials file
           run: echo "${{ secrets.CREDENTIALS_JSON }}" > credentials.json
   ```

5. **Развертывание**

   - Railway автоматически развернет ваше приложение при каждом push в main
   - Следите за логами в Railway для проверки ошибок

## Структура проекта

```
telegram-bot-google-sheets/
├── bot.py                  # Основной файл бота
├── google_sheets.py        # Модуль для работы с Google Sheets
├── excel_generator.py      # Модуль для генерации Excel файлов
├── requirements.txt        # Зависимости проекта
├── Dockerfile             # Docker конфигурация
├── .gitignore             # Git игнор файл
├── .env.example           # Пример переменных окружения
└── README.md              # Этот файл
```

## Использование бота

### Основные команды

- `/start` - Показать главное меню
- `/help` - Показать справку
- `➕ Добавить клиента` - Начать процесс добавления нового клиента
- `📊 Скачать Excel` - Загрузить Excel файл со всеми клиентами

### Процесс добавления клиента

1. Нажмите "➕ Добавить клиента"
2. Введите телефон клиента (минимум 5 символов)
3. Введите email клиента (должен содержать @ и .)
4. Введите процент (число от 0 до 100)
5. Готово! Данные сохранены в Google Sheets

### Загрузка Excel файла

1. Нажмите "📊 Скачать Excel"
2. Бот скачает данные из Google Sheets
3. Создаст красиво отформатированный Excel файл
4. Отправит вам файл в Telegram
5. Временный файл будет удален

## Логирование

Все операции логируются:
- **Консоль** - вывод в реальном времени
- **Файл** - `bot.log` в корне проекта

Логи содержат:
- Ошибки и исключения
- Информацию о добавленных клиентах
- Информацию о скачанных файлах
- Информацию о инициализации

## Решение проблем

### Проблема: "BOT_TOKEN environment variable not set"

**Решение**: Убедитесь, что в файле `.env` установлена переменная `BOT_TOKEN`:

```env
BOT_TOKEN=your_token_here
```

### Проблема: "SPREADSHEET_ID environment variable not set"

**Решение**: Добавьте `SPREADSHEET_ID` в `.env`:

```env
SPREADSHEET_ID=your_spreadsheet_id_here
```

### Проблема: "Credentials file not found"

**Решение**: 
1. Убедитесь, что файл `credentials.json` находится в корне проекта
2. Проверьте, что файл скачан из Google Cloud Console
3. Проверьте права доступа к файлу: `ls -l credentials.json`

### Проблема: "Permission denied" при добавлении клиента

**Решение**:
1. Проверьте, что email сервисного аккаунта имеет доступ к таблице
2. Убедитесь, что доступ выдан с правами "Редактор"
3. В Google Sheets нажмите "Поделиться" и проверьте наличие сервисного аккаунта

### Проблема: Excel файл пуст

**Решение**: Убедитесь, что:
1. В Google Sheets есть данные (кроме заголовков)
2. Данные в правильном формате
3. Сервисный аккаунт может читать таблицу

## Безопасность

⚠️ **Важные правила**:

1. **Никогда** не коммитьте `credentials.json` в репозиторий
2. Используйте `.gitignore` для исключения чувствительных файлов
3. Храните `BOT_TOKEN` и `SPREADSHEET_ID` в переменных окружения
4. Используйте GitHub Secrets для Railway развертывания
5. Регулярно ротируйте ключи доступа
6. Ограничивайте доступ к Google Sheets только необходимыми аккаунтами

## Разработка

### Добавление новых функций

1. Создайте новую ветку: `git checkout -b feature/your-feature`
2. Внесите изменения
3. Добавьте логирование для новых операций
4. Тестируйте локально перед push
5. Создайте Pull Request

### Структура обработчиков aiogram

```python
@dp.message(Command("command_name"))
async def command_handler(message: types.Message):
    # Обработчик команды
    pass

@dp.message(lambda message: message.text == "Button text")
async def button_handler(message: types.Message):
    # Обработчик нажатия кнопки
    pass
```

## Производительность и масштабирование

- Бот использует асинхронность для обработки множественных пользователей одновременно
- Google Sheets имеет лимиты на запросы (300 запросов в минуту при Rate Limit)
- Excel файлы хранятся во временной папке и автоматически удаляются

## Лицензия

MIT License - смотрите файл LICENSE для деталей

## Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте логи: `tail -f bot.log`
2. Убедитесь, что все переменные окружения установлены
3. Перезагрузите бота: `Ctrl+C` и `python bot.py`

## Обновления и изменения

- **v1.0.0** - Первый релиз с полной функциональностью
  - Добавление клиентов
  - Загрузка Excel
  - Интеграция с Google Sheets
  - Поддержка Railway

## Автор

Telegram Bot для управления клиентами через Google Sheets

Created with ❤️ for efficiency

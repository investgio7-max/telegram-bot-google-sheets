# 🎯 Шпаргалка по командам

Быстрая справка по всем командам и действиям.

## 🚀 Команды запуска

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск бота
```bash
python bot.py
```

### Проверка конфигурации
```bash
python test_local.py
```

### Остановка бота
```bash
Ctrl + C
```

---

## 🔧 Утилиты

### Закодировать credentials в Base64 (для Railway)
```bash
python -c "from utils import encode_credentials_base64; print(encode_credentials_base64())"
```

### Проверить конфигурацию
```bash
python -c "from utils import get_bot_info; print(get_bot_info())"
```

### Валидировать credentials файл
```bash
python -c "from utils import validate_credentials_file; validate_credentials_file()"
```

### Просмотр инструкций
```bash
python -c "from utils import print_setup_instructions; print_setup_instructions()"
```

---

## 📝 Telegram команды (в боте)

| Команда | Описание |
|---------|---------|
| `/start` | Показать главное меню |
| `/help` | Показать справку |
| `➕ Добавить клиента` | Начать добавление нового клиента |
| `📊 Скачать Excel` | Загрузить Excel файл с данными |
| `❌ Отмена` | Отменить текущее действие |

---

## 🐍 Python команды для разработчика

### Импорт модулей
```python
from bot import dp, bot
from google_sheets import GoogleSheetsManager
from excel_generator import ExcelGenerator
```

### Работа с Google Sheets
```python
import asyncio
from google_sheets import GoogleSheetsManager

async def example():
    sheets = GoogleSheetsManager()
    
    # Добавить клиента
    await sheets.add_client(
        date="20.06.2024 10:30",
        phone="+7 (123) 456-78-90",
        email="test@example.com",
        percentage=25
    )
    
    # Получить всех клиентов
    data = await sheets.get_all_data()
    print(data)
    
    # Получить ссылку на таблицу
    link = sheets.get_spreadsheet_link()
    print(link)

asyncio.run(example())
```

### Работа с Excel генератором
```python
import asyncio
from excel_generator import ExcelGenerator

async def example():
    generator = ExcelGenerator()
    
    test_data = [
        {
            'Дата': '20.06.2024 10:30',
            'Телефон': '+7 (123) 456-78-90',
            'Email': 'test@example.com',
            'Процент': '25'
        }
    ]
    
    # Создать Excel файл
    filepath = await generator.create_excel(test_data)
    print(f"File: {filepath}")
    
    # Очистить старые файлы
    generator.cleanup_temp_files(max_age_hours=1)

asyncio.run(example())
```

---

## 🔐 Переменные окружения

### Установка через .env файл

**Файл `.env`:**
```
BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZabcdefGHI
SPREADSHEET_ID=1ABC123dEf4GhIjK5lmNoPqRsT6uVwXyZ
```

### Установка через Railway

```bash
railway variables set BOT_TOKEN your_token_here
railway variables set SPREADSHEET_ID your_id_here
railway variables set CREDENTIALS_BASE64 your_base64_here
```

### Чтение переменных в коде
```python
import os

bot_token = os.getenv('BOT_TOKEN')
spreadsheet_id = os.getenv('SPREADSHEET_ID')
credentials_base64 = os.getenv('CREDENTIALS_BASE64')
```

---

## 📊 Структура данных

### Клиент в Google Sheets
```
{
    'Дата': '20.06.2024 10:30',
    'Телефон': '+7 (123) 456-78-90',
    'Email': 'test@example.com',
    'Процент': '25'
}
```

### Формат Telegram сообщения
```python
Message {
    message_id: 123,
    date: 2024-06-20 10:30:00,
    chat: Chat { id: 123456789, type: 'private' },
    from_user: User { id: 123456789, username: 'username' },
    text: 'сообщение'
}
```

---

## 🐛 Отладка

### Просмотр логов в реальном времени
```bash
# На Linux/macOS
tail -f bot.log

# На Windows
Get-Content bot.log -Tail 10 -Wait
```

### Включение debug логирования
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Тестирование в интерпретаторе
```bash
python3 -i bot.py
```

---

## 🌐 Railway команды

### Логин в Railway
```bash
railway login
```

### Просмотр логов
```bash
railway logs
```

### Просмотр переменных
```bash
railway variables
```

### Установка переменной
```bash
railway variables set KEY VALUE
```

### Переменные окружения сразу
```bash
railway run python bot.py
```

### Состояние приложения
```bash
railway status
```

### Переразвертывание
```bash
railway deploy
```

---

## 🔍 Git команды

### Инициализация
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

### Обновление на Railway
```bash
git add .
git commit -m "Update bot"
git push
# Railway автоматически пересоберет и перезагрузит
```

### Проверка статуса
```bash
git status
git log --oneline -5
```

---

## 📦 Docker команды

### Сборка образа
```bash
docker build -t telegram-bot .
```

### Запуск контейнера
```bash
docker run -e BOT_TOKEN=... -e SPREADSHEET_ID=... telegram-bot
```

### Список образов
```bash
docker images
```

### Остановка контейнера
```bash
docker stop container_id
```

---

## ✅ Проверка работоспособности

### Все тесты
```bash
python test_local.py
```

### Отдельная проверка
```bash
python -c "from google_sheets import GoogleSheetsManager; gs = GoogleSheetsManager(); print('OK' if gs.client else 'FAIL')"
```

### Подключение к Telegram
```bash
python -c "import asyncio; from aiogram import Bot; import os; print('BOT_TOKEN:', bool(os.getenv('BOT_TOKEN')))"
```

---

## 📚 Документация быстрые ссылки

```
START_HERE.md       ← Начните отсюда
QUICKSTART.md       ← 15 минут до результата
SETUP_GUIDE.md      ← Подробное руководство
README.md           ← Полная документация
INDEX.md            ← Индекс всех файлов
```

---

## 🎯 Процесс добавления клиента

### Шаг за шагом (в Telegram)
```
1. Пользователь: нажмите "➕ Добавить клиента"
2. Бот: просит телефон
3. Пользователь: вводит "+7 (123) 456-78-90"
4. Бот: просит email
5. Пользователь: вводит "test@example.com"
6. Бот: просит процент
7. Пользователь: вводит "25"
8. Бот: ✅ Данные сохранены в Google Sheets!
```

### Код обработки (bot.py)
```python
@dp.message(ClientStates.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    # ... обработка телефона
    await state.update_data(phone=phone)
    await state.set_state(ClientStates.waiting_for_email)

@dp.message(ClientStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    # ... обработка email
    await state.update_data(email=email)
    await state.set_state(ClientStates.waiting_for_percentage)

@dp.message(ClientStates.waiting_for_percentage)
async def process_percentage(message: types.Message, state: FSMContext):
    # ... обработка процента и сохранение
    success = await google_sheets.add_client(...)
```

---

## 🚀 Развертывание на Railway (быстро)

```bash
# 1. Создать GitHub репозиторий
git init && git add . && git commit -m "Initial"
git remote add origin https://github.com/username/repo.git
git push -u origin main

# 2. На Railway (веб-интерфейс)
# - Создать новый проект
# - Выбрать GitHub репо
# - Добавить переменные BOT_TOKEN, SPREADSHEET_ID, CREDENTIALS_BASE64
# - Нажать Deploy

# 3. Готово! Бот работает 24/7
```

---

## 🎁 Полезные скрипты

### Автоматическая очистка логов
```bash
# Удалить старые логи
rm -f bot.log

# Очистить Python кэш
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Проверка версий
```bash
python --version
pip show aiogram gspread openpyxl
```

### Создание requirements.txt
```bash
pip freeze > requirements.txt
```

---

## 📞 Горячие клавиши (в IDE)

```
Ctrl+K, Ctrl+0      VSCode - Fold all
Ctrl+K, Ctrl+J      VSCode - Unfold all
Ctrl+Shift+F        VSCode - Find in files
Ctrl+H              VSCode - Find and Replace
Ctrl+`              VSCode - Toggle terminal
```

---

## 🎯 Контрольный список перед запуском

```
⬜ Python 3.9+ установлен
⬜ requirements.txt установлены
⬜ .env файл создан
⬜ BOT_TOKEN установлен
⬜ SPREADSHEET_ID установлен
⬜ credentials.json есть или CREDENTIALS_BASE64 установлена
⬜ python test_local.py проходит все тесты
⬜ python bot.py запускается без ошибок
⬜ Бот отвечает на /start в Telegram
```

---

## 💡 Полезные советы

1. **Сохранять логи:** 
   ```bash
   python bot.py >> logs/$(date +%Y-%m-%d).log 2>&1
   ```

2. **Запуск в фоне (Linux/macOS):**
   ```bash
   nohup python bot.py > bot.log 2>&1 &
   ```

3. **Автоперезагрузка при изменении кода:**
   ```bash
   pip install watchdog
   watchmedo auto-restart -d . -p '*.py' -- python bot.py
   ```

4. **Профилирование:**
   ```bash
   python -m cProfile bot.py
   ```

---

**Последнее обновление:** 2024-06-20

**Используйте эту шпаргалку для быстрого доступа к командам!** 🚀

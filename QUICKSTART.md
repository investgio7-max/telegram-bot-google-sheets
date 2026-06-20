# Быстрый старт

Минимальные шаги для запуска бота за 15 минут.

## Пред-условие: Уже установлены?

- ✓ Python 3.9+
- ✓ Telegram аккаунт
- ✓ Google аккаунт

Если нет, посмотрите [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Быстрый старт (15 минут)

### 1️⃣ Создание бота в Telegram (2 мин)

```
1. Найти @BotFather в Telegram
2. Написать: /newbot
3. Дать имя боту (например: MyClientBot)
4. Дать username боту (например: my_client_bot_123)
5. Скопировать токен (длинная строка)
```

✅ **Вы получили**: BOT_TOKEN

### 2️⃣ Создание сервисного аккаунта Google (3 мин)

```
1. Открыть: https://console.cloud.google.com
2. Создать новый проект
3. Включить Google Sheets API
4. Включить Google Drive API
5. Создать Service Account
6. Создать и скачать JSON ключ
7. Переименовать в credentials.json
```

✅ **Вы получили**: credentials.json

### 3️⃣ Создание Google Sheets (1 мин)

```
1. Открыть: https://sheets.google.com
2. Создать новую таблицу
3. Скопировать ID из URL
```

✅ **Вы получили**: SPREADSHEET_ID

### 4️⃣ Выдача доступа (2 мин)

```
1. Открыть credentials.json текстовым редактором
2. Найти поле "client_email"
3. Скопировать email (something@...iam.gserviceaccount.com)
4. Открыть Google Sheets
5. Нажать "Поделиться"
6. Вставить email
7. Выбрать "Редактор"
```

✅ **Разрешение выдано**

### 5️⃣ Настройка окружения (2 мин)

Создать файл `.env`:

```
BOT_TOKEN=YOUR_TOKEN_HERE
SPREADSHEET_ID=YOUR_ID_HERE
```

✅ **Конфигурация готова**

### 6️⃣ Установка зависимостей (3 мин)

```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
```

✅ **Зависимости установлены**

### 7️⃣ Запуск бота (2 мин)

```bash
python test_local.py   # Проверить конфигурацию
python bot.py          # Запустить бота
```

Вы должны увидеть:
```
Bot starting...
Google Sheets initialized successfully
Started polling
```

✅ **БОТ РАБОТАЕТ!**

### 8️⃣ Проверка в Telegram (1 мин)

```
1. Открыть Telegram
2. Найти вашего бота (по username)
3. Написать: /start
4. Вы должны увидеть меню
```

✅ **БОТ ГОТОВ К ИСПОЛЬЗОВАНИЮ!**

---

## Структура проекта

```
telegram-bot/
├── bot.py                    # Основной бот
├── google_sheets.py          # Google Sheets интеграция
├── excel_generator.py        # Генератор Excel
├── utils.py                  # Утилиты
├── test_local.py            # Проверка конфигурации
├── requirements.txt          # Зависимости
├── Dockerfile              # Docker конфиг
├── .env                     # Переменные окружения (не коммитить!)
├── credentials.json         # Ключи Google (не коммитить!)
├── README.md               # Полная документация
├── SETUP_GUIDE.md          # Подробная настройка
├── RAILWAY_DEPLOYMENT.md   # Развертывание
└── .gitignore             # Исключить чувствительные файлы
```

---

## Основные команды

Когда бот запущен:

| Команда | Описание |
|---------|---------|
| `/start` | Показать меню |
| `/help` | Справка по командам |
| `➕ Добавить клиента` | Добавить нового клиента |
| `📊 Скачать Excel` | Загрузить Excel с данными |

---

## Часто встречающиеся ошибки

### ❌ "BOT_TOKEN environment variable not set"

**Решение:**
```bash
# Проверить .env файл
cat .env

# Должно быть:
# BOT_TOKEN=123456789:ABC...
```

### ❌ "SPREADSHEET_ID environment variable not set"

**Решение:**
```bash
# Проверить .env файл
cat .env

# Добавить:
# SPREADSHEET_ID=1ABC123dEf...
```

### ❌ "Credentials file not found"

**Решение:**
1. Убедитесь, что `credentials.json` в корне проекта
2. Проверьте формат: это должен быть JSON файл
3. Или используйте переменную окружения `CREDENTIALS_BASE64`

### ❌ "Permission denied при добавлении клиента"

**Решение:**
1. Откройте Google Sheets
2. Нажмите "Поделиться"
3. Проверьте, что сервис-аккаунт есть в списке
4. Права должны быть "Редактор"

---

## Тестирование функциональности

### Проверить конфигурацию

```bash
python test_local.py
```

Это проверит:
- ✓ Переменные окружения
- ✓ Файл credentials.json
- ✓ Подключение к Google Sheets
- ✓ Генерацию Excel файлов
- ✓ Валидность BOT_TOKEN

### Добавить тестового клиента

1. В боте нажмите "➕ Добавить клиента"
2. Введите тестовые данные:
   - Телефон: `+7 (123) 456-78-90`
   - Email: `test@example.com`
   - Процент: `25`

### Скачать Excel

1. В боте нажмите "📊 Скачать Excel"
2. Скачается файл `clients_YYYYMMDD_HHMMSS.xlsx`
3. Откройте и проверьте данные

---

## Развертывание на Railway (опционально)

Для того чтобы бот работал 24/7:

```bash
# 1. Создать GitHub репозиторий
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main

# 2. Открыть railway.app и подключить GitHub

# 3. Добавить переменные окружения в Railway:
# BOT_TOKEN = your_token
# SPREADSHEET_ID = your_id
# CREDENTIALS_BASE64 = (закодированный credentials.json)

# 4. Railway автоматически развернет ваше приложение
```

Детальнее: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

---

## Что дальше?

### 📚 Почитать документацию

- [README.md](README.md) - Полная документация
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Подробная настройка
- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Развертывание
- [Aiogram Docs](https://docs.aiogram.dev/)
- [Google Sheets API](https://developers.google.com/sheets)

### 🔧 Модифицировать под ваши нужды

**Добавить новую команду:**

```python
@dp.message(Command("mycommand"))
async def my_command(message: types.Message):
    await message.answer("Ответ")
```

**Добавить новое поле:**

1. Отредактируйте `ClientStates` в `bot.py`
2. Добавьте обработчик в `excel_generator.py`
3. Обновите Google Sheets

### 🚀 Запустить в продакшене

```bash
# Развернуть на Railway
# Следить за логами
railway logs

# Обновлять код через GitHub
git push  # Railway автоматически пересоберет
```

---

## Соединение с вашей рабочей системой

**Google Sheets:**
- Данные хранятся в облаке
- Доступны 24/7
- Можно делиться ссылкой
- Сохраняется история

**Telegram:**
- Мобильный доступ
- Уведомления в реальном времени
- Нет необходимости устанавливать приложение

**Excel:**
- Выгружайте данные когда нужно
- Работайте офлайн
- Отправляйте клиентам

---

## Всё работает? 🎉

Отлично! Теперь вы можете:

1. ✅ Добавлять клиентов через Telegram
2. ✅ Данные автоматически сохраняются в Google Sheets
3. ✅ Загружать данные в Excel
4. ✅ Запустить 24/7 на Railway

**Больше ничего не нужно!**

---

## Поддержка

Если что-то не работает:

1. Проверьте логи: `python test_local.py`
2. Прочитайте ошибку внимательно
3. Гуглите ошибку с названием библиотеки (например: "aiogram error xyz")
4. Смотрите документацию в README.md и SETUP_GUIDE.md

---

**Удачи! 🚀**

Created with ❤️ by Telegram Bot Team

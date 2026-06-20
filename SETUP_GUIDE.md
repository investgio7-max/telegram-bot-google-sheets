# Полное руководство по настройке

Это подробное пошаговое руководство для полной настройки бота.

## Этап 1: Создание Telegram бота

### Шаг 1.1: Открытие BotFather

1. Откройте Telegram
2. В поле поиска найдите `@BotFather`
3. Нажмите на профиль и нажмите "Start"

### Шаг 1.2: Создание нового бота

1. Напишите команду `/newbot`
2. BotFather спросит "Alright! A new bot. How are we going to call it? Please choose a name for your bot."
3. Введите имя бота (например: `MyClientBot`)
4. BotFather спросит "Alright! And a few more words about it. What will your bot do?"
5. Введите описание (например: `Управление клиентами через Google Sheets`)
6. BotFather спросит "Good! Now choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot."
7. Введите уникальное имя с окончанием "bot" (например: `my_client_bot_123`)

### Шаг 1.3: Получение токена

После успешного создания BotFather отправит сообщение:

```
Done! Congratulations on your new bot. You will find it at t.me/your_bot_name. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished with creating your bot and stop using it, remember to kill it with the /stop command.

Use this token to access the HTTP API:
123456789:ABCdefGHIjklmnoPQRstuvWXYZabcdefGHI

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

**Скопируйте токен** (длинная строка после "Use this token to access the HTTP API:")

## Этап 2: Создание проекта Google Cloud

### Шаг 2.1: Открытие Google Cloud Console

1. Перейдите на https://console.cloud.google.com/
2. Если нужно, войдите в свой Google аккаунт

### Шаг 2.2: Создание нового проекта

1. В верхней части экрана, слева от поля поиска, нажмите на выпадающее меню "Google Cloud"
2. Нажмите "NEW PROJECT" (или "Новый проект" на русском)
3. В окне "New Project":
   - **Project name**: введите название проекта (например: `Telegram Bot`)
   - **Organization**: оставьте как есть
   - Нажмите "CREATE"
4. Ожидайте создания проекта (может занять несколько секунд)
5. После создания вас автоматически перенесет в новый проект

## Этап 3: Включение Google APIs

### Шаг 3.1: Включение Google Sheets API

1. В Google Cloud Console нажмите на меню (иконка гамбургер) в левом верхнем углу
2. Перейдите в **APIs & Services** → **Library**
3. В поле поиска введите `Google Sheets API`
4. Нажмите на результат "Google Sheets API"
5. Нажмите кнопку "ENABLE" (или "Включить")
6. Ожидайте активации API

### Шаг 3.2: Включение Google Drive API

1. Нажмите на меню в левом верхнем углу
2. Перейдите в **APIs & Services** → **Library**
3. В поле поиска введите `Google Drive API`
4. Нажмите на результат "Google Drive API"
5. Нажмите кнопку "ENABLE" (или "Включить")

## Этап 4: Создание Service Account

### Шаг 4.1: Создание сервисного аккаунта

1. В меню слева нажмите **APIs & Services** → **Credentials**
2. В верхней части нажмите "+ CREATE CREDENTIALS" (или "+ Создать учётные данные")
3. Выберите "Service Account" (или "Сервисный аккаунт")

### Шаг 4.2: Заполнение деталей сервисного аккаунта

На странице "Create service account":

1. **Service account name**: введите `telegram-bot`
2. **Service account ID**: будет заполнено автоматически (что-то вроде `telegram-bot-12345@...`)
3. **Service account description**: введите `Telegram Bot Service Account` (опционально)
4. Нажмите "CREATE AND CONTINUE" (или "Создать и продолжить")

### Шаг 4.3: Выдача прав доступа

На странице "Grant this service account access to project":

1. Нажмите выпадающее меню "Select a role"
2. Найдите и выберите "Editor" (или "Редактор")
3. Нажмите "CONTINUE" (или "Продолжить")

### Шаг 4.4: Завершение

На странице "Grant users access to this service account":

1. Оставьте поля пустыми
2. Нажмите "DONE" (или "Готово")

## Этап 5: Получение ключей доступа

### Шаг 5.1: Открытие страницы ключей

1. В меню слева перейдите **APIs & Services** → **Credentials**
2. В таблице "Service Accounts" найдите только что созданный аккаунт `telegram-bot`
3. Нажмите на email сервисного аккаунта (в колонке "Email")

### Шаг 5.2: Создание ключа

1. На странице сервисного аккаунта перейдите на вкладку "KEYS" (или "Ключи")
2. Нажмите "Add Key" → "Create new key" (или "Добавить ключ" → "Создать новый ключ")
3. Выберите "JSON"
4. Нажмите "CREATE" (или "Создать")

### Шаг 5.3: Загрузка файла

- Браузер автоматически скачает файл с именем похожим на `project-name-abcd1234.json`
- **Переименуйте этот файл в `credentials.json`**
- Поместите его в корень папки проекта (рядом с bot.py)

**Примечание**: Это файл содержит чувствительные данные. Никогда не делитесь им и не коммитьте его в GitHub!

## Этап 6: Создание Google Sheets таблицы

### Шаг 6.1: Создание таблицы

1. Откройте https://sheets.google.com
2. Нажмите на пустую таблицу (первый квадрат с "+" )
3. Откроется новая таблица

### Шаг 6.2: Получение ID таблицы

1. Посмотрите на URL в адресной строке браузера
2. URL будет выглядеть так: `https://docs.google.com/spreadsheets/d/[ID]/edit`
3. Скопируйте только часть `[ID]` (длинная строка букв и цифр)

**Пример**:
```
URL: https://docs.google.com/spreadsheets/d/1ABC123dEf4GhIjK5lmNoPqRsT6uVwXyZ/edit
ID:  1ABC123dEf4GhIjK5lmNoPqRsT6uVwXyZ
```

### Шаг 6.3: Переименование листа (опционально)

1. В таблице найдите вкладку в нижней части "Sheet1"
2. Щелкните правой кнопкой мыши на "Sheet1"
3. Выберите "Rename" (или "Переименовать")
4. Введите новое имя, например "Клиенты"
5. Нажмите Enter

## Этап 7: Выдача доступа Service Account

### Шаг 7.1: Получение email сервисного аккаунта

1. Откройте скачанный файл `credentials.json` в текстовом редакторе
2. Найдите строку `"client_email": "telegram-bot@project-id.iam.gserviceaccount.com"`
3. Скопируйте весь email (важно скопировать точно, с @ и всем содержимым)

### Шаг 7.2: Выдача доступа в Google Sheets

1. Откройте вашу Google Sheets таблицу
2. В верхнем правом углу нажмите на кнопку "Share" (или "Поделиться")
3. В поле введения нажмите на текстовое поле
4. Вставьте email сервисного аккаунта (Ctrl+V или Cmd+V)
5. В выпадающем меню выберите "Editor" (или "Редактор")
6. Убедитесь, что опция "Notify people" отключена
7. Нажмите "Share" (или "Поделиться")

## Этап 8: Настройка локального окружения

### Шаг 8.1: Создание .env файла

1. Откройте текстовый редактор (Notepad, VS Code и т.д.)
2. Создайте новый файл с содержимым:

```
BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZabcdefGHI
SPREADSHEET_ID=1ABC123dEf4GhIjK5lmNoPqRsT6uVwXyZ
```

Где:
- `BOT_TOKEN` - токен из BotFather (этап 1)
- `SPREADSHEET_ID` - ID Google Sheets (этап 6)

3. Сохраните файл как `.env` в корне проекта (рядом с bot.py)

**Внимание**: Убедитесь, что при сохранении файл называется `.env` (без расширения .txt)

## Этап 9: Установка зависимостей

### Шаг 9.1: Создание виртуального окружения

```bash
# На Windows:
python -m venv venv
venv\Scripts\activate

# На macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### Шаг 9.2: Установка пакетов

```bash
pip install -r requirements.txt
```

Это установит все необходимые библиотеки из файла requirements.txt

## Этап 10: Первый запуск

### Шаг 10.1: Запуск бота

```bash
python bot.py
```

Вы должны увидеть в консоли:

```
2024-06-20 10:00:00,123 - bot - INFO - Bot starting...
2024-06-20 10:00:01,456 - bot - INFO - Google Sheets initialized successfully
2024-06-20 10:00:02,789 - root - INFO - Started polling
```

### Шаг 10.2: Проверка работы

1. Откройте Telegram
2. Найдите вашего бота (используя имя из шага 1.2, которое должно начинаться на @)
3. Нажмите "Start"
4. Вы должны увидеть меню с кнопками:
   - ➕ Добавить клиента
   - 📊 Скачать Excel

## Этап 11: Тестирование функциональности

### Тест 1: Добавление клиента

1. Нажмите "➕ Добавить клиента"
2. Введите тестовый телефон: `+7 (123) 456-78-90`
3. Введите тестовый email: `test@example.com`
4. Введите тестовый процент: `25`
5. Вы должны увидеть сообщение: "✅ Клиент успешно добавлен!"

### Тест 2: Проверка Google Sheets

1. Откройте вашу Google Sheets таблицу в браузере
2. Вы должны увидеть добавленные данные:
   - Дата (текущая дата и время)
   - Телефон: `+7 (123) 456-78-90`
   - Email: `test@example.com`
   - Процент: `25`

### Тест 3: Скачивание Excel

1. В боте нажмите "📊 Скачать Excel"
2. Бот отправит вам файл Excel
3. Скачайте файл и откройте его
4. Вы должны увидеть красиво отформатированную таблицу с данными

## Этап 12: Развертывание на Railway (опционально)

### Шаг 12.1: Подготовка GitHub репозитория

1. Создайте новый репозиторий на GitHub
2. Клонируйте его локально:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

3. Скопируйте все файлы проекта (кроме credentials.json)
4. Добавьте .gitignore (уже в проекте)
5. Сделайте коммит:

```bash
git add .
git commit -m "Initial commit"
git push
```

### Шаг 12.2: Подключение к Railway

1. Откройте https://railway.app
2. Нажмите "Dashboard"
3. Нажмите "Create New Project"
4. Выберите "Deploy from GitHub repo"
5. Авторизуйте Railway с GitHub
6. Выберите ваш репозиторий

### Шаг 12.3: Настройка переменных окружения

1. В Railway проекте перейдите в вкладку "Variables"
2. Добавьте переменные:
   - `BOT_TOKEN` - ваш токен
   - `SPREADSHEET_ID` - ваш ID таблицы

### Шаг 12.4: Для credentials.json

1. Откройте file `credentials.json`
2. Закодируйте его в Base64:

На Windows PowerShell:
```powershell
[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("C:\path\to\credentials.json"))
```

На macOS/Linux:
```bash
base64 credentials.json | tr -d '\n'
```

3. Скопируйте весь вывод
4. В Railway добавьте переменную:
   - `CREDENTIALS_BASE64` - значение из шага 2

### Шаг 12.5: Развертывание

1. Railway автоматически развернет приложение
2. В вкладке "Logs" вы увидите логи развертывания
3. Когда развертывание завершится, ваш бот будет работать 24/7

## Часто встречающиеся проблемы и решения

### Проблема: "aiogram not found"

**Решение**: 
```bash
pip install aiogram==3.3.0
```

### Проблема: "Google Sheets не инициализировалась"

**Проверить**:
1. Существует ли файл credentials.json в корне проекта?
2. Установлена ли переменная SPREADSHEET_ID?
3. Скопирован ли email сервисного аккаунта в общий доступ таблицы?

### Проблема: "Permission denied при добавлении клиента"

**Проверить**:
1. В Google Sheets: Поделиться → проверить наличие сервис-аккаунта
2. Права должны быть "Редактор", не "Просмотр"

### Проблема: "Бот не отвечает"

**Решение**:
1. Проверить, запущен ли бот: `python bot.py`
2. Проверить логи в консоли
3. Проверить, правильно ли скопирован BOT_TOKEN
4. Перезагрузить бота: Ctrl+C и снова запустить

## Успешно! 🎉

Если вы дошли до сюда, значит ваш бот полностью настроен и работает!

### Что дальше?

1. Добавьте нескольких клиентов для теста
2. Используйте бота в своем деле
3. Рассмотрите развертывание на Railway для круглосуточной работы
4. При необходимости модифицируйте код под ваши нужды

**Удачи! 🚀**

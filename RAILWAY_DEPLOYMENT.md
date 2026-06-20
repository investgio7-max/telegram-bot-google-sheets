# Развертывание на Railway

Полное руководство по развертыванию бота на Railway для круглосуточной работы.

## Что такое Railway?

Railway - это облачная платформа для развертывания приложений. Она позволяет запускать ваше приложение 24/7 без необходимости держать компьютер включенным.

## Предварительные требования

1. Аккаунт GitHub
2. Аккаунт Railway
3. Завершенная настройка локального проекта (см. SETUP_GUIDE.md)

## Шаг 1: Подготовка GitHub репозитория

### 1.1: Создание репозитория на GitHub

1. Откройте https://github.com/new
2. Заполните форму:
   - **Repository name**: `telegram-bot-google-sheets`
   - **Description**: `Telegram Bot for managing clients via Google Sheets`
   - **Public/Private**: выберите по желанию
3. Нажмите "Create repository"

### 1.2: Загрузка кода на GitHub

В терминале в корне вашего проекта:

```bash
# Инициализация git репозитория (если еще не инициализирован)
git init

# Добавление всех файлов
git add .

# Проверка, что .gitignore исключает credentials.json и .env
git status

# Создание коммита
git commit -m "Initial commit: Telegram bot with Google Sheets integration"

# Добавление удаленного репозитория (замените на ваш URL)
git remote add origin https://github.com/YOUR-USERNAME/telegram-bot-google-sheets.git

# Отправка в GitHub
git branch -M main
git push -u origin main
```

### 1.3: Проверка на GitHub

1. Откройте https://github.com/YOUR-USERNAME/telegram-bot-google-sheets
2. Проверьте, что все файлы загружены
3. Убедитесь, что **credentials.json и .env НЕ видны** в репозитории

## Шаг 2: Регистрация на Railway

1. Откройте https://railway.app
2. Нажмите "Get Started" или "Login"
3. Выберите "Continue with GitHub" и авторизуйте доступ
4. Следуйте инструкциям для завершения регистрации

## Шаг 3: Создание нового проекта в Railway

### 3.1: Создание проекта

1. Откройте https://railway.app/dashboard
2. Нажмите на кнопку "+ New Project" (на английском может быть "Create a new project")
3. Выберите "Deploy from GitHub repo"

### 3.2: Подключение GitHub

1. Нажмите "Connect GitHub Account" (если вы впервые)
2. Авторизуйте Railway доступ к вашему GitHub
3. Выберите репозиторий `telegram-bot-google-sheets`

### 3.3: Нажмите Deploy

1. Railway начнет автоматическое развертывание
2. Вы увидите логи развертывания
3. Ожидайте завершения (может занять 2-3 минуты)

## Шаг 4: Настройка переменных окружения

### 4.1: Открытие настроек переменных

1. В Railway проекте нажмите на сервис (будет виден как `telegram-bot-google-sheets`)
2. Перейдите на вкладку "Variables" (или "Environment variables")
3. Нажмите "Add Variable"

### 4.2: Добавление BOT_TOKEN

1. **Key**: `BOT_TOKEN`
2. **Value**: ваш токен из @BotFather
3. Нажмите "Add" или "Save"

### 4.3: Добавление SPREADSHEET_ID

1. Нажмите "Add Variable" снова
2. **Key**: `SPREADSHEET_ID`
3. **Value**: ID вашей Google Sheets таблицы
4. Нажмите "Add" или "Save"

### 4.4: Добавление CREDENTIALS_BASE64 (важно!)

1. Локально закодируйте credentials.json:

На Windows PowerShell:
```powershell
[Convert]::ToBase64String([System.IO.File]::ReadAllBytes(".\credentials.json")) | Set-Clipboard
```

На macOS/Linux:
```bash
base64 credentials.json | tr -d '\n' | pbcopy  # macOS
base64 credentials.json | tr -d '\n' | xclip -selection clipboard  # Linux
```

Или используйте Python:
```bash
python -c "from utils import encode_credentials_base64; print(encode_credentials_base64())"
```

2. В Railway добавьте новую переменную:
   - **Key**: `CREDENTIALS_BASE64`
   - **Value**: вставьте закодированное значение (Ctrl+V)
3. Нажмите "Add" или "Save"

## Шаг 5: Проверка развертывания

### 5.1: Просмотр логов

1. В Railway проекте перейдите на вкладку "Logs"
2. Вы должны увидеть логи приложения
3. Ищите строку:
   ```
   Google Sheets initialized successfully
   ```
   и
   ```
   Started polling
   ```

### 5.2: Проверка работы бота

1. Откройте Telegram
2. Найдите вашего бота
3. Напишите `/start`
4. Вы должны увидеть меню

Если бот отвечает, это означает, что развертывание успешно! 🎉

## Шаг 6: Мониторинг приложения

### 6.1: Просмотр статуса

1. На странице Railway проекта вы увидите статус:
   - 🟢 **Running** - приложение работает
   - 🔴 **Failed** - ошибка при запуске
   - ⚪ **Deploying** - идет развертывание

### 6.2: Чтение логов

1. Перейдите на вкладку "Logs"
2. Используйте фильтр для поиска ошибок
3. Типичные ошибки:
   - `BOT_TOKEN environment variable not set` - не установлен токен
   - `SPREADSHEET_ID environment variable not set` - не установлен ID таблицы
   - `Failed to initialize Google Sheets` - проблема с credentials

### 6.3: Перезагрузка приложения

Если бот не отвечает:
1. На странице Railway проекта нажмите кнопку "Redeploy"
2. Выберите ветку `main`
3. Railway пересоберет и перезапустит приложение

## Шаг 7: Обновление кода

Если вы внесли изменения в код локально:

1. Сделайте коммит и отправьте в GitHub:
   ```bash
   git add .
   git commit -m "Update bot features"
   git push
   ```

2. Railway автоматически:
   - Обнаружит изменения
   - Пересоберет приложение
   - Перезапустит бота
   - Все это произойдет автоматически!

## Шаг 8: Использование Railway CLI (опционально)

Railway предоставляет CLI для управления проектом из терминала.

### 8.1: Установка Railway CLI

```bash
npm install -g @railway/cli
```

### 8.2: Логин в Railway

```bash
railway login
```

Откроется браузер для авторизации.

### 8.3: Просмотр логов

```bash
railway logs
```

Это покажет логи вашего приложения в реальном времени.

### 8.4: Просмотр переменных окружения

```bash
railway variables
```

### 8.5: Установка переменной

```bash
railway variables set BOT_TOKEN your_token_here
```

## Troubleshooting

### Проблема: "Bot not responding"

**Проверьте:**
1. Статус приложения - должен быть 🟢 Running
2. Логи - есть ли ошибки?
3. BOT_TOKEN - правильно ли скопирован?

**Решение:**
1. Нажмите "Redeploy"
2. Ждите завершения развертывания
3. Попробуйте `/start` в Telegram

### Проблема: "Google Sheets not initialized"

**Проверьте:**
1. SPREADSHEET_ID установлен?
2. CREDENTIALS_BASE64 установлен?
3. Сервис-аккаунт имеет доступ к таблице?

**Решение:**
1. Заново закодируйте credentials.json
2. Обновите CREDENTIALS_BASE64 в Railway
3. Нажмите "Redeploy"

### Проблема: "Permission denied"

**Проверьте:**
1. В Google Sheets - поделиться с сервис-аккаунтом
2. Права должны быть "Редактор"
3. Email сервис-аккаунта скопирован правильно?

**Решение:**
1. Откройте Google Sheets
2. Поделиться → добавьте email сервис-аккаунта
3. Выберите "Редактор"

### Проблема: "Application crashed"

**Проверьте логи:**
```bash
railway logs
```

**Типичные причины:**
- Синтаксическая ошибка в коде
- Отсутствует импорт модуля
- Неверная конфигурация

**Решение:**
1. Проверьте код локально
2. Тестируйте локально: `python bot.py`
3. Исправьте ошибки
4. Отправьте в GitHub
5. Railway автоматически пересоберет

## Плани затрат (Free Tier)

Railway предоставляет бесплатный tier с ограничениями:

- **Вычисления**: $5 кредитов в месяц
- **Хранилище**: 1GB
- **Рекомендуемое использование**: Для Telegram бота этого достаточно

Бот потребляет минимум ресурсов, так что свободный tier должен покрыть ваше использование.

Если вы превышаете лимит:
1. Railroad покажет предупреждение
2. Вы можете добавить платежный метод
3. Или оптимизировать расход ресурсов

## Дополнительные функции Railway

### 1: Автоматический перезапуск

По умолчанию Railway автоматически перезапускает приложение при сбое.

### 2: Логирование

Все логи хранятся в Railway. Вы можете просмотреть их:
- Через веб-интерфейс (Logs tab)
- Через CLI: `railway logs`

### 3: Metrics

На вкладке "Metrics" вы видите:
- CPU использование
- Память
- Входящий/исходящий трафик

## Что дальше?

1. **Мониторинг**: Периодически проверяйте логи
2. **Обновления**: Добавляйте новые функции и обновляйте
3. **Масштабирование**: Если нужно больше ресурсов, обновите план
4. **Backup**: Регулярно сохраняйте данные из Google Sheets

## Полезные ссылки

- [Railway Docs](https://docs.railway.app/)
- [Railway Dashboard](https://railway.app/dashboard)
- [Aiogram Docs](https://docs.aiogram.dev/)
- [Google Sheets API](https://developers.google.com/sheets)

## Успешное развертывание! 🚀

Ваш бот теперь работает 24/7 в облаке Railway!

**Не забывайте:**
- ✓ Регулярно проверять логи
- ✓ Обновлять код в GitHub
- ✓ Мониторить расход ресурсов
- ✓ Хранить credentials безопасно

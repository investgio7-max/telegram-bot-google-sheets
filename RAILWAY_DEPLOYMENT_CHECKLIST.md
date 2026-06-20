# Railway Deployment Checklist

## ✅ Что вам нужно подготовить

### 1️⃣ GitHub репозиторий
- [ ] Создан репозиторий на https://github.com/new
- [ ] Имя репозитория: `telegram-bot-google-sheets`
- [ ] Код отправлен в GitHub (git push)
- [ ] Репозиторий видим по адресу: https://github.com/YOUR_USERNAME/telegram-bot-google-sheets

### 2️⃣ Telegram Bot токен
- [ ] BOT_TOKEN от @BotFather
  - Пример: `123456789:ABCdefGHIjklmnoPQRstuvWXYZabcdefGHI`
  - Скопирован и готов вставить

### 3️⃣ Google Sheets подготовка
- [ ] SPREADSHEET_ID из URL Google Sheets
  - Пример: `1ABC123dEf4GhIjK5lmNoPqRsT6uVwXyZ`
  - Скопирован и готов вставить

### 4️⃣ Google credentials в Base64
- [ ] credentials.json закодирован в Base64
  
  На macOS/Linux:
  ```bash
  base64 credentials.json | tr -d '\n' | pbcopy
  # На Linux используйте: xclip -selection clipboard
  ```
  
  На Windows PowerShell:
  ```powershell
  [Convert]::ToBase64String([System.IO.File]::ReadAllBytes(".\credentials.json")) | Set-Clipboard
  ```
  
  Или используйте Python:
  ```bash
  cd "/Users/oleg/EXEL NEW"
  python -c "from utils import encode_credentials_base64; print(encode_credentials_base64())" | pbcopy
  ```

- [ ] CREDENTIALS_BASE64 скопирован в буфер обмена

### 5️⃣ Railway аккаунт
- [ ] Создан аккаунт на https://railway.app
- [ ] GitHub подключен к Railway

---

## 🚀 Процесс развертывания на Railway

### Шаг 1: GitHub репозиторий

```bash
# В папке проекта
cd "/Users/oleg/EXEL NEW"

# Добавить удаленный репозиторий (замените YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot-google-sheets.git
git branch -M main
git push -u origin main
```

### Шаг 2: Railway аккаунт

1. Откройте https://railway.app
2. Нажмите "Login" → "Continue with GitHub"
3. Авторизуйте Railway

### Шаг 3: Создание проекта в Railway

1. На Railway перейдите в Dashboard
2. Нажмите "+ New Project"
3. Выберите "Deploy from GitHub repo"
4. Найдите `telegram-bot-google-sheets`
5. Нажмите "Deploy"

(Railway начнет автоматическое развертывание)

### Шаг 4: Переменные окружения

Пока Railway разворачивает (это займет 2-3 минуты), подготовьте переменные:

1. В Railway перейдите в проект
2. Найдите вкладку "Variables" 
3. Добавьте переменные:

**Переменная 1: BOT_TOKEN**
- Key: `BOT_TOKEN`
- Value: `ваш_токен_из_botfather`

**Переменная 2: SPREADSHEET_ID**
- Key: `SPREADSHEET_ID`
- Value: `ваш_id_google_sheets`

**Переменная 3: CREDENTIALS_BASE64**
- Key: `CREDENTIALS_BASE64`
- Value: `ваш_base64_encoded_credentials_json`

### Шаг 5: Проверка развертывания

1. Перейдите на вкладку "Logs" в Railway
2. Ищите строки:
   ```
   Google Sheets initialized successfully
   Started polling
   ```
3. Если видите эти строки - бот работает! ✅

### Шаг 6: Тестирование

1. Откройте Telegram
2. Найдите вашего бота
3. Напишите `/start`
4. Должно появиться меню
5. Готово! 🎉

---

## 🆘 Если что-то не работает

### Ошибка: "Bot is not responding"

Проверьте в Logs (в Railway):
- BOT_TOKEN установлен правильно?
- Он начинается с цифр и содержит двоеточие?

Попробуйте:
1. Нажмите кнопку "Redeploy" в Railway
2. Ждите 1-2 минуты
3. Снова проверьте в Telegram

### Ошибка: "Google Sheets not initialized"

Проверьте в Logs:
- SPREADSHEET_ID установлен?
- CREDENTIALS_BASE64 установлен?

Попробуйте:
1. Проверьте значение в переменных
2. Нажмите "Redeploy"
3. Ждите

### Ошибка: "Permission denied"

Проверьте:
1. Email сервис-аккаунта добавлен в Google Sheets? ("Поделиться")
2. Права выставлены на "Редактор"?

Если нет:
1. Откройте Google Sheets
2. Нажмите "Поделиться"
3. Добавьте email из credentials.json
4. Нажмите Redeploy в Railway

---

## ✅ Контрольный список успешного развертывания

- [ ] GitHub репозиторий создан
- [ ] Код отправлен на GitHub (git push)
- [ ] Railway проект создан
- [ ] BOT_TOKEN добавлен в переменные
- [ ] SPREADSHEET_ID добавлен в переменные
- [ ] CREDENTIALS_BASE64 добавлен в переменные
- [ ] Logs показывают "Google Sheets initialized successfully"
- [ ] Telegram бот отвечает на /start
- [ ] Кнопки работают в Telegram
- [ ] Можно добавить клиента
- [ ] Можно скачать Excel

Если всё вышеперечисленное сделано - бот работает 24/7! 🎉

---

## 📞 Быстрые ссылки

- Railway Dashboard: https://railway.app/dashboard
- GitHub репозиторий: https://github.com/YOUR_USERNAME/telegram-bot-google-sheets
- Google Cloud Console: https://console.cloud.google.com/

---

**Готовы? Начните со шага 1 выше! 🚀**

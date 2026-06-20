# Отправка кода на GitHub

Есть несколько способов. Выберите один:

## ✅ Способ 1: Через GitHub CLI (быстро)

```bash
# Аутентифицируемся
gh auth login

# Следуйте инструкциям:
# - Выберите GitHub.com
# - Выберите HTTPS
# - Авторизуйте через браузер

# После этого отправляем код
cd "/Users/oleg/EXEL NEW"
git push -u origin main
```

## ✅ Способ 2: GitHub token (альтернатива)

1. Создайте Personal Access Token:
   - Откройте: https://github.com/settings/tokens
   - Нажмите "Generate new token"
   - Выберите "repo" (полный доступ к репозиториям)
   - Скопируйте токен

2. Используйте токен для отправки:
   ```bash
   cd "/Users/oleg/EXEL NEW"
   git remote remove origin
   git remote add origin https://YOUR_TOKEN@github.com/investgio7-max/telegram-bot-google-sheets.git
   git push -u origin main
   ```
   (замените YOUR_TOKEN на скопированный токен)

## ✅ Способ 3: Через Web UI GitHub (если срочно)

Если не хотите возиться с аутентификацией:

1. Откройте https://github.com/investgio7-max/telegram-bot-google-sheets
2. Нажмите "Add file" → "Upload files"
3. Перетащите все файлы из "/Users/oleg/EXEL NEW"
4. Напишите commit message
5. Нажмите "Commit changes"

## 🎯 Рекомендуемый способ: Способ 1

Самый простой и правильный - использовать GitHub CLI.

```bash
# 1. Аутентификация (один раз)
gh auth login

# 2. Отправка кода
cd "/Users/oleg/EXEL NEW"
git push -u origin main

# Готово! ✅
```

---

**Какой способ используете? Помогу дальше! 🚀**

#!/bin/bash

echo "🚀 Запуск Life Calendar Bot..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден! Установите Python 3.8+"
    exit 1
fi

# Проверяем наличие файла .env
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📝 Создайте файл .env с вашим BOT_TOKEN"
    echo "Пример:"
    echo "BOT_TOKEN=your_bot_token_here"
    exit 1
fi

# Проверяем зависимости
echo "📦 Проверка зависимостей..."
if ! python3 -c "import telegram, matplotlib, PIL" 2>/dev/null; then
    echo "📥 Установка зависимостей..."
    pip3 install -r requirements.txt
fi

# Запуск бота
echo "🤖 Запуск бота..."
python3 bot.py

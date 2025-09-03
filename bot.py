import logging
import os
import asyncio
from datetime import datetime, date
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from life_visualizer import LifeVisualizer
from scheduler import WeeklyReportScheduler
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Словарь для хранения дат рождения пользователей (в реальном проекте лучше использовать базу данных)
user_birth_dates = {}
# Словарь для хранения пола пользователей
user_genders = {}

class LifeBot:
    def __init__(self):
        self.visualizer = LifeVisualizer()
        self.scheduler = None
        self.channel_id = None  # Will be set via command
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
🎯 Добро пожаловать в Life Calendar Bot!

Этот бот показывает вашу жизнь в неделях, как в известной визуализации.

📋 Доступные команды:
/start - показать это сообщение
/setbirth <дата> - установить дату рождения (формат: DD.MM.YYYY)
/setgender <пол> - установить пол (male/female)
/age - показать точный возраст
/show - показать ваш календарь жизни
/week - показать информацию о текущей неделе
/percentage - показать процент прожитой жизни

🕐 **Автоматические отчеты:**
/setchannel <ID> - установить канал для еженедельных отчетов
/schedulestatus - показать статус планировщика
/help - показать справку

Пример: /setbirth 15.03.1990
Пример: /setgender male
Пример: /setchannel -1001234567890
        """
        await update.message.reply_text(welcome_text)
    
    async def set_birth(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Установка даты рождения"""
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text(
                "❌ Пожалуйста, укажите дату рождения!\n"
                "Формат: /setbirth DD.MM.YYYY\n"
                "Пример: /setbirth 15.03.1990"
            )
            return
        
        try:
            birth_date_str = context.args[0]
            birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y").date()
            
            # Проверяем, что дата не в будущем
            if birth_date > date.today():
                await update.message.reply_text("❌ Дата рождения не может быть в будущем!")
                return
            
            # Проверяем разумность даты (не старше 120 лет)
            if (date.today() - birth_date).days > 120 * 365:
                await update.message.reply_text("❌ Пожалуйста, проверьте дату рождения!")
                return
            
            user_birth_dates[user_id] = birth_date
            
            # Создаем новый визуализатор с учетом пола пользователя
            gender = user_genders.get(user_id, 'default')
            self.visualizer.set_gender(gender)
            
            await update.message.reply_text(
                f"✅ Дата рождения установлена: {birth_date.strftime('%d.%m.%Y')}\n"
                f"Пол: {self._get_gender_display(gender)}\n"
                f"Теперь используйте /show для просмотра вашего календаря жизни!"
            )
            
        except ValueError:
            await update.message.reply_text(
                "❌ Неверный формат даты!\n"
                "Используйте формат: DD.MM.YYYY\n"
                "Пример: /setbirth 15.03.1990"
            )
    
    async def set_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Установка пола пользователя"""
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text(
                "❌ Пожалуйста, укажите пол!\n"
                "Формат: /setgender <пол>\n"
                "Варианты: male (мужской) или female (женский)\n"
                "Пример: /setgender male"
            )
            return
        
        gender = context.args[0].lower()
        
        if gender not in ['male', 'female']:
            await update.message.reply_text(
                "❌ Неверный пол!\n"
                "Используйте: male (мужской) или female (женский)\n"
                "Пример: /setgender male"
            )
            return
        
        user_genders[user_id] = gender
        
        # Обновляем визуализатор
        self.visualizer.set_gender(gender)
        
        await update.message.reply_text(
            f"✅ Пол установлен: {self._get_gender_display(gender)}\n"
            f"Ожидаемая продолжительность жизни: {self.visualizer.life_expectancy_years} лет\n"
            f"Используйте /show для обновленного календаря!"
        )
    
    def _get_gender_display(self, gender):
        """Возвращает отображаемое название пола"""
        if gender == 'male':
            return 'мужской'
        elif gender == 'female':
            return 'женский'
        else:
            return 'не указан'
    
    async def show_calendar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать календарь жизни"""
        user_id = update.effective_user.id
        
        if user_id not in user_birth_dates:
            await update.message.reply_text(
                "❌ Сначала установите дату рождения!\n"
                "Используйте: /setbirth DD.MM.YYYY"
            )
            return
        
        birth_date = user_birth_dates[user_id]
        gender = user_genders.get(user_id, 'default')
        self.visualizer.set_gender(gender)
        
        # Создаем изображение
        try:
            image_path = self.visualizer.create_life_grid(birth_date)
            
            # Получаем информацию для подписи
            week_info = self.visualizer.get_week_info(birth_date)
            percentage_info = self.visualizer.get_life_percentage(birth_date)
            
            # Создаем красивую подпись
            caption = f"""🎯 **Your Life Calendar**

📅 **Birth Date:** {birth_date.strftime('%B %d, %Y')}
👤 **Gender:** {self._get_gender_display(gender)}
📊 **Life Expectancy:** {week_info['life_expectancy']} years

📈 **Current Status:**
• Age: {week_info['age_years']} years, {week_info['week_in_year']} weeks
• Weeks Lived: {week_info['total_weeks']:,}
• Weeks Remaining: {week_info['weeks_remaining']:,}
• Life Progress: {percentage_info['percentage']:.1f}%

🔴 Red squares = Weeks you've lived
⚪ White squares = Weeks ahead of you

💡 Each square represents 1 week of your life"""
            
            # Отправляем изображение
            with open(image_path, 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode='Markdown'
                )
            
            # Удаляем временный файл
            os.remove(image_path)
            
        except Exception as e:
            logger.error(f"Ошибка при создании изображения: {e}")
            await update.message.reply_text("❌ Произошла ошибка при создании изображения")
    
    async def week_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать информацию о текущей неделе"""
        user_id = update.effective_user.id
        
        if user_id not in user_birth_dates:
            await update.message.reply_text(
                "❌ Сначала установите дату рождения!\n"
                "Используйте: /setbirth DD.MM.YYYY"
            )
            return
        
        birth_date = user_birth_dates[user_id]
        gender = user_genders.get(user_id, 'default')
        self.visualizer.set_gender(gender)
        week_info = self.visualizer.get_week_info(birth_date)
        
        message = f"""
📊 Информация о вашей жизни:

🎂 Дата рождения: {birth_date.strftime('%d.%m.%Y')}
👤 Пол: {self._get_gender_display(gender)}
📅 Текущий возраст: {week_info['age_years']} лет, {week_info['week_in_year']} недель
✅ Прожито недель: {week_info['total_weeks']:,}
⏳ Осталось недель: {week_info['weeks_remaining']:,}
🎯 Всего недель в жизни: {week_info['total_weeks'] + week_info['weeks_remaining']:,}
📈 Ожидаемая продолжительность: {week_info['life_expectancy']} лет

💡 Используйте /show для просмотра визуального календаря!
        """
        
        await update.message.reply_text(message)
    
    async def show_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать точный возраст"""
        user_id = update.effective_user.id
        
        if user_id not in user_birth_dates:
            await update.message.reply_text(
                "❌ Сначала установите дату рождения!\n"
                "Используйте: /setbirth DD.MM.YYYY"
            )
            return
        
        birth_date = user_birth_dates[user_id]
        age_info = self.visualizer.calculate_age(birth_date)
        
        message = f"""
🎂 Ваш точный возраст:

📅 Дата рождения: {birth_date.strftime('%d.%m.%Y')}
⏰ Текущая дата: {date.today().strftime('%d.%m.%Y')}

📊 Возраст:
   • {age_info['years']} лет
   • {age_info['months']} месяцев  
   • {age_info['days']} дней

📈 Всего:
   • {age_info['total_days']:,} дней
   • {age_info['total_weeks']:,} недель

💡 Используйте /percentage для просмотра процента прожитой жизни!
        """
        
        await update.message.reply_text(message)
    
    async def show_percentage(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать процент прожитой жизни"""
        user_id = update.effective_user.id
        
        if user_id not in user_birth_dates:
            await update.message.reply_text(
                "❌ Сначала установите дату рождения!\n"
                "Используйте: /setbirth DD.MM.YYYY"
            )
            return
        
        birth_date = user_birth_dates[user_id]
        gender = user_genders.get(user_id, 'default')
        self.visualizer.set_gender(gender)
        percentage_info = self.visualizer.get_life_percentage(birth_date)
        
        # Создаем визуальную шкалу прогресса
        progress_bar = self._create_progress_bar(percentage_info['percentage'])
        
        message = f"""
📊 Процент прожитой жизни:

🎂 Дата рождения: {birth_date.strftime('%d.%m.%Y')}
👤 Пол: {self._get_gender_display(gender)}
📈 Ожидаемая продолжительность: {self.visualizer.life_expectancy_years} лет

{progress_bar}

📊 Статистика:
   • Прожито: {percentage_info['weeks_lived']:,} недель
   • Осталось: {percentage_info['weeks_remaining']:,} недель
   • Всего: {percentage_info['total_weeks']:,} недель
   • Процент: {percentage_info['percentage']}%

💡 Используйте /show для просмотра визуального календаря!
        """
        
        await update.message.reply_text(message)
    
    def _create_progress_bar(self, percentage):
        """Создает текстовую шкалу прогресса"""
        filled_length = int(percentage / 5)  # 5% на символ
        empty_length = 20 - filled_length
        
        filled = '█' * filled_length
        empty = '░' * empty_length
        
        return f"Прогресс: [{filled}{empty}] {percentage}%"
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать справку"""
        help_text = """
📚 Справка по Life Calendar Bot

🎯 Что делает бот:
Этот бот создает визуализацию вашей жизни в неделях, показывая сколько недель вы уже прожили и сколько осталось.

📋 Основные команды:
/start - начать работу с ботом
/setbirth <дата> - установить дату рождения
/setgender <пол> - установить пол (male/female)
/age - показать точный возраст
/show - показать календарь жизни
/week - показать статистику по неделям
/percentage - показать процент прожитой жизни

🕐 **Автоматические отчеты:**
/setchannel <ID> - установить канал для еженедельных отчетов
/schedulestatus - показать статус планировщика
/help - показать эту справку

📅 Формат даты:
Используйте формат DD.MM.YYYY
Пример: 15.03.1990

👤 Установка пола:
Используйте: male (мужской) или female (женский)
Пример: /setgender male

💡 Особенности:
• Пол влияет на ожидаемую продолжительность жизни
• Мужчины: 75 лет, Женщины: 82 года
• По умолчанию: 80 лет
• Установите дату рождения и пол один раз!

🎨 Визуализация:
• Красные квадраты = прожитые недели
• Серые квадраты = будущие недели
• Каждый квадрат = 1 неделя жизни
        """
        await update.message.reply_text(help_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик обычных сообщений"""
        await update.message.reply_text(
            "🤖 Я понимаю только команды!\n"
            "Используйте /start для начала работы или /help для справки."
        )
    
    async def set_channel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Установка канала для еженедельных отчетов"""
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text(
                "❌ Пожалуйста, укажите ID канала!\n"
                "Формат: /setchannel <ID_канала>\n"
                "Пример: /setchannel -1001234567890\n\n"
                "💡 Как получить ID канала:\n"
                "1. Добавьте @userinfobot в ваш канал\n"
                "2. Скопируйте ID (начинается с -100)"
            )
            return
        
        try:
            channel_id = context.args[0]
            
            # Проверяем формат ID канала (должен начинаться с -100)
            if not channel_id.startswith('-100'):
                await update.message.reply_text(
                    "❌ Неверный формат ID канала!\n"
                    "ID канала должен начинаться с -100\n"
                    "Пример: -1001234567890"
                )
                return
            
            # Сохраняем ID канала
            self.channel_id = channel_id
            
            # Инициализируем планировщик если еще не создан
            if not self.scheduler:
                self.scheduler = WeeklyReportScheduler(BOT_TOKEN, channel_id)
                self.scheduler.start_scheduler()
                await update.message.reply_text(
                    f"✅ Канал установлен: {channel_id}\n"
                    f"🕐 Планировщик запущен!\n"
                    f"📅 Отчеты будут отправляться каждый понедельник в 00:00 по португальскому времени\n"
                    f"🌍 Время: Europe/Lisbon (Португалия)"
                )
            else:
                # Обновляем существующий планировщик
                self.scheduler.channel_id = channel_id
                await update.message.reply_text(
                    f"✅ Канал обновлен: {channel_id}\n"
                    f"🕐 Планировщик продолжает работать\n"
                    f"📅 Следующий отчет: каждый понедельник в 00:00 (Португалия)"
                )
                
        except Exception as e:
            logger.error(f"Ошибка при установке канала: {e}")
            await update.message.reply_text("❌ Произошла ошибка при установке канала")
    
    async def scheduler_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статус планировщика"""
        if not self.scheduler:
            await update.message.reply_text(
                "🕐 **Статус планировщика:**\n\n"
                "❌ Планировщик не запущен\n"
                "💡 Используйте /setchannel для настройки автоматических отчетов"
            )
            return
        
        try:
            status = self.scheduler.get_scheduler_status()
            
            if 'error' in status:
                await update.message.reply_text(f"❌ Ошибка получения статуса: {status['error']}")
                return
            
            next_run = status['next_run']
            next_run_str = next_run.strftime('%A, %d %B %Y at %H:%M') if next_run else "Не определено"
            
            message = f"""🕐 **Статус планировщика:**

✅ **Состояние:** {'Работает' if status['running'] else 'Остановлен'}
📅 **Расписание:** {status['schedule']}
🌍 **Часовой пояс:** {status['timezone']}
📊 **Задач:** {status['job_count']}
⏰ **Следующий запуск:** {next_run_str}

💡 **Автоматические отчеты:**
• Отправляются каждый понедельник в 00:00
• Время: Португалия (Europe/Lisbon)
• Канал: {self.channel_id or 'Не установлен'}"""
            
            await update.message.reply_text(message)
            
        except Exception as e:
            logger.error(f"Ошибка при получении статуса планировщика: {e}")
            await update.message.reply_text("❌ Произошла ошибка при получении статуса")

def main():
    """Главная функция"""
    if not BOT_TOKEN:
        logger.error("Не установлен BOT_TOKEN в переменных окружения!")
        return
    
    # Создаем бота
    bot = LifeBot()
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("setbirth", bot.set_birth))
    application.add_handler(CommandHandler("setgender", bot.set_gender))
    application.add_handler(CommandHandler("age", bot.show_age))
    application.add_handler(CommandHandler("show", bot.show_calendar))
    application.add_handler(CommandHandler("week", bot.week_info))
    application.add_handler(CommandHandler("percentage", bot.show_percentage))
    application.add_handler(CommandHandler("setchannel", bot.set_channel))
    application.add_handler(CommandHandler("schedulestatus", bot.scheduler_status))
    application.add_handler(CommandHandler("help", bot.help_command))
    
    # Обработчик обычных сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Запускаем бота
    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

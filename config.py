import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Life parameters
LIFE_EXPECTANCY_YEARS_MALE = 75    # средняя продолжительность жизни мужчин
LIFE_EXPECTANCY_YEARS_FEMALE = 82  # средняя продолжительность жизни женщин
LIFE_EXPECTANCY_YEARS_DEFAULT = 80 # по умолчанию
WEEKS_PER_YEAR = 52

# Visualization settings
GRID_COLUMNS = 52  # weeks per year
GRID_ROWS = LIFE_EXPECTANCY_YEARS_DEFAULT
CELL_SIZE = 8
DPI = 100

# Colors
COMPLETED_WEEK_COLOR = '#FF6B6B'  # красный для прожитых недель
FUTURE_WEEK_COLOR = '#F8F9FA'     # светло-серый для будущих недель
GRID_COLOR = '#E9ECEF'            # цвет сетки
TEXT_COLOR = '#495057'             # цвет текста

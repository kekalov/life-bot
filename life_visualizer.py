import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, date
import math
from config import *

class LifeVisualizer:
    def __init__(self, gender='default'):
        self.gender = gender
        self.life_expectancy_years = self._get_life_expectancy(gender)
        self.weeks_per_year = WEEKS_PER_YEAR
        self.grid_columns = GRID_COLUMNS
        self.grid_rows = self.life_expectancy_years
        self.cell_size = CELL_SIZE
        self.dpi = DPI
    
    def _get_life_expectancy(self, gender):
        """Возвращает ожидаемую продолжительность жизни в зависимости от пола"""
        if gender == 'male':
            return LIFE_EXPECTANCY_YEARS_MALE
        elif gender == 'female':
            return LIFE_EXPECTANCY_YEARS_FEMALE
        else:
            return LIFE_EXPECTANCY_YEARS_DEFAULT
    
    def set_gender(self, gender):
        """Устанавливает пол и пересчитывает параметры"""
        self.gender = gender
        self.life_expectancy_years = self._get_life_expectancy(gender)
        self.grid_rows = self.life_expectancy_years
        
    def calculate_weeks_lived(self, birth_date):
        """Вычисляет количество прожитых недель"""
        today = date.today()
        delta = today - birth_date
        weeks = math.floor(delta.days / 7)
        return max(0, weeks)
    
    def create_life_grid(self, birth_date, output_path="life_grid.png"):
        """Создает визуализацию жизни в неделях"""
        weeks_lived = self.calculate_weeks_lived(birth_date)
        
        # Создаем фигуру с оптимальными размерами для Telegram
        fig, ax = plt.subplots(figsize=(14, 12), dpi=self.dpi)
        
        # Настройки осей с запасом для текста
        ax.set_xlim(-2, self.grid_columns + 2)
        ax.set_ylim(-12, self.grid_rows + 3)
        
        # Убираем оси
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Рисуем сетку недель
        for row in range(self.grid_rows):
            for col in range(self.grid_columns):
                week_number = row * self.grid_columns + col
                
                if week_number < weeks_lived:
                    # Прожитая неделя - красный квадрат
                    rect = patches.Rectangle(
                        (col, self.grid_rows - 1 - row), 
                        1, 1, 
                        facecolor=COMPLETED_WEEK_COLOR,
                        edgecolor=GRID_COLOR,
                        linewidth=0.5
                    )
                else:
                    # Будущая неделя - пустой квадрат
                    rect = patches.Rectangle(
                        (col, self.grid_rows - 1 - row), 
                        1, 1, 
                        facecolor=FUTURE_WEEK_COLOR,
                        edgecolor=GRID_COLOR,
                        linewidth=0.5
                    )
                
                ax.add_patch(rect)
        
        # Добавляем подписи осей
        ax.text(-1.5, self.grid_rows / 2, 'AGE\nВОЗРАСТ', 
                rotation=90, ha='center', va='center', 
                fontsize=14, color=TEXT_COLOR, fontweight='bold')
        
        ax.text(self.grid_columns / 2, -1, 'WEEK OF THE YEAR', 
                ha='center', va='center', 
                fontsize=14, color=TEXT_COLOR, fontweight='bold')
        
        # Добавляем заголовок
        ax.text(self.grid_columns / 2, self.grid_rows + 2, 
                f'A {self.life_expectancy_years}-YEAR HUMAN LIFE IN WEEKS', 
                ha='center', va='center', 
                fontsize=18, color=TEXT_COLOR, fontweight='bold')
        
        # Добавляем статистику жизни
        current_age = weeks_lived // self.weeks_per_year
        current_week_in_year = weeks_lived % self.weeks_per_year
        total_weeks = self.life_expectancy_years * self.weeks_per_year
        weeks_remaining = total_weeks - weeks_lived
        life_percentage = (weeks_lived / total_weeks) * 100
        
        # Создаем красивую статистику
        stats_text = f"LIFE STATISTICS\n"
        stats_text += f"Current Age: {current_age} years, {current_week_in_year} weeks\n"
        stats_text += f"Weeks Lived: {weeks_lived:,}\n"
        stats_text += f"Weeks Remaining: {weeks_remaining:,}\n"
        stats_text += f"Life Progress: {life_percentage:.1f}%"
        
        ax.text(self.grid_columns / 2, -3, stats_text, 
                ha='center', va='center', 
                fontsize=11, color=TEXT_COLOR, fontweight='normal',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='#f8f9fa', edgecolor='#dee2e6', alpha=0.8))
        
        # Добавляем легенду
        legend_text = "Red squares = Weeks lived\nWhite squares = Weeks remaining"
        ax.text(self.grid_columns / 2, -6, legend_text, 
                ha='center', va='center', 
                fontsize=10, color=TEXT_COLOR, fontweight='normal',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='#e9ecef', edgecolor='#ced4da', alpha=0.8))
        
        # Добавляем подпись бота
        ax.text(self.grid_columns / 2, -9, 
                "Get this visualization every week: @your_bot_username", 
                ha='center', va='center', 
                fontsize=9, color=TEXT_COLOR, style='italic',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#f1f3f4', edgecolor='#dadce0', alpha=0.8))
        
        # Добавляем дату создания
        creation_date = date.today().strftime("%B %d, %Y")
        ax.text(self.grid_columns / 2, -11, 
                f"Generated on {creation_date}", 
                ha='center', va='center', 
                fontsize=8, color='#6c757d', style='italic')
        
        # Настройки макета
        plt.tight_layout()
        
        # Сохраняем изображение с высоким качеством
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', 
                   pad_inches=0.2)
        plt.close()
        
        return output_path
    
    def get_week_info(self, birth_date):
        """Возвращает информацию о текущей неделе"""
        weeks_lived = self.calculate_weeks_lived(birth_date)
        current_age = weeks_lived // self.weeks_per_year
        current_week_in_year = weeks_lived % self.weeks_per_year
        
        return {
            'total_weeks': weeks_lived,
            'age_years': current_age,
            'week_in_year': current_week_in_year,
            'weeks_remaining': (self.life_expectancy_years * self.weeks_per_year) - weeks_lived,
            'gender': self.gender,
            'life_expectancy': self.life_expectancy_years
        }
    
    def calculate_age(self, birth_date):
        """Вычисляет точный возраст в годах, месяцах и днях"""
        today = date.today()
        delta = today - birth_date
        
        years = delta.days // 365
        remaining_days = delta.days % 365
        
        # Примерный расчет месяцев (не очень точный, но простой)
        months = remaining_days // 30
        days = remaining_days % 30
        
        return {
            'years': years,
            'months': months,
            'days': days,
            'total_days': delta.days,
            'total_weeks': self.calculate_weeks_lived(birth_date)
        }
    
    def get_life_percentage(self, birth_date):
        """Вычисляет процент прожитой жизни"""
        weeks_lived = self.calculate_weeks_lived(birth_date)
        total_weeks = self.life_expectancy_years * self.weeks_per_year
        percentage = (weeks_lived / total_weeks) * 100
        
        return {
            'percentage': round(percentage, 2),
            'weeks_lived': weeks_lived,
            'total_weeks': total_weeks,
            'weeks_remaining': total_weeks - weeks_lived
        }

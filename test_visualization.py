#!/usr/bin/env python3
"""
Тестовый скрипт для проверки генерации визуализации жизни
"""

import os
from datetime import date
from life_visualizer import LifeVisualizer

def test_visualization():
    """Тестирует генерацию визуализации"""
    print("🎯 Тестирование генератора визуализации жизни...")
    
    # Тестируем разные полы
    genders = ['default', 'male', 'female']
    
    for gender in genders:
        print(f"\n👤 Тестирование для пола: {gender}")
        
        # Создаем визуализатор
        visualizer = LifeVisualizer(gender)
        
        # Тестовая дата рождения (например, 15 марта 1990)
        test_birth_date = date(1990, 3, 15)
        
        print(f"📅 Тестовая дата рождения: {test_birth_date.strftime('%d.%m.%Y')}")
        print(f"📈 Ожидаемая продолжительность жизни: {visualizer.life_expectancy_years} лет")
        
        # Получаем информацию о неделях
        week_info = visualizer.get_week_info(test_birth_date)
        
        print(f"📊 Информация о жизни:")
        print(f"   Возраст: {week_info['age_years']} лет, {week_info['week_in_year']} недель")
        print(f"   Прожито недель: {week_info['total_weeks']:,}")
        print(f"   Осталось недель: {week_info['weeks_remaining']:,}")
        
        # Получаем точный возраст
        age_info = visualizer.calculate_age(test_birth_date)
        print(f"   Точный возраст: {age_info['years']} лет, {age_info['months']} месяцев, {age_info['days']} дней")
        
        # Получаем процент жизни
        percentage_info = visualizer.get_life_percentage(test_birth_date)
        print(f"   Процент прожитой жизни: {percentage_info['percentage']}%")
        
        # Создаем изображение
        print("🎨 Создание изображения...")
        try:
            image_path = visualizer.create_life_grid(test_birth_date, f"test_life_grid_{gender}.png")
            print(f"✅ Изображение создано: {image_path}")
            print(f"   Размер файла: {os.path.getsize(image_path)} байт")
        except Exception as e:
            print(f"❌ Ошибка при создании изображения: {e}")
    
    print("\n🎉 Тест завершен!")
    print("\n📱 Готово для отправки в Telegram канал!")
    print("   - Красивая визуализация с английскими подписями")
    print("   - Статистика в отдельных блоках")
    print("   - Легенда и дата создания")
    print("   - Оптимальные размеры для мобильных устройств")

if __name__ == "__main__":
    test_visualization()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Автоматическая настройка PostgreSQL с использованием стандартного пользователя postgres
"""

import os
import sys
import django
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database_only():
    """Создание только базы данных без нового пользователя"""
    
    print("АВТОМАТИЧЕСКАЯ НАСТРОЙКА POSTGRESQL")
    print("=" * 45)
    
    # Запрашиваем пароль postgres
    postgres_password = input("Введите пароль пользователя postgres: ")
    
    try:
        # Подключаемся к PostgreSQL как postgres
        print("\nПодключаемся к PostgreSQL...")
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',
            password=postgres_password,
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Проверяем, существует ли база данных
        cursor.execute("""
            SELECT 1 FROM pg_catalog.pg_database 
            WHERE datname = 'pets_shelter_db'
        """)
        
        if cursor.fetchone():
            print("[WARNING] База данных 'pets_shelter_db' уже существует")
            recreate = input("Пересоздать базу данных? (y/n): ").lower()
            if recreate == 'y':
                # Закрываем все соединения с базой
                cursor.execute("""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = 'pets_shelter_db' AND pid <> pg_backend_pid()
                """)
                
                # Удаляем базу данных
                cursor.execute("DROP DATABASE pets_shelter_db")
                print("[OK] Старая база данных удалена")
        
        # Создаем базу данных
        if not cursor.fetchone() or recreate == 'y':
            print("Создаем базу данных 'pets_shelter_db'...")
            cursor.execute("""
                CREATE DATABASE pets_shelter_db 
                OWNER postgres 
                ENCODING 'UTF8'
            """)
            print("[OK] База данных создана")
        
        cursor.close()
        conn.close()
        
        # Тестируем подключение к новой базе
        print("\nТестируем подключение к базе данных...")
        test_conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='pets_shelter_db',
            user='postgres',
            password=postgres_password
        )
        
        test_cursor = test_conn.cursor()
        test_cursor.execute('SELECT version();')
        version = test_cursor.fetchone()
        
        print(f"[OK] Подключение успешно!")
        print(f"Версия PostgreSQL: {version[0][:50]}...")
        
        test_cursor.close()
        test_conn.close()
        
        # Создаем .env файл с настройками
        env_content = f"""# Django настройки
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL настройки
DB_NAME=pets_shelter_db
DB_USER=postgres
DB_PASSWORD={postgres_password}
DB_HOST=localhost
DB_PORT=5432

# Медиа файлы
MEDIA_URL=/media/
MEDIA_ROOT=media/

# Google OAuth настройки (заполните после настройки Google Console)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
"""
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n[OK] Файл .env создан с настройками подключения")
        
        print("\nБАЗА ДАННЫХ ГОТОВА!")
        print("=" * 45)
        print("Параметры подключения:")
        print("  База данных: pets_shelter_db")
        print("  Пользователь: postgres")
        print("  Хост: localhost")
        print("  Порт: 5432")
        
        return True
        
    except psycopg2.Error as e:
        print(f"[ERROR] Ошибка PostgreSQL: {e}")
        print("\nВозможные причины:")
        print("- Неправильный пароль")
        print("- PostgreSQL не запущен")
        print("- Неправильные настройки подключения")
        return False
    except Exception as e:
        print(f"[ERROR] Общая ошибка: {e}")
        return False

def setup_django():
    """Настройка Django после создания базы данных"""
    
    print("\nНАСТРОЙКА DJANGO")
    print("=" * 20)
    
    # Настройка Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    django.setup()
    
    try:
        from django.core.management import call_command
        
        # Создаем миграции
        print("Создаем миграции...")
        call_command('makemigrations', 'game', verbosity=1)
        print("[OK] Миграции созданы")
        
        # Применяем миграции
        print("Применяем миграции...")
        call_command('migrate', verbosity=1)
        print("[OK] Миграции применены")
        
        # Создаем базовые данные
        print("Создаем базовые данные...")
        create_initial_data()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка настройки Django: {e}")
        return False

def create_initial_data():
    """Создание начальных данных"""
    
    from game.models import PetType, Shelter, PaymentInfo
    
    # Создаем типы питомцев
    pet_types = ['Собака', 'Кошка', 'Кролик', 'Птица', 'Другое']
    for pet_type_name in pet_types:
        pet_type, created = PetType.objects.get_or_create(name=pet_type_name)
        if created:
            print(f"  [OK] Создан тип питомца: {pet_type_name}")
    
    # Создаем приют
    shelter, created = Shelter.objects.get_or_create(
        name="Приют для животных",
        defaults={
            'address': 'г. Москва, ул. Примерная, д. 1',
            'phone': '+7 (495) 123-45-67',
            'email': 'info@shelter.ru'
        }
    )
    if created:
        print(f"  [OK] Создан приют: {shelter.name}")
    
    # Создаем способы оплаты
    payment_methods = [
        {
            'name': 'Карта Сбербанк',
            'type': 'bank_card',
            'details': '1234 5678 9012 3456',
            'description': 'Карта Сбербанка для пожертвований'
        },
        {
            'name': 'СБП',
            'type': 'sbp',
            'details': '+7 (900) 123-45-67',
            'description': 'Система быстрых платежей'
        },
        {
            'name': 'ЮMoney',
            'type': 'yoomoney',
            'details': '410012345678901',
            'description': 'Кошелек ЮMoney'
        }
    ]
    
    for method_data in payment_methods:
        method, created = PaymentInfo.objects.get_or_create(
            name=method_data['name'],
            defaults=method_data
        )
        if created:
            print(f"  [OK] Создан способ оплаты: {method.name}")
    
    print("[OK] Базовые данные созданы")

def main():
    """Основная функция"""
    
    # Шаг 1: Создаем базу данных
    if not create_database_only():
        return
    
    # Шаг 2: Настраиваем Django
    if not setup_django():
        return
    
    # Шаг 3: Предлагаем создать суперпользователя
    print("\nСОЗДАНИЕ СУПЕРПОЛЬЗОВАТЕЛЯ")
    print("=" * 30)
    create_superuser = input("Создать суперпользователя для админки? (y/n): ").lower()
    if create_superuser == 'y':
        try:
            from django.core.management import call_command
            call_command('createsuperuser')
            print("[OK] Суперпользователь создан")
        except Exception as e:
            print(f"[ERROR] Ошибка создания суперпользователя: {e}")
    
    print("\nНАСТРОЙКА ЗАВЕРШЕНА!")
    print("=" * 45)
    print("[OK] PostgreSQL база данных готова")
    print("[OK] Django настроен")
    print("[OK] Базовые данные созданы")
    
    print("\nЧто дальше:")
    print("1. Запустите сервер: python manage.py runserver")
    print("2. Откройте http://localhost:8000")
    print("3. Войдите в админку: http://localhost:8000/admin/")
    print("4. Добавьте питомцев и их фотографии")
    
    print("\nДОПОЛНИТЕЛЬНО:")
    print("Для настройки входа через Google:")
    print("python setup_google_oauth.py")

if __name__ == '__main__':
    main()
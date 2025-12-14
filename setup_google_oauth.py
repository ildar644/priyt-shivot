#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Настройка Google OAuth для Django проекта
"""

import os
import sys
import django

def setup_google_oauth():
    """Настройка Google OAuth"""
    
    print("НАСТРОЙКА GOOGLE OAUTH")
    print("=" * 30)
    
    print("\n1. Получение Google OAuth ключей")
    print("Перейдите на: https://console.developers.google.com/")
    print("Создайте новый проект или выберите существующий")
    print("Включите Google+ API")
    print("Создайте OAuth 2.0 Client ID")
    print("Добавьте redirect URI: http://localhost:8000/accounts/google/login/callback/")
    
    client_id = input("\nВведите Google Client ID: ").strip()
    client_secret = input("Введите Google Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("[ERROR] Client ID и Client Secret обязательны!")
        return False
    
    # Создаем .env файл
    env_content = f"""# Django настройки
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL настройки
DB_NAME=pets_shelter_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Медиа файлы
MEDIA_URL=/media/
MEDIA_ROOT=media/

# Google OAuth настройки
GOOGLE_OAUTH_CLIENT_ID={client_id}
GOOGLE_OAUTH_CLIENT_SECRET={client_secret}
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("\n[OK] Файл .env создан с Google OAuth настройками")
    
    # Настройка Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    django.setup()
    
    try:
        from django.core.management import call_command
        from django.contrib.sites.models import Site
        
        # Применяем миграции
        print("\n2. Применение миграций...")
        call_command('migrate', verbosity=0)
        print("[OK] Миграции применены")
        
        # Создаем или обновляем Site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'Pets Shelter Local'
            }
        )
        if created:
            print("[OK] Site создан")
        else:
            site.domain = 'localhost:8000'
            site.name = 'Pets Shelter Local'
            site.save()
            print("[OK] Site обновлен")
        
        print("[OK] Google OAuth настроен через переменные окружения")
        
        print("\n3. НАСТРОЙКА ЗАВЕРШЕНА!")
        print("=" * 30)
        print("[OK] Google OAuth готов к использованию")
        print("\nТеперь пользователи могут:")
        print("- Входить через Google")
        print("- Регистрироваться через Google")
        print("- Использовать обычную регистрацию")
        
        print("\nЗапустите сервер:")
        print("python manage.py runserver")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка настройки Django: {e}")
        return False

def show_google_console_instructions():
    """Показать подробные инструкции по настройке Google Console"""
    
    print("\nПОДРОБНЫЕ ИНСТРУКЦИИ ПО GOOGLE CONSOLE:")
    print("=" * 50)
    
    print("\n1. Перейдите на https://console.developers.google.com/")
    print("2. Создайте новый проект или выберите существующий")
    print("3. В меню слева выберите 'APIs & Services' > 'Credentials'")
    print("4. Нажмите '+ CREATE CREDENTIALS' > 'OAuth client ID'")
    print("5. Выберите 'Web application'")
    print("6. Заполните поля:")
    print("   - Name: Pets Shelter")
    print("   - Authorized redirect URIs:")
    print("     http://localhost:8000/accounts/google/login/callback/")
    print("7. Нажмите 'Create'")
    print("8. Скопируйте Client ID и Client Secret")
    
    print("\nВАЖНО:")
    print("- Не делитесь Client Secret с другими")
    print("- Для продакшена добавьте свой домен в redirect URIs")
    print("- Включите Google+ API если потребуется")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        show_google_console_instructions()
    else:
        setup_google_oauth()
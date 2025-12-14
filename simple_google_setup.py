#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Простая настройка Google OAuth - только создание .env файла
"""

def simple_google_setup():
    """Простая настройка Google OAuth"""
    
    print("ПРОСТАЯ НАСТРОЙКА GOOGLE OAUTH")
    print("=" * 35)
    
    print("\n1. Получение Google OAuth ключей")
    print("Перейдите на: https://console.developers.google.com/")
    print("Создайте OAuth 2.0 Client ID (тип: Web application)")
    print("Добавьте redirect URI: http://localhost:8000/accounts/google/login/callback/")
    
    client_id = input("\nВведите Google Client ID: ").strip()
    client_secret = input("Введите Google Client Secret: ").strip()
    
    if not client_id:
        print("[ERROR] Client ID обязателен!")
        return False
    
    if not client_secret:
        print("[ERROR] Client Secret обязателен!")
        print("Убедитесь, что создали 'Web application', а не 'Desktop application'")
        return False
    
    # Читаем существующий .env или создаем новый
    env_content = ""
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            env_content = f.read()
    except FileNotFoundError:
        # Создаем базовый .env файл
        env_content = """# Django настройки
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

"""
    
    # Добавляем или обновляем Google OAuth настройки
    if 'GOOGLE_OAUTH_CLIENT_ID' in env_content:
        # Обновляем существующие
        lines = env_content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('GOOGLE_OAUTH_CLIENT_ID='):
                new_lines.append(f'GOOGLE_OAUTH_CLIENT_ID={client_id}')
            elif line.startswith('GOOGLE_OAUTH_CLIENT_SECRET='):
                new_lines.append(f'GOOGLE_OAUTH_CLIENT_SECRET={client_secret}')
            else:
                new_lines.append(line)
        env_content = '\n'.join(new_lines)
    else:
        # Добавляем новые
        env_content += f"""
# Google OAuth настройки
GOOGLE_OAUTH_CLIENT_ID={client_id}
GOOGLE_OAUTH_CLIENT_SECRET={client_secret}
"""
    
    # Сохраняем .env файл
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("\n[OK] Файл .env обновлен с Google OAuth настройками")
    
    print("\n2. НАСТРОЙКА ЗАВЕРШЕНА!")
    print("=" * 35)
    print("[OK] Google OAuth ключи сохранены в .env")
    
    print("\nТеперь:")
    print("1. Установите зависимости: pip install -r requirements.txt")
    print("2. Примените миграции: python manage.py migrate")
    print("3. Запустите сервер: python manage.py runserver")
    print("4. Откройте http://localhost:8000/accounts/login/")
    print("5. Нажмите 'Войти через Google'")
    
    return True

if __name__ == '__main__':
    simple_google_setup()
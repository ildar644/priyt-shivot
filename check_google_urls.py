#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Проверка URL для Google OAuth
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.urls import reverse
from django.conf import settings

def check_google_urls():
    """Проверка URL для Google OAuth"""
    
    print("ПРОВЕРКА GOOGLE OAUTH URL")
    print("=" * 30)
    
    try:
        # Получаем URL для Google callback
        callback_url = reverse('google_login_callback')
        print(f"Django callback URL: {callback_url}")
        
        # Полные URL для разных хостов
        hosts = ['localhost:8000', '127.0.0.1:8000']
        
        print("\nДобавьте ВСЕ эти URL в Google Console:")
        print("(APIs & Services → Credentials → OAuth Client ID → Authorized redirect URIs)")
        print()
        
        for host in hosts:
            full_url = f"http://{host}{callback_url}"
            print(f"✓ {full_url}")
        
        print("\nТакже попробуйте без слеша в конце:")
        for host in hosts:
            full_url = f"http://{host}{callback_url.rstrip('/')}"
            print(f"✓ {full_url}")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        
        # Показываем стандартные URL
        print("\nИспользуйте эти стандартные URL:")
        standard_urls = [
            "http://localhost:8000/accounts/google/login/callback/",
            "http://127.0.0.1:8000/accounts/google/login/callback/",
            "http://localhost:8000/accounts/google/login/callback",
            "http://127.0.0.1:8000/accounts/google/login/callback",
        ]
        
        for url in standard_urls:
            print(f"✓ {url}")
    
    print("\nПОСЛЕ ДОБАВЛЕНИЯ URL В GOOGLE CONSOLE:")
    print("1. Подождите 5-10 минут (Google кеширует настройки)")
    print("2. Перезапустите Django сервер")
    print("3. Попробуйте войти через Google снова")
    
    print(f"\nТекущие настройки Django:")
    print(f"SITE_ID: {getattr(settings, 'SITE_ID', 'не установлен')}")
    print(f"DEBUG: {getattr(settings, 'DEBUG', 'не установлен')}")
    print(f"ALLOWED_HOSTS: {getattr(settings, 'ALLOWED_HOSTS', 'не установлен')}")

if __name__ == '__main__':
    check_google_urls()
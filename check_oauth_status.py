#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Проверка статуса Google OAuth
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

def check_oauth_status():
    """Проверка статуса Google OAuth"""
    
    print("ПРОВЕРКА СТАТУСА GOOGLE OAUTH")
    print("=" * 35)
    
    try:
        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site
        
        # Проверяем сайты
        sites = Site.objects.all()
        print(f"Сайты в базе данных: {sites.count()}")
        for site in sites:
            print(f"  - ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
        
        # Проверяем Google приложения
        google_apps = SocialApp.objects.filter(provider='google')
        print(f"\nGoogle OAuth приложения: {google_apps.count()}")
        
        if google_apps.exists():
            for app in google_apps:
                print(f"  - Название: {app.name}")
                print(f"  - Provider: {app.provider}")
                print(f"  - Client ID: {app.client_id[:20]}..." if app.client_id else "  - Client ID: НЕ УСТАНОВЛЕН")
                print(f"  - Client Secret: {'УСТАНОВЛЕН' if app.secret else 'НЕ УСТАНОВЛЕН'}")
                print(f"  - Сайты: {[s.domain for s in app.sites.all()]}")
                print()
        else:
            print("  НЕТ GOOGLE OAUTH ПРИЛОЖЕНИЙ")
            print("\nДля настройки запустите:")
            print("python setup_google_admin.py")
        
        # Проверяем переменные окружения
        print("Переменные окружения:")
        from django.conf import settings
        from decouple import config
        
        client_id = config('GOOGLE_OAUTH_CLIENT_ID', default='НЕ УСТАНОВЛЕН')
        client_secret = config('GOOGLE_OAUTH_CLIENT_SECRET', default='НЕ УСТАНОВЛЕН')
        
        print(f"  - GOOGLE_OAUTH_CLIENT_ID: {client_id[:20]}..." if client_id != 'НЕ УСТАНОВЛЕН' else f"  - GOOGLE_OAUTH_CLIENT_ID: {client_id}")
        print(f"  - GOOGLE_OAUTH_CLIENT_SECRET: {'УСТАНОВЛЕН' if client_secret != 'НЕ УСТАНОВЛЕН' else 'НЕ УСТАНОВЛЕН'}")
        
        # Рекомендации
        print("\nРЕКОМЕНДАЦИИ:")
        if not google_apps.exists():
            print("1. Запустите: python setup_google_admin.py")
            print("2. Введите ваши Google OAuth ключи")
        else:
            print("1. Проверьте Google Console redirect URIs:")
            print("   http://localhost:8000/accounts/google/login/callback/")
            print("2. Убедитесь, что Client ID и Secret правильные")
        
        print("3. Перезапустите сервер после изменений")
        
    except Exception as e:
        print(f"[ERROR] Ошибка проверки: {e}")

if __name__ == '__main__':
    check_oauth_status()
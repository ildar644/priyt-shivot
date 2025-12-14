#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Настройка Google OAuth через админку Django
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

def setup_google_oauth_admin():
    """Настройка Google OAuth через админку"""
    
    print("НАСТРОЙКА GOOGLE OAUTH ЧЕРЕЗ АДМИНКУ")
    print("=" * 40)
    
    try:
        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site
        
        # Получаем ключи от пользователя
        client_id = input("Введите Google Client ID: ").strip()
        client_secret = input("Введите Google Client Secret: ").strip()
        
        if not client_id or not client_secret:
            print("[ERROR] Client ID и Client Secret обязательны!")
            return False
        
        # Создаем или обновляем Site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'Pets Shelter Local'
            }
        )
        if not created:
            site.domain = 'localhost:8000'
            site.name = 'Pets Shelter Local'
            site.save()
        
        print(f"[OK] Site настроен: {site.domain}")
        
        # Удаляем старые Google приложения
        SocialApp.objects.filter(provider='google').delete()
        
        # Создаем новое Google приложение
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=client_secret,
        )
        
        # Привязываем к сайту
        google_app.sites.add(site)
        
        print("[OK] Google OAuth приложение создано")
        print(f"[OK] Client ID: {client_id[:20]}...")
        print(f"[OK] Привязано к сайту: {site.domain}")
        
        # Проверяем настройки
        print("\nПроверка настроек:")
        apps = SocialApp.objects.filter(provider='google')
        for app in apps:
            print(f"  - Приложение: {app.name}")
            print(f"  - Provider: {app.provider}")
            print(f"  - Client ID: {app.client_id[:20]}...")
            print(f"  - Сайты: {[s.domain for s in app.sites.all()]}")
        
        print("\n[OK] НАСТРОЙКА ЗАВЕРШЕНА!")
        print("Теперь можно тестировать Google OAuth:")
        print("1. Запустите сервер: python manage.py runserver")
        print("2. Откройте: http://localhost:8000/accounts/login/")
        print("3. Нажмите 'Войти через Google'")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка настройки: {e}")
        return False

if __name__ == '__main__':
    setup_google_oauth_admin()
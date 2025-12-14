@echo off
chcp 65001 >nul
title Приют для животных - Быстрый запуск
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🐾 ПРИЮТ ДЛЯ ЖИВОТНЫХ 🐾                  ║
echo ║                      Быстрый запуск                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден!
    echo.
    echo 📥 Скачайте Python с https://www.python.org/downloads/
    echo ⚠️  ОБЯЗАТЕЛЬНО поставьте галочку "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python найден
python --version

echo.
echo 📦 [1/6] Обновление pip...
python -m pip install --upgrade pip --quiet

echo 📦 [2/6] Установка зависимостей...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Ошибка установки зависимостей
    echo Попробуйте: pip install -r requirements.txt --user
    pause
    exit /b 1
)

echo ⚙️  [3/6] Создание настроек...
if not exist .env (
    copy .env.example .env >nul
    echo ✅ Файл .env создан
) else (
    echo ✅ Файл .env уже существует
)

echo 🗄️  [4/6] Настройка базы данных...
python manage.py migrate --verbosity=0
if %errorlevel% neq 0 (
    echo ❌ Ошибка настройки базы данных
    pause
    exit /b 1
)

echo 🎨 [5/6] Сбор статических файлов...
python manage.py collectstatic --noinput --verbosity=0

echo 👤 [6/6] Создание администратора...
echo.
echo Сейчас нужно создать администратора сайта.
echo Введите данные (пароль при вводе не отображается - это нормально):
echo.
python manage.py createsuperuser
if %errorlevel% neq 0 (
    echo ❌ Ошибка создания администратора
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ УСТАНОВКА ЗАВЕРШЕНА!                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Сайт будет доступен по адресу:
echo    http://127.0.0.1:8000
echo.
echo 🔧 Админ-панель:
echo    http://127.0.0.1:8000/admin/
echo.
echo 📝 Для входа используйте созданные данные администратора
echo.
echo ⏸️  Для остановки сервера нажмите Ctrl+C
echo.
echo Нажмите любую клавишу для запуска сервера...
pause >nul

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 ЗАПУСК СЕРВЕРА...                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Откройте браузер и перейдите на: http://127.0.0.1:8000
echo.

python manage.py runserver

echo.
echo Сервер остановлен.
pause
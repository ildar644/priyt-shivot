#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функция для красивого вывода
print_header() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🐾 ПРИЮТ ДЛЯ ЖИВОТНЫХ 🐾                  ║"
    echo "║                      Быстрый запуск                          ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Проверка Python
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        print_error "Python не найден!"
        echo
        echo "Установите Python:"
        echo "• macOS: brew install python"
        echo "• Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "• Fedora: sudo dnf install python3 python3-pip"
        echo "• Arch: sudo pacman -S python python-pip"
        exit 1
    fi
    
    print_success "Python найден: $($PYTHON_CMD --version)"
}

# Основная функция установки
main() {
    clear
    print_header
    
    # Проверка Python
    check_python
    
    echo
    print_step "📦 [1/6] Обновление pip..."
    $PYTHON_CMD -m pip install --upgrade pip --quiet
    
    print_step "📦 [2/6] Установка зависимостей..."
    $PIP_CMD install -r requirements.txt --quiet
    if [ $? -ne 0 ]; then
        print_error "Ошибка установки зависимостей"
        echo "Попробуйте: $PIP_CMD install --user -r requirements.txt"
        exit 1
    fi
    
    print_step "⚙️  [3/6] Создание настроек..."
    if [ ! -f .env ]; then
        cp .env.example .env
        print_success "Файл .env создан"
    else
        print_success "Файл .env уже существует"
    fi
    
    print_step "🗄️  [4/6] Настройка базы данных..."
    $PYTHON_CMD manage.py migrate --verbosity=0
    if [ $? -ne 0 ]; then
        print_error "Ошибка настройки базы данных"
        exit 1
    fi
    
    print_step "🎨 [5/6] Сбор статических файлов..."
    $PYTHON_CMD manage.py collectstatic --noinput --verbosity=0
    
    print_step "👤 [6/6] Создание администратора..."
    echo
    echo "Сейчас нужно создать администратора сайта."
    echo "Введите данные (пароль при вводе не отображается - это нормально):"
    echo
    $PYTHON_CMD manage.py createsuperuser
    if [ $? -ne 0 ]; then
        print_error "Ошибка создания администратора"
        exit 1
    fi
    
    echo
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    ✅ УСТАНОВКА ЗАВЕРШЕНА!                   ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
    echo -e "${GREEN}🌐 Сайт будет доступен по адресу:${NC}"
    echo "   http://127.0.0.1:8000"
    echo
    echo -e "${GREEN}🔧 Админ-панель:${NC}"
    echo "   http://127.0.0.1:8000/admin/"
    echo
    echo -e "${YELLOW}📝 Для входа используйте созданные данные администратора${NC}"
    echo
    echo -e "${YELLOW}⏸️  Для остановки сервера нажмите Ctrl+C${NC}"
    echo
    
    read -p "Нажмите Enter для запуска сервера..."
    
    clear
    echo
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🚀 ЗАПУСК СЕРВЕРА...                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
    echo -e "${GREEN}🌐 Откройте браузер и перейдите на: http://127.0.0.1:8000${NC}"
    echo
    
    $PYTHON_CMD manage.py runserver
    
    echo
    echo "Сервер остановлен."
}

# Запуск основной функции
main
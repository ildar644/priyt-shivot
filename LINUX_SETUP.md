# 🐧 Гайд для Linux: Запуск сайта приюта за 5 минут

## 🎯 Для кого этот гайд?
Для пользователей Linux (Ubuntu, Debian, Fedora, CentOS и др.), которые хотят быстро запустить готовый сайт.

---

## ⚡ Супер-быстрый запуск

### Ubuntu/Debian:
```bash
# Обновление системы и установка Python
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git

# Скачивание проекта
git clone https://github.com/ildar644/priyt-shivot.git
cd priyt-shivot/project

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка и запуск
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py runserver
```

### Fedora/CentOS/RHEL:
```bash
# Установка Python
sudo dnf install -y python3 python3-pip git  # Fedora
# sudo yum install -y python3 python3-pip git  # CentOS/RHEL

# Остальные команды такие же, как для Ubuntu
```

### Arch Linux:
```bash
# Установка Python
sudo pacman -S python python-pip git

# Остальные команды такие же
```

---

## 🔧 Подробная инструкция

### Шаг 1: Обновление системы

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt upgrade -y
```

**Fedora:**
```bash
sudo dnf update -y
```

**Arch Linux:**
```bash
sudo pacman -Syu
```

### Шаг 2: Установка Python и зависимостей

**Ubuntu/Debian:**
```bash
sudo apt install -y python3 python3-pip python3-venv python3-dev git curl wget
```

**Fedora:**
```bash
sudo dnf install -y python3 python3-pip python3-devel git curl wget
```

**CentOS/RHEL 8+:**
```bash
sudo yum install -y python3 python3-pip python3-devel git curl wget
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip git curl wget
```

### Шаг 3: Проверка установки
```bash
python3 --version
pip3 --version
git --version
```

### Шаг 4: Скачивание проекта

**Через Git (рекомендуется):**
```bash
cd ~
git clone https://github.com/ildar644/priyt-shivot.git
cd priyt-shivot/project
```

**Через wget:**
```bash
cd ~
wget https://github.com/ildar644/priyt-shivot/archive/refs/heads/main.zip
unzip main.zip
cd priyt-shivot-main/project
```

### Шаг 5: Создание виртуального окружения (рекомендуется)
```bash
python3 -m venv venv
source venv/bin/activate
```

Для деактивации окружения (когда закончите работу):
```bash
deactivate
```

### Шаг 6: Установка зависимостей
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Шаг 7: Настройка проекта
```bash
# Копирование настроек
cp .env.example .env

# Настройка базы данных
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput
```

### Шаг 8: Создание администратора
```bash
python manage.py createsuperuser
```

### Шаг 9: Запуск сервера
```bash
python manage.py runserver
```

### Шаг 10: Открытие сайта
Откройте браузер и перейдите на: http://127.0.0.1:8000

---

## 🚀 Автоматический скрипт установки

Создайте файл `install.sh`:

```bash
cat > install.sh << 'EOF'
#!/bin/bash

set -e  # Остановка при ошибке

echo "🐾 Установка сайта приюта для животных на Linux"
echo "=============================================="

# Определение дистрибутива
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
fi

echo "Обнаружена система: $OS"

# Установка зависимостей в зависимости от дистрибутива
if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
    echo "📦 Установка пакетов для Ubuntu/Debian..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv python3-dev git curl
elif [[ "$OS" == *"Fedora"* ]]; then
    echo "📦 Установка пакетов для Fedora..."
    sudo dnf install -y python3 python3-pip python3-devel git curl
elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
    echo "📦 Установка пакетов для CentOS/RHEL..."
    sudo yum install -y python3 python3-pip python3-devel git curl
elif [[ "$OS" == *"Arch"* ]]; then
    echo "📦 Установка пакетов для Arch Linux..."
    sudo pacman -S --noconfirm python python-pip git curl
else
    echo "⚠️ Неизвестный дистрибутив. Попробуйте установить python3, pip3 и git вручную."
fi

# Скачивание проекта
echo "📥 Скачивание проекта..."
if [ -d "priyt-shivot" ]; then
    echo "Папка проекта уже существует. Обновляем..."
    cd priyt-shivot
    git pull
else
    git clone https://github.com/ildar644/priyt-shivot.git
    cd priyt-shivot
fi

cd project

# Создание виртуального окружения
echo "🔧 Создание виртуального окружения..."
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
echo "📦 Установка зависимостей Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Настройка проекта
echo "⚙️ Настройка проекта..."
cp .env.example .env
python manage.py migrate
python manage.py collectstatic --noinput

echo "✅ Установка завершена!"
echo
echo "Для создания администратора выполните:"
echo "source venv/bin/activate && python manage.py createsuperuser"
echo
echo "Для запуска сервера выполните:"
echo "source venv/bin/activate && python manage.py runserver"
echo
echo "Сайт будет доступен по адресу: http://127.0.0.1:8000"
echo "Админ-панель: http://127.0.0.1:8000/admin/"
EOF

chmod +x install.sh
./install.sh
```

---

## 🎨 Создание системного сервиса (автозапуск)

### Создание пользователя для сервиса:
```bash
sudo useradd --system --shell /bin/bash --home /opt/shelter shelter
sudo mkdir -p /opt/shelter
sudo chown shelter:shelter /opt/shelter
```

### Перемещение проекта:
```bash
sudo cp -r ~/priyt-shivot /opt/shelter/
sudo chown -R shelter:shelter /opt/shelter/priyt-shivot
```

### Создание systemd сервиса:
```bash
sudo tee /etc/systemd/system/shelter.service > /dev/null << 'EOF'
[Unit]
Description=Shelter Website
After=network.target

[Service]
Type=simple
User=shelter
Group=shelter
WorkingDirectory=/opt/shelter/priyt-shivot/project
Environment=PATH=/opt/shelter/priyt-shivot/project/venv/bin
ExecStart=/opt/shelter/priyt-shivot/project/venv/bin/python manage.py runserver 0.0.0.0:8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
```

### Запуск сервиса:
```bash
sudo systemctl daemon-reload
sudo systemctl enable shelter
sudo systemctl start shelter
sudo systemctl status shelter
```

### Управление сервисом:
```bash
sudo systemctl start shelter    # Запуск
sudo systemctl stop shelter     # Остановка
sudo systemctl restart shelter  # Перезапуск
sudo systemctl status shelter   # Статус
```

---

## 🌐 Настройка Nginx (продакшн)

### Установка Nginx:
```bash
# Ubuntu/Debian
sudo apt install nginx

# Fedora
sudo dnf install nginx

# Arch
sudo pacman -S nginx
```

### Настройка Nginx:
```bash
sudo tee /etc/nginx/sites-available/shelter << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # Замените на ваш домен

    location /static/ {
        alias /opt/shelter/priyt-shivot/project/staticfiles/;
    }

    location /media/ {
        alias /opt/shelter/priyt-shivot/project/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/shelter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 Настройка SSL с Let's Encrypt

### Установка Certbot:
```bash
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx

# Fedora
sudo dnf install certbot python3-certbot-nginx
```

### Получение SSL сертификата:
```bash
sudo certbot --nginx -d your-domain.com
```

### Автообновление сертификата:
```bash
sudo crontab -e
# Добавьте строку:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🗄️ Настройка PostgreSQL (рекомендуется для продакшн)

### Установка PostgreSQL:
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib python3-psycopg2

# Fedora
sudo dnf install postgresql postgresql-server python3-psycopg2

# Arch
sudo pacman -S postgresql python-psycopg2
```

### Инициализация и запуск:
```bash
# Fedora/CentOS
sudo postgresql-setup --initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Ubuntu/Debian (запускается автоматически)
sudo systemctl enable postgresql
```

### Создание базы данных:
```bash
sudo -u postgres psql << 'EOF'
CREATE DATABASE shelter_db;
CREATE USER shelter_user WITH PASSWORD 'your_strong_password';
GRANT ALL PRIVILEGES ON DATABASE shelter_db TO shelter_user;
ALTER USER shelter_user CREATEDB;
\q
EOF
```

### Обновление настроек в .env:
```bash
# Отредактируйте файл .env
nano /opt/shelter/priyt-shivot/project/.env

# Измените строки:
DB_NAME=shelter_db
DB_USER=shelter_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=5432
```

### Миграция на PostgreSQL:
```bash
cd /opt/shelter/priyt-shivot/project
source venv/bin/activate
pip install psycopg2-binary
python manage.py migrate
sudo systemctl restart shelter
```

---

## 🚨 Частые проблемы и решения

### "python3: command not found"
```bash
# Ubuntu/Debian
sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

### "pip3: command not found"
```bash
# Ubuntu/Debian
sudo apt install python3-pip

# Fedora
sudo dnf install python3-pip
```

### "Permission denied" при установке пакетов
```bash
pip install --user -r requirements.txt
```

### Проблемы с виртуальным окружением
```bash
# Удалите старое окружение
rm -rf venv

# Создайте новое
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
# Найдите процесс
sudo netstat -tlnp | grep :8000
# или
sudo ss -tlnp | grep :8000

# Убейте процесс
sudo kill -9 PID_ПРОЦЕССА

# Или используйте другой порт
python manage.py runserver 8080
```

### Проблемы с правами доступа
```bash
# Исправление прав на файлы проекта
sudo chown -R $USER:$USER ~/priyt-shivot
chmod -R 755 ~/priyt-shivot
```

---

## 🔧 Полезные команды для диагностики

### Проверка системы:
```bash
# Информация о системе
uname -a
lsb_release -a  # Ubuntu/Debian
cat /etc/os-release

# Проверка ресурсов
free -h         # Память
df -h           # Диск
top             # Процессы
```

### Проверка сети:
```bash
# Проверка портов
sudo netstat -tlnp
sudo ss -tlnp

# Проверка подключения
curl http://127.0.0.1:8000
wget -qO- http://127.0.0.1:8000
```

### Просмотр логов:
```bash
# Логи Django
tail -f ~/priyt-shivot/project/django.log

# Логи системного сервиса
sudo journalctl -u shelter -f

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 📊 Мониторинг и обслуживание

### Создание скрипта резервного копирования:
```bash
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/shelter"
PROJECT_DIR="/opt/shelter/priyt-shivot/project"

mkdir -p $BACKUP_DIR

# Резервная копия базы данных
cd $PROJECT_DIR
source venv/bin/activate
python manage.py dumpdata > $BACKUP_DIR/db_backup_$DATE.json

# Резервная копия медиа файлов
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz media/

# Удаление старых копий (старше 30 дней)
find $BACKUP_DIR -name "*.json" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Резервная копия создана: $DATE"
EOF

chmod +x backup.sh

# Добавление в cron (ежедневно в 2:00)
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/backup.sh") | crontab -
```

### Мониторинг производительности:
```bash
# Установка htop
sudo apt install htop  # Ubuntu/Debian
sudo dnf install htop  # Fedora

# Мониторинг в реальном времени
htop

# Проверка использования диска
du -sh ~/priyt-shivot
```

---

## ✅ Финальный чек-лист

### Базовая установка:
- [ ] Python3 установлен (`python3 --version`)
- [ ] pip3 установлен (`pip3 --version`)
- [ ] Git установлен (`git --version`)
- [ ] Проект скачан
- [ ] Виртуальное окружение создано
- [ ] Зависимости установлены
- [ ] База данных настроена
- [ ] Администратор создан
- [ ] Сервер запускается
- [ ] Сайт открывается (http://127.0.0.1:8000)

### Продакшн установка:
- [ ] Системный пользователь создан
- [ ] Systemd сервис настроен
- [ ] Nginx установлен и настроен
- [ ] SSL сертификат получен
- [ ] PostgreSQL настроен
- [ ] Резервное копирование настроено
- [ ] Мониторинг настроен

**Если все галочки стоят - отлично! Сайт готов к работе! 🎉🐾**

---

## 🆘 Получение помощи

1. **Проверьте логи**: `journalctl -u shelter -f`
2. **Перечитайте инструкции**
3. **Проверьте раздел "Частые проблемы"**
4. **Создайте Issue**: https://github.com/ildar644/priyt-shivot/issues

**Удачи в помощи животным! 🐾❤️**
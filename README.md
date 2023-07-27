# tgparsing-bots

## Клонирование и настройка проекта

### HTTPS
```bash
git clone https://github.com/CrowMEV/tgparsing-bots.git tgparsing-bots
```

### SSH
```bash
git clone git@github.com:CrowMEV/tgparsing-bots.git tgparsing-bots
```


## Локальный запуск сервера

### Переход в директорию, установка пакетов
```bash
cd tgparsing-bots
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip -r requirements.txt
poetry install

```
### Установка pre-commit hooks

Установка хуков
```bash
pre-commit install
```
### Запуск docker compose с базой для разработки
Переименовавать файл env.example в .env, пустые ключи заполнить согласно settings.py дефолтными значения
Запустить docker compose
```bash
docker compose up -d
```
### Запуск сервера

```bash
./manage.py site run
```


Документация:  
- [Swagger](http://localhost:8000/docs)  
- [Redoc](http://127.0.0.1:8000/redoc)  

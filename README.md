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

### Переход в директорию, установка пакетов и накат миграций
**Для запуска сервера переменные окружения не нужны. Данные для базы данных можно взять из файла settings. До запуска миграций база данных должна быть уже создана**
```bash
cd tgparsing-bots
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install

```
### Установка pre-commit hooks

Установка хуков
```bash
pip install pre-commit
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

# tgparsing-bots

## Локальный запуск сервера

### Переход в директорию, установка пакетов и накат миграций
**Для запуска сервера переменные окружения не нужны. Данные для базы данных можно взять из файла settings. До запуска миграций база данных должна быть уже создана**
```bash
cd backend
pip install -r requirements.txt
```

### Запуск сервера

```bash
./manage.py site run
```


Документация:  
- [Swagger](http://localhost:8000/docs)  
- [Redoc](http://127.0.0.1:8000/redoc)  

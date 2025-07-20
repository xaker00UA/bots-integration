## Описание проекта

Этот проект представляет собой интеграцию существующего сервера с использованием FastAPI для взаимодействия с ботами Discord и Telegram. Основной сервер доступен по ссылке: [wotblitz-site](https://github.com/xaker00UA/Backend-on-fastapi).

## Запуск и настройка

### Требования

- Python 3.10+
- poetry
- Доступ к основному серверу ([wotblitz-site](https://github.com/xaker00UA/Backend-on-fastapi))
- Токены для Discord и Telegram ботов

### Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/xaker00UA/bots-integration.git
    cd bots-integration
    ```

2. Установите зависимости:
    ```bash
    poetry install --only main
    ```

3. Создайте файл `.env` и добавьте необходимые переменные окружения:
    ```
    mode=PROD | DEV | TEST

    tokens__telegram_token=TOKEN_TELEGRAM
    tokens__discord_token=TOKEN_DISCORD

    database__sqlite_path=bots.db 
    ****
    # Main Server
    server__protocol=http
    server__host=localhost
    server__port=8000
    server__prefix=api
    # Optional parameter
    server__version=v1
    # Нужно выпустить токены с безграничным сроком действия указывая name=Discord|Telegram
    # Используя тот же секретный ключ что у на основном сервере
    server__discord_token=
    server__telegram_token=

    # Ссылка на основной вебсайт
    frontend__frontend_url=

    # AUTH
    bots__discord__client_id=
    bots__discord__client_secret=
    bots__discord__redirect_url=http://localhost:8000/api/v1/bot/discord

    bots__telegram__client_id=
    bots__telegram__client_secret=
    bots__telegram__redirect_url=http://localhost:8000/api/v1/bot/telegram

    ```

### Запуск

```bash
python main.py
```

Боты автоматически подключатся к основному серверу и начнут обрабатывать команды.

### Дополнительная информация

- Для корректной работы убедитесь, что основной сервер запущен и доступен по адресу, указанному в блоке `Main Server`.
- Подробную документацию по API основного сервера смотрите в [репозитории wotblitz-site](https://github.com/xaker00UA/Backend-on-fastapi).


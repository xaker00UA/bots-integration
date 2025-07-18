from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from src.service.auth import DiscordAuth

app = FastAPI(root_path="/api/v1")


@app.get("/bot/telegram")
async def auth_telegram_bot(code: str):
    return HTMLResponse(
        content="""
        <html>
            <head>
                <title>Авторизация успешна</title>
            </head>
            <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                <h1>✅ Успешно!</h1>
                <p>Вы авторизовались через Telegram. Можете закрыть окно.</p>
            </body>
        </html>
    """,
        status_code=200,
    )


@app.get("/bot/discord")
async def auth_discord_bot(code: str):
    token = await DiscordAuth().get_token(code)
    return HTMLResponse(
        content="""
        <html>
            <head>
                <title>Авторизация успешна</title>
            </head>
            <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                <h1>✅ Успешно!</h1>
                <p>Вы авторизовались через Discord. Можете закрыть окно.</p>
            </body>
        </html>
    """,
        status_code=200,
    )

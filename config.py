import os
from dotenv import load_dotenv

load_dotenv()


# Учётные данные GigaChat берутся из переменной окружения
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
# Токен Telegram-бота
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# Параметры модели GigaChat
MODEL_NAME = "GigaChat-2-Pro"
VERIFY_SSL = False
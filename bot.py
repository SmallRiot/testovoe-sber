import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from config import TELEGRAM_TOKEN
from tools import list_deposit_names, recommend_deposits, ask_rag_about_deposits, calculate_final_amount
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from rag import model

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Системный prompt для агента
SYSTEM_PROMPT = (
    "Ты — вежливый ИИ-агент, который помогает подобрать банковский вклад. "
    "Если пользователю не хватает параметров (валюта, срок, пополнение/снятие), уточняй эти данные. "
    "Используй инструменты только при необходимости."
)

# Инициализация ReAct-агента
agent = create_react_agent(
    model=model,
    tools=[list_deposit_names, recommend_deposits, ask_rag_about_deposits, calculate_final_amount],
    checkpointer=MemorySaver(),
    state_modifier=SYSTEM_PROMPT,
)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-консультант по банковским вкладам. Задайте мне вопрос — например, 'посоветуй вклад на 6 месяцев без пополнения'."
    )

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    # Вызов агента с передачей истории диалога и идентификатором потока для чекпоинтера
    response = agent.invoke(
        {"messages": [("user", user_text)]},
        config={"configurable": {"thread_id": str(chat_id)}}
    )
    # Последний ответ агента
    reply = response["messages"][-1].content
    await update.message.reply_text(reply)

# Основная функция запуска

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Запущен Telegram-бот")
    app.run_polling()


if __name__ == "__main__":
    main()
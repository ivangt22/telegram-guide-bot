import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = '@surkovofficial'

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! ✌️\n"
        f"Напиши /guide, чтобы получить гайд.\n"
        f"Но сначала подпишись на наш канал: {CHANNEL_USERNAME}"
    )

async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except Exception as e:
        logging.warning(f"Ошибка при проверке подписки: {e}")
        return False

async def guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_subscription(user_id, context):
        await update.message.reply_text("✅ Ты подписан! Вот твой гайд:\n\nТут ваш гайд.")
    else:
        await update.message.reply_text(
            f"❗️Похоже, ты не подписан на канал {CHANNEL_USERNAME}\n"
            f"Подпишись и напиши /guide снова!"
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("guide", guide))
    print("✅ Бот запущен!")
    app.run_polling()

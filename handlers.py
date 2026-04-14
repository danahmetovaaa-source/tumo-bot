import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from ai_handler import get_ai_response

logger = logging.getLogger(__name__)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋 Я AI-помощник TUMO Astana.\n"
        "Спрашивай про запись, расписание, документы — всё что угодно!\n\n"
        "/help — команды\n"
        "/reset — начать разговор заново"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — приветствие\n"
        "/reset — очистить историю разговора\n\n"
        "Или просто пиши свой вопрос!"
    )


async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from ai_handler import conversation_history
    user_id = update.effective_user.id
    conversation_history.pop(user_id, None)
    await update.message.reply_text("✅ История очищена, начнём заново!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id   = update.effective_user.id
    user_text = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    try:
        answer = get_ai_response(user_id, user_text)
        await update.message.reply_text(answer)
    except Exception as e:
        logger.error("AI error: %s", e)
        await update.message.reply_text(
            "Что-то пошло не так 😔 Напиши нам: info.astana@tumo.kz"
        )
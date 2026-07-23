import os
import re
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from app.core.config import get_settings
from app.agents.agent_manager import AgentManager

logger = logging.getLogger(__name__)

# Initialize Agent Manager
agent_manager = AgentManager()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for the /start command.
    """
    if not update.message:
        return
    chat_id = str(update.effective_chat.id)
    print(f"📩 [Telegram] Received /start from chat_id={chat_id}")
    welcome_text = (
        "🤖 **Welcome to the Supermarket Operations Agent Bot!**\n\n"
        "I am your AI operational assistant. You can manage your store by sending me natural language messages. "
        "Here are some examples of what you can ask me:\n\n"
        "🛒 **Products & Catalog**\n"
        "• _'List all products'_\n"
        "• _'Find products under 50 rupees'_\n"
        "• _'Is milk in stock?'_\n\n"
        "📦 **Inventory Management**\n"
        "• _'Show inventory'_\n"
        "• _'Which products are low on stock?'_\n"
        "• _'Show stock history for rice'_\n\n"
        "💳 **Billing & Credit (Khata)**\n"
        "• _'Create bill for 2 rice and 1 milk'_\n"
        "• _'Show outstanding balance for Rahul'_\n"
        "• _'Record credit of 500 for John'_\n\n"
        "📊 **Analytics & Reports**\n"
        "• _'Today's sales summary'_\n"
        "• _'What are the top selling products?'_\n"
        "• _'Generate sales report PPT'_\n\n"
        "Start chatting with me now! I keep track of your chat context so you can perform multi-step sales."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Message handler for incoming text queries.
    """
    if not update.message or not update.message.text:
        return
        
    user_text = update.message.text
    chat_id = str(update.effective_chat.id)
    print(f"📩 [Telegram] Received message from chat_id={chat_id}: '{user_text}'")

    # Indicate the bot is processing/typing
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        # Call Agent Manager with dynamic session isolation
        agent_response = await agent_manager.chat(user_text, session_id=chat_id)
        
        # Clean up absolute file paths from the visible text response to keep UI premium
        clean_response = agent_response
        
        # Extract files that might have been generated
        # Regex matches absolute paths like C:\... or relative like data/reports/...
        found_paths = re.findall(
            r'(?:[a-zA-Z]:\\[^\s\n\'"\(\)]+\.(?:pdf|html|pptx)|[^\s\n\'"\(\)]+\.(?:pdf|html|pptx))',
            agent_response
        )
        
        # Unique list of files that exist
        files_to_send = []
        for path in found_paths:
            # Strip quotes and brackets
            clean_path = path.strip('\'"()')
            abs_path = os.path.abspath(clean_path)
            
            if os.path.exists(abs_path) and os.path.isfile(abs_path):
                if abs_path not in files_to_send:
                    files_to_send.append(abs_path)
                    # Replace absolute path in user-facing message with a friendly name
                    base_name = os.path.basename(abs_path)
                    clean_response = clean_response.replace(path, f"[{base_name}]")

        # Reply with the text response
        await update.message.reply_text(clean_response)
        print(f"📤 [Telegram] Sent response to chat_id={chat_id}")

        # Upload and send the documents
        for file_path in files_to_send:
            await context.bot.send_chat_action(chat_id=chat_id, action="upload_document")
            
            file_name = os.path.basename(file_path)
            # Create a user friendly caption
            if file_path.endswith(".pdf"):
                caption = "📄 Here is your generated PDF Invoice."
            elif file_path.endswith(".html"):
                caption = "🌐 Invoice HTML document (PDF fallback due to environment)."
            elif file_path.endswith(".pptx"):
                caption = "📊 Here is your compiled PowerPoint Presentation Report."
            else:
                caption = f"📁 Document: {file_name}"
                
            with open(file_path, "rb") as doc:
                await update.message.reply_document(
                    document=doc,
                    filename=file_name,
                    caption=caption
                )
                print(f"📎 [Telegram] Sent file '{file_name}' to chat_id={chat_id}")
                
    except Exception as e:
        logger.exception("Error handling user message in Telegram Bot")
        print(f"❌ [Telegram Error] {e}")
        await update.message.reply_text(
            f"⚠️ An error occurred while processing your request: {str(e)}\n"
            "Please check settings or try again."
        )


from telegram.request import HTTPXRequest


def main():
    """
    Main entrypoint for running the bot inside app.bot.
    """
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    
    settings = get_settings()
    
    if not settings.telegram_bot_token or settings.telegram_bot_token == "your_token":
        print("Error: TELEGRAM_BOT_TOKEN is not configured in .env file.")
        return
        
    print("Starting Supermarket Ops Telegram Bot...")

    # Configure custom HTTPX request with longer timeouts to prevent network connection timeouts
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0,
    )

    application = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .request(request)
        .build()
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Run bot polling with bootstrap retries
    application.run_polling(bootstrap_retries=5)

if __name__ == "__main__":
    main()

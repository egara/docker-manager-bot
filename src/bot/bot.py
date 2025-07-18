import logging
from telegram.ext import CommandHandler, Application, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.docker_manager.docker_manager import DockerManager

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    """
    Manages the Telegram bot, including its initialization,
    command handling, and execution.
    """
    def __init__(self, token):
        """
        Initializes the Telegram bot.

        Args:
            token (str): The authentication token for the Telegram bot.
        """
        self.application = Application.builder().token(token).build()
        self.docker_manager = DockerManager()

        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("list", self.list_containers))
        self.application.add_handler(CommandHandler("stop", self.stop_container_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler for the /start command.
        Sends a welcome message and a button to show the commands.
        """
        user = update.effective_user
        logger.info("User %s (%s) has executed the /start command", user.first_name, user.id)

        keyboard = [[InlineKeyboardButton("Show Commands", callback_data='show_commands')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Hello {user.first_name}! I am your bot for managing Docker. Press the button to see the available commands.",
            reply_markup=reply_markup
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler for inline button presses.
        """
        query = update.callback_query
        await query.answer() # Answer the callback query so the button doesn't seem "stuck"

        if query.data == 'show_commands':
            logger.info("User %s (%s) has requested to see the commands", query.from_user.first_name, query.from_user.id)
            commands_message = "Available commands:\n/list - Lists running Docker containers.\n/stop - Stops a running Docker container."
            keyboard = [[InlineKeyboardButton("Show Commands", callback_data='show_commands')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=query.message.chat_id, text=commands_message, reply_markup=reply_markup)
        elif query.data.startswith('stop_'):
            container_id = query.data.replace('stop_', '')
            logger.info("User %s (%s) has requested to stop the container with ID: %s", query.from_user.first_name, query.from_user.id, container_id)
            try:
                self.docker_manager.stop_container(container_id)
                message = f"Container {container_id} stopped successfully."
            except Exception as e:
                message = f"Error stopping container {container_id}: {e}"
            
            keyboard = [[InlineKeyboardButton("Show Commands", callback_data='show_commands')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=message, reply_markup=reply_markup)

    async def list_containers(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler for the /list command.

        Gets the list of running containers and sends it as
        a message to the user.
        """
        user = update.effective_user
        logger.info("User %s (%s) has executed the /list command", user.first_name, user.id)

        containers = self.docker_manager.list_containers()
        if containers:
            message = "Running containers:\n"
            for container in containers:
                message += f"- {container.name} ({container.short_id})\n"
        else:
            message = "No running containers."

        keyboard = [[InlineKeyboardButton("Show Commands", callback_data='show_commands')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup)

    async def stop_container_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler for the /stop command.
        Displays a list of running containers for the user to select which one to stop.
        """
        user = update.effective_user
        logger.info("User %s (%s) has executed the /stop command", user.first_name, user.id)

        containers = self.docker_manager.list_containers()
        if containers:
            message = "Select the container to stop:\n"
            keyboard = []
            for container in containers:
                keyboard.append([InlineKeyboardButton(f"{container.name} ({container.short_id})", callback_data=f'stop_{container.short_id}')])
            
            # Add the "Show Commands" button at the end
            keyboard.append([InlineKeyboardButton("Show Commands", callback_data='show_commands')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(message, reply_markup=reply_markup)
        else:
            message = "No running containers to stop."
            keyboard = [[InlineKeyboardButton("Show Commands", callback_data='show_commands')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(message, reply_markup=reply_markup)

    def run(self, use_webhook=False, public_url=None, port=8443):
        """
        Starts the bot, either using Polling or Webhooks.

        Args:
            use_webhook (bool): If True, uses Webhooks. Otherwise, uses Polling.
            public_url (str): The base public URL (e.g., https://your-domain.com).
            port (int): The port the bot will listen on.
        """
        self.application.initialize()

        if use_webhook:
            if not public_url:
                raise ValueError("The public URL is required to use webhooks.")
            
            print(f"Starting bot with Webhook on port {port}")
            self.application.run_webhook(listen="0.0.0.0",
                                         port=port,
                                         url_path="/", # Use root path for webhook
                                         webhook_url=f"{public_url}/")
        else:
            print("Starting bot with Polling")
            self.application.run_polling()
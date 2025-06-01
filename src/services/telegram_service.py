"""
Service principal pour gérer les interactions avec le bot Telegram.
Ce module orchestre la gestion des commandes, des messages et l'intégration avec Mistral AI.
"""
import logging
from typing import Dict, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from ..db.db_adapter import DatabaseAdapter
from .mistral_client import MistralClient
from ..config.env import config

# Initialisation du logger pour ce service
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TelegramService:
    """
    Service pour gérer toutes les interactions du bot Telegram avec les utilisateurs.
    """

    def __init__(self, db_adapter: DatabaseAdapter):
        """
        Initialise le service Telegram avec l'adaptateur de base de données et le client Mistral.

        Args:
            db_adapter: Instance de l'adaptateur de base de données à utiliser.
        """
        self.token = config.TELEGRAM_BOT_TOKEN
        if not self.token:
            raise ValueError("La variable d'environnement TELEGRAM_BOT_TOKEN est requise.")
        self.db_adapter = db_adapter
        self.mistral_client = MistralClient()
        self.chat_mode = {}  # Suivi du mode chat par chat_id

        # Création de l'application Telegram
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """
        Configure les gestionnaires de commandes, messages et callbacks pour le bot.
        """
        self.app.add_handler(CommandHandler("start", self._start_command))
        self.app.add_handler(CommandHandler("chat", self._chat_command))
        self.app.add_handler(CommandHandler("reset", self._reset_command))
        self.app.add_handler(CommandHandler("help", self._help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        self.app.add_handler(CallbackQueryHandler(self._handle_callback))
        self.app.add_error_handler(self._error_handler)

    async def start_polling(self):
        """
        Démarre le bot Telegram en mode polling.
        
        """
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        logger.info("Bot Telegram lancé en mode polling.")

    async def stop(self):
        """
        Arrête proprement le bot Telegram.

        """
        if self.app.updater:
            await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
        logger.info("Bot Telegram arrêté.")

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Gère la commande /start pour accueillir l'utilisateur.

        Args:
            update: Objet Update de Telegram.
            context: Contexte de la conversation.

        """
        welcome_message = (
            "Bonjour ! Je suis votre assistant IA alimenté par Mistral AI. "
            "Utilisez /chat pour démarrer une conversation, /reset pour effacer l'historique, "
            "ou /help pour voir toutes les commandes disponibles."
        )
        await update.message.reply_text(welcome_message)

    async def _chat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Active le mode chat pour le chat courant.

        Args:
            update: Objet Update de Telegram.
            context: Contexte de la conversation.

        """
        chat_id = update.effective_chat.id
        self.chat_mode[chat_id] = True
        await update.message.reply_text("Mode chat activé ! Vous pouvez maintenant discuter avec moi.")

    async def _reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Réinitialise l'historique de conversation pour le chat courant.

        Args:
            update: Objet Update de Telegram.
            context: Contexte de la conversation.

        """
        chat_id = update.effective_chat.id
        await self.db_adapter.reset_conversation(chat_id)
        await update.message.reply_text("Votre historique de conversation a été réinitialisé.")

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Affiche la liste des commandes disponibles.

        Args:
            update: Objet Update de Telegram.
            context: Contexte de la conversation.

        """
        help_message = (
            "Commandes disponibles :\n"
            "/start - Démarrer la conversation\n"
            "/chat - Activer le mode chat\n"
            "/reset - Réinitialiser l'historique\n"
            "/help - Afficher ce message d'aide"
        )
        await update.message.reply_text(help_message)

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Gère les messages texte envoyés par l'utilisateur.

        Args:
            update: Objet Update de Telegram.
            context: Contexte de la conversation.

        """
        chat_id = update.effective_chat.id
        username = update.effective_user.username or "user"
        message = update.message.text

        # Activation automatique du mode chat si nécessaire
        if not self.chat_mode.get(chat_id):
            self.chat_mode[chat_id] = True
            logger.info(f"Mode chat activé automatiquement pour le chat {chat_id}")

        # Indiquer que le bot est en train d'écrire
        await update.effective_chat.send_action(action="typing")

        # Traitement du message utilisateur
        response = await self.process_message(chat_id, username, message)

        # Ajout de boutons de feedback
        keyboard = [
            [
                InlineKeyboardButton("👍", callback_data="feedback_positive"),
                InlineKeyboardButton("👎", callback_data="feedback_negative")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(response, reply_markup=reply_markup)

    async def _handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Gère les retours des boutons de feedback.

        Args:
            update: Objet Update de Telegram.
            context: Contexte de la conversation.

        """
        query = update.callback_query
        await query.answer()

        if query.data == "feedback_positive":
            await query.edit_message_reply_markup(reply_markup=None)
            await query.message.reply_text("Merci pour votre retour positif ! 😊")
        elif query.data == "feedback_negative":
            await query.edit_message_reply_markup(reply_markup=None)
            await query.message.reply_text("Je suis désolé que ma réponse n'ait pas été utile. N'hésitez pas à préciser votre besoin.")

    async def _error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Capture et log les erreurs survenues lors du traitement des mises à jour Telegram.

        Args:
            update: Objet Update de Telegram.
            context: Contexte de la conversation.

        """
        logger.error(f"Erreur lors du traitement de la mise à jour {update}: {context.error}")

    async def process_message(self, chat_id: int, username: str, message: str) -> str:
        """
        Traite un message utilisateur, interroge Mistral AI et retourne la réponse.

        Args:
            chat_id: ID du chat Telegram.
            username: Nom d'utilisateur Telegram.
            message: Message envoyé par l'utilisateur.

        Returns:
            str: Réponse générée par Mistral AI.

        """
        # Enregistrer le message utilisateur
        await self.db_adapter.save_message(chat_id, username, message)

        # Récupérer l'historique de la conversation
        conversation_history = await self.db_adapter.get_conversation(chat_id)

        # Obtenir la réponse de Mistral AI
        response = await self.mistral_client.get_completion(message, conversation_history)

        # Enregistrer la réponse du bot
        await self.db_adapter.save_response(chat_id, response)

        return response
"""
Point d'entrée principal de l'application chatbot Telegram.
Ce module configure l'application FastAPI, l'intégration avec Telegram, la base de données et la documentation Swagger.
Il gère également les événements de démarrage et d'arrêt de l'application.

"""
import asyncio
import logging
from fastapi import FastAPI
from typing import Optional

from .config.env import config, validate_env
from .config.swagger import setup_swagger
from .db.db_adapter import DatabaseAdapter
from .db.adapters.memory_adapter import MemoryAdapter
from .db.adapters.dynamo_adapter import DynamoAdapter
from .services.telegram_service import TelegramService
from .controllers.chat_controllers import ChatController
from .routes.chat_route import create_chat_router

# Initialisation du logger principal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_database_adapter() -> DatabaseAdapter:
    """
    Sélectionne et retourne l'adaptateur de base de données approprié selon la configuration.

    Returns:
        DatabaseAdapter: Instance de l'adaptateur choisi.
    """
    if config.USE_MEMORY_ADAPTER:
        logger.info("Base de données en mémoire sélectionnée.")
        return MemoryAdapter()
    if config.IS_LAMBDA_ENVIRONMENT:
        logger.info("Base de données DynamoDB sélectionnée (environnement Lambda).")
        return DynamoAdapter()
    logger.info("Base de données en mémoire utilisée par défaut.")
    return MemoryAdapter()

def create_app(db_adapter: Optional[DatabaseAdapter] = None) -> 'FastAPI': # type: ignore

    """
    Instancie et configure l'application FastAPI pour le chatbot.

    Args:
        db_adapter: Adaptateur de base de données à utiliser (optionnel).

    Returns:
        FastAPI: Application FastAPI prête à l'emploi.
    """
    app = FastAPI(title="ESGIS Telegram Chatbot API")

    # Configuration de la documentation Swagger
    setup_swagger(app)

    # Sélection de l'adaptateur de base de données
    if db_adapter is None:
        db_adapter = get_database_adapter()

    # Instanciation des services et contrôleurs
    telegram_service = TelegramService(db_adapter)
    chat_controller = ChatController(telegram_service)

    # Ajout des routes de chat
    app.include_router(create_chat_router(chat_controller), prefix="/chat")

    # Événement de démarrage : vérification de l'environnement et lancement du bot
    @app.on_event("startup")
    async def startup_event():
        missing_vars = validate_env()
        if missing_vars:
            logger.error(f"Variables d'environnement manquantes : {', '.join(missing_vars)}")
            logger.error("Merci de compléter le fichier .env avec les variables requises.")
            return
        if not config.IS_LAMBDA_ENVIRONMENT:
            asyncio.create_task(telegram_service.start_polling())
            logger.info(f"Serveur lancé sur le port {config.PORT}")
            logger.info(f"Documentation API : http://localhost:{config.PORT}")
            logger.info("Bot Telegram opérationnel et en écoute.")

    # Événement d'arrêt : arrêt propre du bot Telegram
    @app.on_event("shutdown")
    async def shutdown_event():
        if not config.IS_LAMBDA_ENVIRONMENT:
            await telegram_service.stop()

    return app
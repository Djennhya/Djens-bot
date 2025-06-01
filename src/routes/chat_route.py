"""
Définition des routes pour l'API de chat du chatbot Telegram.
Ce module expose les endpoints pour envoyer un message et vérifier la santé du service.

"""
from fastapi import APIRouter
from typing import Dict

from ..controllers.chat_controllers import ChatController, MessageRequest, MessageResponse

def create_chat_router(chat_controller: ChatController) -> APIRouter:
    """
    Crée un routeur FastAPI pour les endpoints de chat.

    Args:
        chat_controller: Instance du contrôleur de chat à utiliser.

    Returns:
        APIRouter: Routeur FastAPI configuré avec les routes de chat.

    """
    router = APIRouter(tags=["chat"])

    @router.post("/send", response_model=MessageResponse)
    async def send_message(request: MessageRequest) -> MessageResponse:
        """
        Endpoint pour envoyer un message au bot et obtenir la réponse.

        Args:
            request (MessageRequest): Requête contenant les informations du message utilisateur.

        Returns:
            MessageResponse: Réponse générée par le bot.

        """
        return await chat_controller.send_message(request)

    @router.get("/health", response_model=Dict[str, str])
    async def health_check() -> Dict[str, str]:
        """
        Endpoint pour vérifier l'état de santé du service de chat.

        Returns:
            dict: Dictionnaire indiquant l'état du service.

        """
        return await chat_controller.get_health()

    return router
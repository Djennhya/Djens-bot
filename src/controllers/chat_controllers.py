"""
Contrôleur principal pour la gestion des requêtes de chat via l'API FastAPI.
Ce fichier définit les modèles de requête/réponse et le contrôleur de chat.

"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List

from ..services.telegram_service import TelegramService

class MessageRequest(BaseModel):
    """
    Modèle de données pour la requête d'envoi de message au chatbot.

    """
    chat_id: int
    username: str
    message: str

class MessageResponse(BaseModel):
    """
    Modèle de données pour la réponse du chatbot.

    """
    response: str

class ChatController:
    """
    Contrôleur regroupant les méthodes pour gérer les requêtes de chat via l'API.

    """

    def __init__(self, telegram_service: TelegramService):
        """
        Initialise le contrôleur de chat avec le service Telegram.

        Args:
            telegram_service: Instance du service Telegram à utiliser.

        """
        self.telegram_service = telegram_service

    async def send_message(self, request: MessageRequest) -> MessageResponse:
        """
        Traite l'envoi d'un message utilisateur au bot et retourne la réponse générée.

        Args:
            request: Objet contenant les informations du message utilisateur.

        Returns:
            MessageResponse: Réponse générée par le bot.

        """
        try:
            response = await self.telegram_service.process_message(
                request.chat_id,
                request.username,
                request.message
            )
            return MessageResponse(response=response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors du traitement du message: {str(e)}")

    async def get_health(self) -> Dict[str, str]:
        """
        Vérifie l'état de santé du service de chat.

        Returns:
            dict: Dictionnaire indiquant l'état du service.
            
        """
        return {"status": "ok", "message": "Le service de chat est opérationnel"}
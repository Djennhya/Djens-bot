"""
Client HTTP pour communiquer avec l'API Mistral AI.
Ce module permet d'envoyer des requêtes à Mistral et de récupérer les réponses générées.

"""
import requests
from typing import List, Dict, Any
import logging
from ..config.env import config

# Configuration du logger pour ce module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MistralClient:
    """
    Classe client pour interagir avec l'API Mistral AI.

    """

    def __init__(self):
        """
        Initialise le client Mistral avec les paramètres de configuration.

        """
        self.api_key = config.MISTRAL_API_KEY
        self.base_url = config.MISTRAL_BASE_URL
        self.model = config.MISTRAL_MODEL

        if not self.api_key:
            logger.warning("La clé API MISTRAL_API_KEY n'est pas définie.")

    async def get_completion(self, prompt: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Envoie une requête à l'API Mistral pour obtenir une complétion basée sur le prompt et l'historique.

        Args:
            prompt: Texte de l'utilisateur à envoyer à l'IA.
            conversation_history: Historique des échanges pour le contexte.

        Returns:
            str: Réponse générée par Mistral AI.

        """
        if conversation_history is None:
            conversation_history = []

        try:
            # Préparer les messages au format attendu par l'API Mistral
            messages = self._format_conversation_history(conversation_history)
            messages.append({
                "role": "user",
                "content": prompt
            })

            # Effectuer la requête POST à l'API Mistral
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )

            # Vérifier le succès de la requête
            response.raise_for_status()

            # Retourner le contenu de la réponse générée
            return response.json()["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as exc:
            logger.error(f"Erreur lors de la communication avec Mistral: {exc}")
            if hasattr(exc, "response") and exc.response is not None:
                logger.error(f"Réponse de l'API Mistral: {exc.response.text}")
            return "Une erreur est survenue lors de la communication avec Mistral AI."

    def _format_conversation_history(self, conversation_history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Transforme l'historique de conversation interne au format attendu par l'API Mistral.

        Args:
            conversation_history: Liste de messages avec expéditeur et contenu.

        Returns:
            Liste de messages formatés pour l'API Mistral.

        """
        return [
            {
                "role": "user" if msg.get("from") == "user" else "assistant",
                "content": msg.get("content", "")
            }
            for msg in conversation_history
        ]
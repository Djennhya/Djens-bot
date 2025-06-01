"""
Entrée principale pour le déploiement AWS Lambda.
Ce module adapte l'application FastAPI pour l'environnement Lambda via Mangum.

"""
import json
import logging
from mangum import Mangum

from .app import create_app
from .config.env import config

# Initialisation du logger pour Lambda
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = create_app()

# Adaptateur Mangum pour AWS Lambda
handler = Mangum(app)

def lambda_handler(event, context):
    """
    Gestionnaire Lambda pour traiter les événements API Gateway ou Telegram.

    Args:
        event: Données de l'événement Lambda.
        context: Contexte d'exécution Lambda.

    Returns:
        dict: Réponse HTTP adaptée à l'événement traité.
        
    """
    logger.info(f"Événement reçu par Lambda : {json.dumps(event)}")

    # Cas d'un appel via API Gateway HTTP
    if 'httpMethod' in event:
        return handler(event, context)

    # Cas d'un événement Telegram (par SNS ou webhook direct)
    if 'body' in event and isinstance(event['body'], str):
        try:
            body = json.loads(event['body'])
            if 'message' in body or 'callback_query' in body:
                logger.info("Mise à jour Telegram détectée dans l'événement Lambda.")
                # Ici, le bot Telegram gère la suite du traitement
                return {
                    'statusCode': 200,
                    'body': json.dumps({'status': 'ok'})
                }
        except json.JSONDecodeError:
            logger.error("Erreur de décodage JSON du corps de la requête.")

    # Si l'événement n'est pas reconnu
    logger.warning(f"Type d'événement non supporté : {event}")
    return {
        'statusCode': 400,
        'body': json.dumps({'error': "Type d'événement non pris en charge"})
    }
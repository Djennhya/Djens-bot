"""
Point d'entrée principal pour lancer le serveur FastAPI du chatbot Telegram.
Ce module vérifie la configuration, instancie l'application et démarre le serveur avec Uvicorn.
"""
import logging
import uvicorn
import sys
from .config.env import config, validate_env
from .app import create_app

# Initialisation du logger principal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Fonction principale pour initialiser et démarrer le serveur FastAPI.
    """
    # Vérification des variables d'environnement requises
    missing_vars = validate_env()
    if missing_vars:
        logger.error(f"Variables d'environnement manquantes : {', '.join(missing_vars)}")
        logger.error("Merci de compléter le fichier .env avec les variables nécessaires.")
        sys.exit(1)

    # Création de l'application FastAPI
    app = create_app()

    # Lancement du serveur Uvicorn
    logger.info(f"Lancement du serveur sur le port {config.PORT}")
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.ENV == "development"
    )

# Permet l'exécution directe du script
if __name__ == "__main__":
    main()

# Instance de l'application FastAPI pour Uvicorn
app = create_app()
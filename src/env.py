import os

class Config:
    # ... tes variables d'environnement ici ...
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    # etc.

config = Config()

def validate_env():
    # ... ta logique de validation ...
    return []
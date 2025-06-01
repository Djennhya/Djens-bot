import os

# Configuration du serveur
PORT = int(os.getenv('PORT', '3000'))
ENV = os.getenv('ENV', 'development')

# Configuration de Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Configuration de Mistral AI
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY', '')
MISTRAL_BASE_URL = 'https://api.mistral.ai/v1'
MISTRAL_MODEL = 'mistral-medium'

# Configuration de la base de données
DATABASE_URL = os.getenv('DATABASE_URL', '')
USE_MEMORY_ADAPTER = os.getenv('USE_MEMORY_ADAPTER', 'false').lower() == 'true'

# MongoDB (optionnel)
MONGODB_URI = os.getenv('MONGODB_URI', '')

# DynamoDB (optionnel)
AWS_REGION = os.getenv('AWS_REGION', 'eu-west-3')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
DYNAMO_TABLE = os.getenv('DYNAMO_TABLE', '')
AWS_PROFILE = os.getenv('AWS_PROFILE', 'esgis_profile')
ENV_NAME = os.getenv('ENV_NAME', 'tleguede-dev')
IS_LAMBDA_ENVIRONMENT = bool(os.getenv('AWS_LAMBDA_FUNCTION_NAME', ''))
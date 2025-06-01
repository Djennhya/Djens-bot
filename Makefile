.PHONY: bot run clean venv install build test deploy-local deploy serve test-endpoint

# Région et profil AWS par défaut
AWS_REGION ?= eu-west-3
AWS_PROFILE ?= "esgis_profile"
ENV_NAME ?= "djennhya"

# Lancer uniquement le bot Telegram
bot:
    python -m src.telegram_bot

# Lancer l'API FastAPI et le bot Telegram
run:
    python -m src.main

# Nettoyer les fichiers et dossiers générés
clean:
    if exist "venv" rd /s /q venv
    if exist "__pycache__" rd /s /q __pycache__
    if exist "*.egg-info" rd /s /q *.egg-info
    if exist ".pytest_cache" rd /s /q .pytest_cache
    if exist ".aws-sam" rd /s /q .aws-sam
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

# Créer un environnement virtuel Python
venv:
    python -m venv venv

# Installer les dépendances Python dans l'environnement virtuel
install: venv
    venv\Scripts\pip install -r requirements.txt

# Lancer les tests unitaires
test:
    venv\Scripts\pytest

# Construire le package AWS SAM
build:
    sam build --use-container -t infrastructure/template.yaml

# Démarrer l'API localement avec SAM
deploy-local:
    sam local start-api

# Déployer sur AWS avec SAM
deploy:
    @echo "Déploiement sur l'environnement ${ENV_NAME}"
    sam deploy --resolve-s3 --template-file .aws-sam/build/template.yaml --stack-name multi-stack-${ENV_NAME} \
         --capabilities CAPABILITY_IAM --region ${AWS_REGION} --parameter-overrides EnvironmentName=${ENV_NAME} --no-fail-on-empty-changeset

# Lancer le serveur FastAPI en mode développement
serve:
    venv\Scripts\python -m uvicorn src.main:app --reload

# Tester l'endpoint déployé sur AWS
test-endpoint:
    @echo "Test des endpoints déployés..."
    aws cloudformation describe-stacks --stack-name multi-stack-${ENV_NAME} --region ${AWS_REGION} \
        --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" --output text | xargs -I {} curl -X GET {}
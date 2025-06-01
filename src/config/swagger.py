"""
Fichier de configuration Swagger pour la documentation de l'API FastAPI.
Permet de personnaliser l'interface Swagger et les métadonnées OpenAPI.

"""
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

def setup_swagger(app: FastAPI) -> None:
    """
    Configure la documentation Swagger pour l'application FastAPI.

    Args:
        app: Instance de l'application FastAPI à configurer.

    """
    # Fonction interne pour personnaliser le schéma OpenAPI
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="Chatbot ESGIS - Mistral AI",
            version="1.0.0",
            description="API pour le chatbot Telegram intégré avec Mistral AI",
            routes=app.routes,
            openapi_version="3.0.2"
        )

        # Définition des tags personnalisés pour la documentation
        openapi_schema["tags"] = [
            {
                "name": "chat",
                "description": "Opérations liées au chat",
            },
            {
                "name": "health",
                "description": "Vérifications de l'état de santé",
            }
        ]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    # Route personnalisée pour afficher la page Swagger UI à la racine "/"
    @app.get("/", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Documentation API",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
        )
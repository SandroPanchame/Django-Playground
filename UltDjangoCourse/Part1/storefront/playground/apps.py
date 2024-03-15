from django.apps import AppConfig
# for application configuration, Mosh thinks it should have been called config

class PlaygroundConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "playground"

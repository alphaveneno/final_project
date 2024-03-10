"""
config for chat
"""
from django.apps import AppConfig


class ChatConfig(AppConfig):
    """
    chat config
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

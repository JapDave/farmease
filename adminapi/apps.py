from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = 'adminapi'

    def ready(self):
        import adminapi.signals
from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = 'subadmin'

    def ready(self):
        import subadmin.signals
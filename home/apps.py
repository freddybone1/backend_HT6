from django.apps import AppConfig


class MainAppConfig(AppConfig):
    name = 'home'

    def ready(self):
        import home.signals

from django.apps import AppConfig


class SistemConfig(AppConfig):
    name = 'sistem'

    def ready(self):
        import sistem.signals
from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'small_business.events'

    def ready(self):
        import small_business.events.signals.handlers

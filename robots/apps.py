from django.apps import AppConfig


class RobotsConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'robots'

    def ready(self):
        '''Импортируем сигналы при загрузке приложения'''
        import robots.signals

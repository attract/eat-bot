from django.apps import AppConfig


class FoodSitesConfig(AppConfig):
    name = 'food_sites'
    verbose_name = 'Food sites'

    def ready(self):
        import food_sites.signals

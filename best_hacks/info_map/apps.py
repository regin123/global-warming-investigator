from django.apps import AppConfig
from ..settings import DATABASES

class InfoMapConfig(AppConfig):
    name = 'best_hacks.info_map'
    def ready(self):
        DATABASES.update({
        })

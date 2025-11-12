from django.apps import AppConfig

class SgbUsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sgb_usuarios'
    
    def ready(self):
        import sgb_usuarios.signals
from django.contrib import admin

# Register your models here.
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'ativo_2fa', 'chave_2fa']
    list_filter = ['ativo_2fa']
    search_fields = ['user__username', 'user__email']
    
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import pyotp

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    chave_2fa = models.CharField(max_length=32, blank=True, null=True)
    ativo_2fa = models.BooleanField(default=False)
    
    def gerar_chave_2fa(self):
        self.chave_2fa = pyotp.random_base32()
        self.save()
        return self.chave_2fa
    
    def obter_uri_provisioning(self):
        if not self.chave_2fa:
            self.gerar_chave_2fa()
        totp = pyotp.TOTP(self.chave_2fa)
        return totp.provisioning_uri(
            name=self.user.email or self.user.username,
            issuer_name='Sistema Biblioteca'
        )
    
    def verificar_codigo_2fa(self, codigo):
        if not self.chave_2fa:
            return False
        totp = pyotp.TOTP(self.chave_2fa)
        return totp.verify(codigo, valid_window=1)
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
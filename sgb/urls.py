"""
URL configuration for sgb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect  # ← ADICIONE ESTA LINHA

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs existentes
    path('auth/', include('sgb_usuarios.urls')),
    path('livros/', include('sgb_livros.urls')),
    path('', lambda request: redirect('login')),
    
    # Recuperação de senha
    path('recuperar-senha/', 
         auth_views.PasswordResetView.as_view(
             template_name='sgb_usuarios/recuperar_senha.html',
             email_template_name='sgb_usuarios/recuperar_senha_email.html',
             subject_template_name='sgb_usuarios/recuperar_senha_assunto.txt',
             success_url='/recuperar-senha/enviado/'
         ), 
         name='password_reset'),
    
    path('recuperar-senha/enviado/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='sgb_usuarios/recuperar_senha_enviado.html'
         ), 
         name='password_reset_done'),
    
    path('redefinir/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='sgb_usuarios/redefinir_senha.html',
             success_url='/redefinir/concluido/'
         ), 
         name='password_reset_confirm'),
    
    path('redefinir/concluido/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='sgb_usuarios/redefinir_senha_concluido.html'
         ), 
         name='password_reset_complete'),
    
    # 2FA - REMOVA ESTA LINHA POR ENQUANTO (comentar até criar o arquivo)
    # path('verificar-2fa/', include('sgb_usuarios.urls_2fa')),
]
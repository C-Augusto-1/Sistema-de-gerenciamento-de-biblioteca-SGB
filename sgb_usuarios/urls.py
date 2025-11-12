from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticação básica
    path('cadastro/', views.cadastra_usuario, name='cadastro'),
    path('login/', views.loga_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    
    # Sistema de Recuperação de Senha
    # Etapa 1: Solicitar recuperação
    path('recuperar-senha/', 
         auth_views.PasswordResetView.as_view(
             template_name='sgb_usuarios/recuperar_senha.html',
             email_template_name='sgb_usuarios/email_recuperacao.html',
             subject_template_name='sgb_usuarios/email_recuperacao_assunto.txt',
             success_url='/auth/recuperar-senha/enviado/'
         ), 
         name='recuperar_senha'),
    
    # Etapa 2: Confirmação de envio do e-mail
    path('recuperar-senha/enviado/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='sgb_usuarios/recuperar_senha_enviado.html'
         ), 
         name='password_reset_done'),
    
    # Etapa 3: Formulário de nova senha (link do e-mail)
    path('redefinir/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='sgb_usuarios/redefinir_senha.html',
             success_url='/auth/redefinir/concluido/'
         ), 
         name='password_reset_confirm'),
    
    # Etapa 4: Confirmação de sucesso
    path('redefinir/concluido/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='sgb_usuarios/senha_redefinida.html'
         ), 
         name='password_reset_complete'),
]
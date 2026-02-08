"""
URL configuration for toca_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from torneios import views
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('torneios.urls')),
    
    # Login e Logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Recuperação de Senha
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        html_email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done') # Garante que ele vá para a URL certa
    ), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'), # O name precisa ser esse para o success_url acima funcionar
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Alteração de Senha (Dentro do sistema)
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url=reverse_lazy('perfil')  # Redireciona direto para o perfil após sucesso
    ), name='password_change'),
    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),

    # Perfil e Configurações
    path('perfil/config/', views.perfil_config, name='perfil_config'),
    path('perfil/atualizar/', views.atualizar_dados, name='atualizar_dados'),
]

if settings.DEBUG:
    urlpatterns += list(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
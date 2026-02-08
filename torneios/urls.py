from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quem-somos/', views.sobre, name='sobre'),
    path('torneio/<int:id>/', views.detalhe_torneio, name='detalhe_torneio'),
    path('torneio/<int:torneio_id>/inscrever/', views.inscrever_torneio, name='inscrever_torneio'),
    path('torneio/<int:torneio_id>/desistir/', views.desistir_torneio, name='desistir_torneio'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('perfil/', views.perfil, name='perfil'),
    path('torneio/<int:torneio_id>/exportar/', views.exportar_inscritos_csv, name='exportar_inscritos_csv'),
    path('torneios/proximos/', views.proximos_torneios, name='proximos_torneios'),
]
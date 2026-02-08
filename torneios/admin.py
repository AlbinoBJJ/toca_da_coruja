from django.contrib import admin
from .models import Jogador, Torneio

# Configuração personalizada para o modelo Jogador 👤
class JogadorAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na lista geral
    list_display = ('nome_completo', 'categoria', 'rating_local', 'user')
    
    # Adiciona uma barra de pesquisa por nome ou username
    search_fields = ('nome_completo', 'user__username')
    
    # Adiciona filtros na lateral direita
    list_filter = ('categoria', 'genero')

# Registramos o modelo com a configuração personalizada
admin.site.register(Jogador, JogadorAdmin)
admin.site.register(Torneio)
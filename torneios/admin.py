from django.contrib import admin
from .models import Jogador, Torneio


class JogadorAdmin(admin.ModelAdmin):

    list_display = ('nome_completo', 'categoria', 'rating_local', 'user')
    
    search_fields = ('nome_completo', 'user__username')
    list_filter = ('categoria', 'genero')


admin.site.register(Jogador, JogadorAdmin)
admin.site.register(Torneio)
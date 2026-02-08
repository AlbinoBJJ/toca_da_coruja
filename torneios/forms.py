from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Jogador
from datetime import date

class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")

    class Meta:
        model = User
        fields = ("username", "email")
        

class JogadorForm(forms.ModelForm):
    class Meta:
        model = Jogador
        fields = [
            'nome_completo', 'data_nascimento', 'genero', 
            'telefone', 'id_cbx', 'rating_cbx', 'rating_fide', 
            'username_chesscom', 'username_lichess', 'categoria'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nascimento = cleaned_data.get('data_nascimento')
        categoria_escolhida = cleaned_data.get('categoria')

        if nascimento and categoria_escolhida:
            ano_atual = 2026
            idade_ref = ano_atual - nascimento.year
            
            # Define o limite de idade para cada categoria
            limites = {
                'U8': 8, 'U10': 10, 'U12': 12, 'U14': 14, 
                'U16': 16, 'U18': 18, 'U20': 20
            }

            # Se a categoria escolhida for uma de base (U8 a U20)
            if categoria_escolhida in limites:
                if idade_ref > limites[categoria_escolhida]:
                    self.add_error('categoria', f'Sua idade ({idade_ref} anos) é superior ao limite da categoria {categoria_escolhida}.')
            
            # Se a categoria for Sênior 60+
            if categoria_escolhida == 'S60' and idade_ref < 60:
                self.add_error('categoria', 'A categoria S60 é exclusiva para jogadores com 60 anos ou mais.')

        return cleaned_data
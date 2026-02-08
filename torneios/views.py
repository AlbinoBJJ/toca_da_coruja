from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Torneio, Jogador
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CadastroForm
from .forms import JogadorForm
import csv
from django.http import HttpResponse
from datetime import date
from django.utils import timezone
import requests


def home(request):
    # Filtra apenas o torneio que está com inscrições abertas
    torneios_abertos = Torneio.objects.filter(status='ABERTO').order_by('data')
    return render(request, 'torneios/home.html', {'torneios': torneios_abertos})


def sobre(request):
    return render(request, 'torneios/sobre.html')


def detalhe_torneio(request, id):
    # 1. Buscamos o torneio ou retornamos erro 404 se não existir
    torneio = get_object_or_404(Torneio, id=id)
    
    # 2. Renderizamos o template passando o torneio encontrado
    return render(request, 'torneios/detalhe_torneio.html', {'torneio': torneio})


@login_required
def inscrever_torneio(request, torneio_id):
    # 1. Busca o torneio
    torneio = get_object_or_404(Torneio, id=torneio_id)
    
    if request.method == 'POST':
        # 2. Busca ou cria o perfil de Jogador do usuário logado
        # Use o related_name ou get_or_create como você já fazia
        jogador, created = Jogador.objects.get_or_create(user=request.user)
        
        # 3. Adiciona o jogador ao torneio (Lógica ManyToMany que você já usa)
        torneio.participantes.add(jogador)
        
        # Mensagem de sucesso para o usuário
        messages.success(request, f'Inscrição confirmada no {torneio.nome}! 🏆')
        
        # 4. Redireciona para os detalhes (o parâmetro é 'id' conforme sua url)
        return redirect('detalhe_torneio', id=torneio.id)
    
    # Se tentarem acessar via link direto (GET), mandamos de volta
    return redirect('proximos_torneios')


@login_required
def desistir_torneio(request, torneio_id):
    # 1. Busca o torneio
    torneio = get_object_or_404(Torneio, id=torneio_id)

    # 2. Busca ou cria o perfil de Jogador do usuário logado
    jogador, created = Jogador.objects.get_or_create(user=request.user)

    # 3. Adiciona o jogador ao torneio
    torneio.participantes.remove(jogador)
 
    # 4. Redireciona de volta para a página do torneio
    # 'detalhe_torneio' é o nome na URL
    return redirect('detalhe_torneio', id=torneio.id)



def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST) 
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Bem-vindo à Toca, {user.username}!')
            return redirect('login')
    else:
        form = CadastroForm() 
    
    return render(request, 'torneios/cadastro.html', {'form': form})


def buscar_ratings_chesscom(username):
    """Retorna os ratings de Blitz, Rapid e Bullet do Chess.com"""
    if not username:
        return None
    
    url = f"https://api.chess.com/pub/player/{username}/stats"
    # Lembre-se de colocar seu e-mail aqui para o Chess.com não te bloquear
    headers = {
        'User-Agent': 'TocaDaCoruja - seuemail@exemplo.com'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            dados = response.json()
            return {
                'blitz': dados.get('chess_blitz', {}).get('last', {}).get('rating', 'N/A'),
                'rapid': dados.get('chess_rapid', {}).get('last', {}).get('rating', 'N/A'),
                'bullet': dados.get('chess_bullet', {}).get('last', {}).get('rating', 'N/A'),
            }
    except Exception as e:
        print(f"Erro ao buscar Chess.com: {e}")
    return None

def buscar_ratings_lichess(username):
    """Retorna os ratings de Blitz, Rapid e Bullet do Lichess"""
    if not username:
        return None
    
    url = f"https://lichess.org/api/user/{username}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            dados = response.json()
            perfil_perfs = dados.get('perfs', {})
            return {
                'blitz': perfil_perfs.get('blitz', {}).get('rating', 'N/A'),
                'rapid': perfil_perfs.get('rapid', {}).get('rating', 'N/A'),
                'bullet': perfil_perfs.get('bullet', {}).get('rating', 'N/A'),
            }
    except Exception as e:
        print(f"Erro ao buscar Lichess: {e}")
    return None

@login_required
def perfil(request):
    jogador = request.user.jogador
    historico = jogador.torneios.all().order_by('-data')
    
    if request.method == 'POST':
        form = JogadorForm(request.POST, instance=jogador)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso! ✅")
            return redirect('perfil')
    else:
        form = JogadorForm(instance=jogador)
    
    # Busca os ratings de ambas as plataformas
    ratings_chesscom = buscar_ratings_chesscom(jogador.username_chesscom)
    ratings_lichess = buscar_ratings_lichess(jogador.username_lichess)

    return render(request, 'torneios/perfil.html', {
        'form': form,
        'historico': historico,
        'ratings_chesscom': ratings_chesscom,
        'ratings_lichess': ratings_lichess,
    })
    


def exportar_inscritos_csv(request, torneio_id):
    torneio = get_object_or_404(Torneio, id=torneio_id)
    # Buscamos todos os participantes vinculados a este torneio
    jogadores = torneio.participantes.all()

    # Criamos a resposta do Django como um arquivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inscritos_{torneio.nome}.csv"'

    writer = csv.writer(response, delimiter=';') # O Swiss Manager costuma aceitar ponto e vírgula

    # Escrevemos o cabeçalho EXATO que o Swiss Manager espera
    writer.writerow(['ID_No', 'Name', 'Sex', 'Fed', 'Clubnumber', 'ClubName', 'Birthday', 'Categ', 'Rtg_Nat'])

    # Agora precisamos percorrer a lista de jogadores e escrever os dados
    for jogador in jogadores:
    
        data_nasc = jogador.data_nascimento.strftime("%d/%m/%Y") if jogador.data_nascimento else ""
        
        # Escrevemos a linha no arquivo
        writer.writerow([
            jogador.id_cbx or "",
            jogador.nome_swiss(),
            jogador.genero or "",
            'BRA',
            jogador.id,
            'Toca da Coruja',
            data_nasc,
            jogador.categoria,
            jogador.rating_local or 0
        ])

    return response


def proximos_torneios(request):
    agora = timezone.now()
    # Filtra torneios com data maior ou igual a hoje, ordenando pelos mais próximos
    torneios = Torneio.objects.filter(data__gte=agora).order_by('data')
    
    return render(request, 'torneios/proximos_torneios.html', {
        'torneios': torneios
    })


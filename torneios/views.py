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
from django.contrib.auth.models import User


def home(request):
    torneios_abertos = Torneio.objects.filter(status='ABERTO').order_by('data')
    return render(request, 'torneios/home.html', {'torneios': torneios_abertos})


def sobre(request):
    return render(request, 'torneios/sobre.html')


def detalhe_torneio(request, id):
    torneio = get_object_or_404(Torneio, id=id)
    return render(request, 'torneios/detalhe_torneio.html', {'torneio': torneio})


@login_required
def inscrever_torneio(request, torneio_id):
    torneio = get_object_or_404(Torneio, id=torneio_id)   
    if request.method == 'POST':
        jogador, created = Jogador.objects.get_or_create(user=request.user)
        torneio.participantes.add(jogador)
        messages.success(request, f'Inscrição confirmada no {torneio.nome}! 🏆')
        return redirect('detalhe_torneio', id=torneio.id)
    return redirect('proximos_torneios')


@login_required
def desistir_torneio(request, torneio_id):
    torneio = get_object_or_404(Torneio, id=torneio_id)
    jogador, created = Jogador.objects.get_or_create(user=request.user)
    torneio.participantes.remove(jogador)
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
    if not username:
        return None
    url = f"https://api.chess.com/pub/player/{username}/stats"
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
    jogadores = torneio.participantes.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inscritos_{torneio.nome}.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID_No', 'Name', 'Sex', 'Fed', 'Clubnumber', 'ClubName', 'Birthday', 'Categ', 'Rtg_Nat'])
    for jogador in jogadores:
        data_nasc = jogador.data_nascimento.strftime("%d/%m/%Y") if jogador.data_nascimento else ""
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
    torneios = Torneio.objects.filter(data__gte=agora).order_by('data')
    return render(request, 'torneios/proximos_torneios.html', {
        'torneios': torneios
    })


@login_required
def atualizar_dados(request):
    if request.method == 'POST':
        user = request.user
        novo_username = request.POST.get('username')
        novo_email = request.POST.get('email')
        if User.objects.filter(username=novo_username).exclude(pk=user.pk).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return redirect('perfil_config')
        user.username = novo_username
        user.email = novo_email
        user.save()
        messages.success(request, "Seus dados foram atualizados com sucesso! ✅")
        return redirect('perfil_config')
    return redirect('perfil_config')


@login_required
def perfil_config(request):
    return render(request, 'registration/perfil_config.html')
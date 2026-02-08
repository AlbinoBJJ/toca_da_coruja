from django.db import models
from django.db.models import ManyToManyField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Torneio(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMAR', 'A Confirmar'),
        ('BREVE', 'Confirmado (Inscrições em breve)'),
        ('ABERTO', 'Inscrições Abertas'),
        ('ANDAMENTO', 'Em Andamento / Inscrições Encerradas'),
        ('ENCERRADO', 'Torneio Finalizado'),
    ]

    nome = models.CharField(max_length=200)
    data = models.DateField()
    local = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BREVE')
    imagem_capa = models.ImageField(upload_to='capas_torneios/', blank=True, null=True)

    participantes: ManyToManyField = models.ManyToManyField('Jogador', blank=True, related_name="torneios")

    def __str__(self):
        return self.nome

class Jogador(models.Model):
    CATEGORIAS = [
        ('U8', 'Sub-08'), ('U10', 'Sub-10'), ('U12', 'Sub-12'),
        ('U14', 'Sub-14'), ('U16', 'Sub-16'), ('U18', 'Sub-18'),
        ('U20', 'Sub-20'), ('S60', 'Sênior 60+'), ('ABERTO', 'Aberto'),
    ]
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(
        max_length=1, 
        choices=GENERO_CHOICES, 
        null=True, 
        blank=True
    )
    telefone = models.CharField(max_length=20, null=True, blank=True)
    rating_fide = models.IntegerField(null=True, blank=True)
    id_cbx = models.CharField(max_length=20, null=True, blank=True, verbose_name="ID CBX")
    rating_cbx = models.IntegerField(null=True, blank=True, verbose_name="Rating CBX")
    rating_local = models.IntegerField(null=True, blank=True, verbose_name="Rating Local")
    
    username_chesscom = models.CharField(max_length=100, null=True, blank=True, verbose_name="Usuário Chess.com")
    username_lichess = models.CharField(max_length=100, null=True, blank=True, verbose_name="Usuário Lichess.org")
    
    rating_atual = models.IntegerField(default=0)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, default='ABERTO')

    def nome_swiss(self):
        if not self.nome_completo:
            return self.user.username
        
        partes = self.nome_completo.split()
        if len(partes) > 1:
            # Pega o último nome e junta com o restante
            return f"{partes[-1].upper()}, {' '.join(partes[:-1])}"
        return self.nome_completo.upper()

    def __str__(self):
        return self.nome_completo or self.user.username
        
    class Meta:
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"

@receiver(post_save, sender=User)
def criar_perfil_jogador(sender, instance, created, **kwargs):
    if created:
        Jogador.objects.create(user=instance)
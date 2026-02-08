import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toca_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'AlbinoBJJ'
email = 'xadrezcabreuva@gmail.com'
password = 'Chessc@br3uva'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superusuario {username} criado com sucesso!")
else:
    print(f"Superusuario {username} ja existe.")
"""
Django settings for toca_project project.
"""

from pathlib import Path
import os
import dj_database_url

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURANÇA: A chave real ficará escondida no servidor. 
# Se não encontrar uma chave no servidor, usa a de desenvolvimento abaixo.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-lx@qizf3nsk*aot5^8@bj)&m8a0_xhxgqf@h#$)132@=q18uch')

# DEBUG: Ficará False automaticamente no servidor (se você configurar lá)
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# ALLOWED_HOSTS: Aceita o endereço do Render e o localhost
ALLOWED_HOSTS = ['*'] 

# Definição dos Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'torneios',
    'markdown_deux',
]

# Middlewares (WhiteNoise inserido na posição correta)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essencial para o CSS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'toca_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'toca_project.wsgi.application'

# Banco de Dados: Usa SQLite localmente e se adapta ao PostgreSQL no servidor
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Validação de Senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Arquivos Estáticos (CSS, JS)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuração do WhiteNoise para comprimir e cachear os arquivos
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# Arquivos de Mídia (Imagens enviadas por você)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Redirecionamentos de Login
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'home'

# Markdown Config
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            'a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
            'ul', 'li', 'ol', 'strong', 'em', 'br'
        ],
        "MARKDOWN_EXTENSIONS": [
            'markdown.extensions.nl2br', 
            'markdown.extensions.extra',
        ],
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'